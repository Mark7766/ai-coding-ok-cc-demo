from __future__ import annotations

from datetime import date

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.expense import ExpenseCreate
from src.services.expense_service import expense_service


async def _create_expense(
    db: AsyncSession,
    amount: float = 10.0,
    category: str = "餐饮",
    note: str | None = None,
    target_date: date = date(2026, 4, 19),
    record_type: str = "支出",
) -> int:
    """Helper: create an expense/income record and return its ID."""
    data = ExpenseCreate(amount=amount, category=category, record_type=record_type, note=note, date=target_date)
    expense = await expense_service.create(db, data)
    return expense.id


class TestCreate:
    async def test_create_expense_returns_correct_fields(self, db_session: AsyncSession) -> None:
        # Arrange
        data = ExpenseCreate(amount=15.5, category="交通", note="地铁", date=date(2026, 4, 19))

        # Act
        expense = await expense_service.create(db_session, data)

        # Assert
        assert expense.id is not None
        assert expense.amount == 15.5
        assert expense.category == "交通"
        assert expense.note == "地铁"
        assert expense.date == date(2026, 4, 19)

    async def test_create_expense_without_note(self, db_session: AsyncSession) -> None:
        data = ExpenseCreate(amount=8.0, category="餐饮", note=None, date=date(2026, 4, 19))
        expense = await expense_service.create(db_session, data)
        assert expense.note is None


class TestListByDate:
    async def test_list_by_date_returns_expenses_for_that_date(self, db_session: AsyncSession) -> None:
        # Arrange — add two expenses on target date, one on another date
        await _create_expense(db_session, amount=10.0, target_date=date(2026, 4, 19))
        await _create_expense(db_session, amount=5.0, target_date=date(2026, 4, 19))
        await _create_expense(db_session, amount=99.0, target_date=date(2026, 4, 20))

        # Act
        results = await expense_service.list_by_date(db_session, date(2026, 4, 19))

        # Assert
        assert len(results) == 2
        amounts = {e.amount for e in results}
        assert amounts == {10.0, 5.0}

    async def test_list_by_date_returns_empty_for_no_records(self, db_session: AsyncSession) -> None:
        results = await expense_service.list_by_date(db_session, date(2026, 1, 1))
        assert results == []


class TestDelete:
    async def test_delete_existing_expense_returns_true(self, db_session: AsyncSession) -> None:
        expense_id = await _create_expense(db_session)
        result = await expense_service.delete(db_session, expense_id)
        assert result is True

    async def test_delete_nonexistent_expense_returns_false(self, db_session: AsyncSession) -> None:
        result = await expense_service.delete(db_session, 99999)
        assert result is False

    async def test_delete_removes_from_db(self, db_session: AsyncSession) -> None:
        expense_id = await _create_expense(db_session, target_date=date(2026, 4, 19))
        await expense_service.delete(db_session, expense_id)
        remaining = await expense_service.list_by_date(db_session, date(2026, 4, 19))
        assert all(e.id != expense_id for e in remaining)


class TestGetDailyTotal:
    async def test_daily_total_sums_correctly(self, db_session: AsyncSession) -> None:
        await _create_expense(db_session, amount=10.0, target_date=date(2026, 4, 19))
        await _create_expense(db_session, amount=5.5, target_date=date(2026, 4, 19))
        await _create_expense(db_session, amount=100.0, target_date=date(2026, 4, 20))  # different date

        total = await expense_service.get_daily_total(db_session, date(2026, 4, 19))
        assert total == pytest.approx(15.5)

    async def test_daily_total_excludes_income(self, db_session: AsyncSession) -> None:
        await _create_expense(db_session, amount=10.0, target_date=date(2026, 4, 19), record_type="支出")
        await _create_expense(db_session, amount=500.0, target_date=date(2026, 4, 19), record_type="收入")

        total = await expense_service.get_daily_total(db_session, date(2026, 4, 19))
        assert total == pytest.approx(10.0)

    async def test_daily_total_returns_zero_for_empty_day(self, db_session: AsyncSession) -> None:
        total = await expense_service.get_daily_total(db_session, date(2026, 1, 1))
        assert total == 0.0


