from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, AsyncGenerator

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.expenses import router as expenses_router
from src.database import get_db, init_db
from src.schemas.expense import CATEGORIES, INCOME_CATEGORIES, ExpenseCreate
from src.services.expense_service import expense_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEMPLATES_DIR = Path(__file__).parent / "templates"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: create data dir and initialize DB on startup."""
    Path("data").mkdir(exist_ok=True)
    await init_db()
    logger.info("Database initialized")
    yield


app = FastAPI(title="记账本", lifespan=lifespan)
app.include_router(expenses_router)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/", response_class=Response)
async def index(
    request: Request,
    date: date | None = None,  # type: ignore[assignment]
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Render main page with expenses for the given date.

    Args:
        request: FastAPI request object.
        date: Date to display (defaults to today).
        db: Injected async database session.
    """
    target_date: date = date or _today()  # type: ignore[assignment]
    expenses = await expense_service.list_by_date(db, target_date)
    total = await expense_service.get_daily_total(db, target_date)

    income = await expense_service.get_daily_income(db, target_date)
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "date": target_date,
            "expenses": expenses,
            "total": total,
            "income": income,
            "categories": CATEGORIES,
            "income_categories": INCOME_CATEGORIES,
            "prev_date": target_date - timedelta(days=1),
            "next_date": target_date + timedelta(days=1),
            "is_today": target_date == _today(),
        },
    )


@app.post("/expenses/create")
async def create_expense(
    request: Request,
    amount: float = Form(...),
    category: str = Form(...),
    record_type: str = Form("支出"),
    note: str = Form(""),
    expense_date: date = Form(...),
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse:
    """Handle expense/income creation form submission.

    Args:
        request: FastAPI request object.
        amount: Amount in yuan.
        category: Record category.
        record_type: "支出" or "收入".
        note: Optional note (empty string treated as None).
        expense_date: Date of the record.
        db: Injected async database session.
    """
    data = ExpenseCreate(
        amount=amount,
        category=category,
        record_type=record_type,
        note=note.strip() or None,
        date=expense_date,
    )
    await expense_service.create(db, data)
    return RedirectResponse(url=f"/?date={expense_date}", status_code=303)


@app.get("/stats", response_class=Response)
async def stats(
    request: Request,
    year: int | None = None,
    month: int | None = None,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Render monthly statistics page.

    Args:
        request: FastAPI request object.
        year: Year to show (defaults to current year).
        month: Month to show (defaults to current month).
        db: Injected async database session.
    """
    today = _today()
    display_year = year or today.year
    display_month = month or today.month

    stats_data = await expense_service.get_monthly_stats(db, display_year, display_month)
    prev_month, prev_year = _prev_month(display_year, display_month)
    next_month, next_year = _next_month(display_year, display_month)

    return templates.TemplateResponse(
        request,
        "stats.html",
        {
            "stats": stats_data,
            "prev_year": prev_year,
            "prev_month": prev_month,
            "next_year": next_year,
            "next_month": next_month,
            "today": today,
        },
    )


@app.get("/dashboard", response_class=Response)
async def dashboard(
    request: Request,
    year: int | None = None,
    month: int | None = None,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Render personal finance dashboard.

    Args:
        request: FastAPI request object.
        year: Year to show (defaults to current year).
        month: Month to show (defaults to current month).
        db: Injected async database session.
    """
    today = _today()
    display_year = year or today.year
    display_month = month or today.month

    stats_data = await expense_service.get_dashboard_stats(db, display_year, display_month)
    prev_month, prev_year = _prev_month(display_year, display_month)
    next_month, next_year = _next_month(display_year, display_month)

    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "stats": stats_data,
            "prev_year": prev_year,
            "prev_month": prev_month,
            "next_year": next_year,
            "next_month": next_month,
            "today": today,
        },
    )


def _today() -> date:
    """Return today's date."""
    return datetime.now().date()


def _prev_month(year: int, month: int) -> tuple[int, int]:
    """Return (month, year) for the previous month."""
    if month == 1:
        return 12, year - 1
    return month - 1, year


def _next_month(year: int, month: int) -> tuple[int, int]:
    """Return (month, year) for the next month."""
    if month == 12:
        return 1, year + 1
    return month + 1, year
