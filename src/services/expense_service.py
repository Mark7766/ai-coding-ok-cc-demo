from __future__ import annotations

import logging
from datetime import date

from sqlalchemy import extract, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.expense import Expense
from src.schemas.expense import (
    CATEGORY_COLOR,
    CATEGORY_EMOJI,
    INCOME_CATEGORY_COLOR,
    INCOME_CATEGORY_EMOJI,
    CategoryStats,
    DailyStats,
    DashboardStats,
    ExpenseCreate,
    MonthlyStats,
)

logger = logging.getLogger(__name__)


class ExpenseService:
    """Service layer for expense operations."""

    async def create(self, db: AsyncSession, data: ExpenseCreate) -> Expense:
        """Create a new expense record.

        Args:
            db: Async database session.
            data: Validated expense creation data.

        Returns:
            The created Expense ORM instance.
        """
        expense = Expense(**data.model_dump())
        db.add(expense)
        await db.commit()
        await db.refresh(expense)
        logger.info(
            "Expense created: id=%s, amount=%.2f, category=%s, date=%s",
            expense.id,
            expense.amount,
            expense.category,
            expense.date,
        )
        return expense

    async def list_by_date(self, db: AsyncSession, target_date: date) -> list[Expense]:
        """List all expenses for a given date, newest first.

        Args:
            db: Async database session.
            target_date: The date to query.

        Returns:
            List of Expense instances.
        """
        result = await db.execute(
            select(Expense).where(Expense.date == target_date).order_by(Expense.id.desc())
        )
        return list(result.scalars().all())

    async def delete(self, db: AsyncSession, expense_id: int) -> bool:
        """Delete an expense by ID.

        Args:
            db: Async database session.
            expense_id: Primary key of the expense to delete.

        Returns:
            True if deleted, False if not found.
        """
        expense = await db.get(Expense, expense_id)
        if expense is None:
            return False
        await db.delete(expense)
        await db.commit()
        logger.info("Expense deleted: id=%s", expense_id)
        return True

    async def get_daily_total(self, db: AsyncSession, target_date: date) -> float:
        """Get total expense spending for a given date (excludes income).

        Args:
            db: Async database session.
            target_date: The date to sum.

        Returns:
            Total expense amount as float (0.0 if no records).
        """
        result = await db.execute(
            select(func.sum(Expense.amount)).where(
                Expense.date == target_date, Expense.record_type == "支出"
            )
        )
        return float(result.scalar() or 0.0)

    async def get_daily_income(self, db: AsyncSession, target_date: date) -> float:
        """Get total income for a given date.

        Args:
            db: Async database session.
            target_date: The date to sum.

        Returns:
            Total income amount as float (0.0 if no records).
        """
        result = await db.execute(
            select(func.sum(Expense.amount)).where(
                Expense.date == target_date, Expense.record_type == "收入"
            )
        )
        return float(result.scalar() or 0.0)

    async def get_monthly_stats(self, db: AsyncSession, year: int, month: int) -> MonthlyStats:
        """Get monthly expense statistics.

        Args:
            db: Async database session.
            year: The year (e.g. 2026).
            month: The month (1-12).

        Returns:
            MonthlyStats with totals, category breakdown, and daily breakdown.
        """
        date_filter = (
            extract("year", Expense.date) == year,
            extract("month", Expense.date) == month,
            Expense.record_type == "支出",
        )

        total_result = await db.execute(select(func.sum(Expense.amount)).where(*date_filter))
        total = float(total_result.scalar() or 0.0)

        cat_result = await db.execute(
            select(Expense.category, func.sum(Expense.amount), func.count(Expense.id))
            .where(*date_filter)
            .group_by(Expense.category)
            .order_by(func.sum(Expense.amount).desc())
        )
        by_category = [
            CategoryStats(
                category=row[0],
                total=float(row[1]),
                count=int(row[2]),
                color=CATEGORY_COLOR.get(row[0], "#94a3b8"),
                emoji=CATEGORY_EMOJI.get(row[0], "📦"),
                pct=round(float(row[1]) / total * 100, 1) if total > 0 else 0.0,
            )
            for row in cat_result.all()
        ]

        day_result = await db.execute(
            select(Expense.date, func.sum(Expense.amount), func.count(Expense.id))
            .where(*date_filter)
            .group_by(Expense.date)
            .order_by(Expense.date.desc())
        )
        by_day = [
            DailyStats(date=row[0], total=float(row[1]), count=int(row[2]))
            for row in day_result.all()
        ]

        return MonthlyStats(year=year, month=month, total=total, by_category=by_category, by_day=by_day)

    async def get_dashboard_stats(self, db: AsyncSession, year: int, month: int) -> DashboardStats:
        """Get monthly dashboard statistics: income vs expense by category.

        Args:
            db: Async database session.
            year: The year (e.g. 2026).
            month: The month (1-12).

        Returns:
            DashboardStats with income/expense totals and category breakdowns.
        """
        date_filter = (
            extract("year", Expense.date) == year,
            extract("month", Expense.date) == month,
        )

        income_total_result = await db.execute(
            select(func.sum(Expense.amount)).where(*date_filter, Expense.record_type == "收入")
        )
        total_income = float(income_total_result.scalar() or 0.0)

        expense_total_result = await db.execute(
            select(func.sum(Expense.amount)).where(*date_filter, Expense.record_type == "支出")
        )
        total_expense = float(expense_total_result.scalar() or 0.0)

        income_cat_result = await db.execute(
            select(Expense.category, func.sum(Expense.amount), func.count(Expense.id))
            .where(*date_filter, Expense.record_type == "收入")
            .group_by(Expense.category)
            .order_by(func.sum(Expense.amount).desc())
        )
        income_by_category = [
            CategoryStats(
                category=row[0],
                total=float(row[1]),
                count=int(row[2]),
                color=INCOME_CATEGORY_COLOR.get(row[0], "#16a34a"),
                emoji=INCOME_CATEGORY_EMOJI.get(row[0], "💰"),
                pct=round(float(row[1]) / total_income * 100, 1) if total_income > 0 else 0.0,
            )
            for row in income_cat_result.all()
        ]

        expense_cat_result = await db.execute(
            select(Expense.category, func.sum(Expense.amount), func.count(Expense.id))
            .where(*date_filter, Expense.record_type == "支出")
            .group_by(Expense.category)
            .order_by(func.sum(Expense.amount).desc())
        )
        expense_by_category = [
            CategoryStats(
                category=row[0],
                total=float(row[1]),
                count=int(row[2]),
                color=CATEGORY_COLOR.get(row[0], "#94a3b8"),
                emoji=CATEGORY_EMOJI.get(row[0], "📦"),
                pct=round(float(row[1]) / total_expense * 100, 1) if total_expense > 0 else 0.0,
            )
            for row in expense_cat_result.all()
        ]

        return DashboardStats(
            year=year,
            month=month,
            total_income=total_income,
            total_expense=total_expense,
            net=total_income - total_expense,
            income_by_category=income_by_category,
            expense_by_category=expense_by_category,
        )


expense_service = ExpenseService()
