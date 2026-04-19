from __future__ import annotations

from datetime import date

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.expense import ExpenseCreate
from src.services.expense_service import expense_service


class TestIndexPage:
    async def test_index_returns_200(self, client: AsyncClient) -> None:
        resp = await client.get("/")
        assert resp.status_code == 200

    async def test_index_with_date_param(self, client: AsyncClient) -> None:
        resp = await client.get("/?date=2026-04-19")
        assert resp.status_code == 200
        assert "2026" in resp.text

    async def test_index_shows_expense_in_list(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        data = ExpenseCreate(amount=42.0, category="餐饮", note="午饭", date=date(2026, 4, 19))
        await expense_service.create(db_session, data)

        resp = await client.get("/?date=2026-04-19")
        assert resp.status_code == 200
        assert "42.00" in resp.text
        assert "午饭" in resp.text


class TestCreateExpense:
    async def test_create_redirects_to_index(self, client: AsyncClient) -> None:
        resp = await client.post(
            "/expenses/create",
            data={"amount": "25.0", "category": "交通", "note": "", "expense_date": "2026-04-19"},
            follow_redirects=False,
        )
        assert resp.status_code == 303
        assert "date=2026-04-19" in resp.headers["location"]

    async def test_create_stores_expense(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await client.post(
            "/expenses/create",
            data={"amount": "8.5", "category": "交通", "note": "地铁", "expense_date": "2026-04-20"},
        )
        expenses = await expense_service.list_by_date(db_session, date(2026, 4, 20))
        assert len(expenses) == 1
        assert expenses[0].amount == pytest.approx(8.5)
        assert expenses[0].note == "地铁"


class TestDeleteExpense:
    async def test_delete_existing_returns_ok(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        data = ExpenseCreate(amount=10.0, category="购物", note=None, date=date(2026, 4, 19))
        expense = await expense_service.create(db_session, data)

        resp = await client.delete(f"/api/expenses/{expense.id}")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}

    async def test_delete_nonexistent_returns_404(self, client: AsyncClient) -> None:
        resp = await client.delete("/api/expenses/99999")
        assert resp.status_code == 404

    async def test_delete_removes_from_db(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        data = ExpenseCreate(amount=10.0, category="购物", note=None, date=date(2026, 4, 19))
        expense = await expense_service.create(db_session, data)

        await client.delete(f"/api/expenses/{expense.id}")
        remaining = await expense_service.list_by_date(db_session, date(2026, 4, 19))
        assert all(e.id != expense.id for e in remaining)


class TestCreateWithType:
    async def test_create_income_record(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await client.post(
            "/expenses/create",
            data={
                "amount": "5000.0",
                "category": "工资",
                "record_type": "收入",
                "note": "四月工资",
                "expense_date": "2026-04-30",
            },
        )
        records = await expense_service.list_by_date(db_session, date(2026, 4, 30))
        assert len(records) == 1
        assert records[0].record_type == "收入"
        assert records[0].category == "工资"


class TestDashboardPage:
    async def test_dashboard_returns_200(self, client: AsyncClient) -> None:
        resp = await client.get("/dashboard")
        assert resp.status_code == 200

    async def test_dashboard_with_year_month_params(self, client: AsyncClient) -> None:
        resp = await client.get("/dashboard?year=2026&month=4")
        assert resp.status_code == 200
        assert "2026" in resp.text

    async def test_dashboard_shows_income_and_expense(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        data_income = ExpenseCreate(amount=5000.0, category="工资", record_type="收入", date=date(2026, 4, 1))
        data_expense = ExpenseCreate(amount=200.0, category="餐饮", record_type="支出", date=date(2026, 4, 2))
        await expense_service.create(db_session, data_income)
        await expense_service.create(db_session, data_expense)

        resp = await client.get("/dashboard?year=2026&month=4")
        assert resp.status_code == 200
        assert "工资" in resp.text
        assert "餐饮" in resp.text
        assert "5000.00" in resp.text
        assert "200.00" in resp.text


class TestStatsPage:
    async def test_stats_returns_200(self, client: AsyncClient) -> None:
        resp = await client.get("/stats")
        assert resp.status_code == 200

    async def test_stats_with_year_month_params(self, client: AsyncClient) -> None:
        resp = await client.get("/stats?year=2026&month=4")
        assert resp.status_code == 200
        assert "2026" in resp.text
        assert "4" in resp.text

    async def test_stats_shows_category_data(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        data = ExpenseCreate(amount=50.0, category="餐饮", note=None, date=date(2026, 4, 10))
        await expense_service.create(db_session, data)

        resp = await client.get("/stats?year=2026&month=4")
        assert "餐饮" in resp.text
        assert "50.00" in resp.text