class TestGetMonthlyStats:
    async def test_monthly_stats_total(self, db_session: AsyncSession) -> None:
        await _create_expense(db_session, amount=30.0, category="餐饮", target_date=date(2026, 4, 1))
        await _create_expense(db_session, amount=20.0, category="交通", target_date=date(2026, 4, 15))
        await _create_expense(db_session, amount=999.0, target_date=date(2026, 5, 1))  # different month

        stats = await expense_service.get_monthly_stats(db_session, 2026, 4)
        assert stats.total == pytest.approx(50.0)

    async def test_monthly_stats_by_category(self, db_session: AsyncSession) -> None:
        await _create_expense(db_session, amount=40.0, category="餐饮", target_date=date(2026, 4, 1))
        await _create_expense(db_session, amount=20.0, category="餐饮", target_date=date(2026, 4, 2))
        await _create_expense(db_session, amount=10.0, category="交通", target_date=date(2026, 4, 3))

        stats = await expense_service.get_monthly_stats(db_session, 2026, 4)
        assert len(stats.by_category) == 2
        # 餐饮 should be first (highest total)
        assert stats.by_category[0].category == "餐饮"
        assert stats.by_category[0].total == pytest.approx(60.0)

    async def test_monthly_stats_by_category_includes_pct(self, db_session: AsyncSession) -> None:
        await _create_expense(db_session, amount=75.0, category="餐饮", target_date=date(2026, 4, 1))
        await _create_expense(db_session, amount=25.0, category="交通", target_date=date(2026, 4, 1))

        stats = await expense_service.get_monthly_stats(db_session, 2026, 4)
        cat_map = {c.category: c for c in stats.by_category}
        assert cat_map["餐饮"].pct == pytest.approx(75.0)
        assert cat_map["交通"].pct == pytest.approx(25.0)

    async def test_monthly_stats_excludes_income(self, db_session: AsyncSession) -> None:
        await _create_expense(db_session, amount=30.0, category="餐饮", target_date=date(2026, 4, 1), record_type="支出")
        await _create_expense(db_session, amount=5000.0, category="工资", target_date=date(2026, 4, 1), record_type="收入")

        stats = await expense_service.get_monthly_stats(db_session, 2026, 4)
        assert stats.total == pytest.approx(30.0)

    async def test_monthly_stats_empty_month_returns_zeros(self, db_session: AsyncSession) -> None:
        stats = await expense_service.get_monthly_stats(db_session, 2020, 1)
        assert stats.total == 0.0
        assert stats.by_category == []
        assert stats.by_day == []


class TestGetDashboardStats:
    async def test_dashboard_separates_income_and_expense(self, db_session: AsyncSession) -> None:
        await _create_expense(db_session, amount=200.0, category="餐饮", target_date=date(2026, 4, 1), record_type="支出")
        await _create_expense(db_session, amount=5000.0, category="工资", target_date=date(2026, 4, 5), record_type="收入")

        stats = await expense_service.get_dashboard_stats(db_session, 2026, 4)
        assert stats.total_expense == pytest.approx(200.0)
        assert stats.total_income == pytest.approx(5000.0)
        assert stats.net == pytest.approx(4800.0)

    async def test_dashboard_income_by_category(self, db_session: AsyncSession) -> None:
        await _create_expense(db_session, amount=5000.0, category="工资", target_date=date(2026, 4, 1), record_type="收入")
        await _create_expense(db_session, amount=500.0, category="副业", target_date=date(2026, 4, 10), record_type="收入")

        stats = await expense_service.get_dashboard_stats(db_session, 2026, 4)
        assert len(stats.income_by_category) == 2
        assert stats.income_by_category[0].category == "工资"
        assert stats.income_by_category[0].pct == pytest.approx(5000 / 5500 * 100, abs=0.1)

    async def test_dashboard_expense_by_category(self, db_session: AsyncSession) -> None:
        await _create_expense(db_session, amount=300.0, category="餐饮", target_date=date(2026, 4, 1), record_type="支出")
        await _create_expense(db_session, amount=100.0, category="交通", target_date=date(2026, 4, 2), record_type="支出")

        stats = await expense_service.get_dashboard_stats(db_session, 2026, 4)
        assert len(stats.expense_by_category) == 2
        assert stats.expense_by_category[0].category == "餐饮"

    async def test_dashboard_net_negative_when_spending_exceeds_income(self, db_session: AsyncSession) -> None:
        await _create_expense(db_session, amount=1000.0, category="购物", target_date=date(2026, 4, 1), record_type="支出")
        await _create_expense(db_session, amount=200.0, category="奖金", target_date=date(2026, 4, 5), record_type="收入")

        stats = await expense_service.get_dashboard_stats(db_session, 2026, 4)
        assert stats.net == pytest.approx(-800.0)

    async def test_dashboard_empty_month_returns_zeros(self, db_session: AsyncSession) -> None:
        stats = await expense_service.get_dashboard_stats(db_session, 2020, 1)
        assert stats.total_income == 0.0
        assert stats.total_expense == 0.0
        assert stats.net == 0.0
        assert stats.income_by_category == []
        assert stats.expense_by_category == []
