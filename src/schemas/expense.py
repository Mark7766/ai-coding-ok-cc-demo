from __future__ import annotations

from datetime import date as Date

from pydantic import BaseModel, Field

CATEGORIES: list[str] = ["餐饮", "交通", "购物", "娱乐", "医疗", "居家", "其他"]

CATEGORY_EMOJI: dict[str, str] = {
    "餐饮": "🍜",
    "交通": "🚇",
    "购物": "🛍️",
    "娱乐": "🎮",
    "医疗": "💊",
    "居家": "🏠",
    "其他": "📦",
}

CATEGORY_COLOR: dict[str, str] = {
    "餐饮": "#f97316",
    "交通": "#3b82f6",
    "购物": "#a855f7",
    "娱乐": "#ec4899",
    "医疗": "#ef4444",
    "居家": "#22c55e",
    "其他": "#94a3b8",
}

INCOME_CATEGORIES: list[str] = ["工资", "奖金", "副业", "投资", "其他收入"]

INCOME_CATEGORY_EMOJI: dict[str, str] = {
    "工资": "💼",
    "奖金": "🎁",
    "副业": "💡",
    "投资": "📈",
    "其他收入": "💰",
}

INCOME_CATEGORY_COLOR: dict[str, str] = {
    "工资": "#16a34a",
    "奖金": "#0ea5e9",
    "副业": "#8b5cf6",
    "投资": "#f59e0b",
    "其他收入": "#64748b",
}


class ExpenseCreate(BaseModel):
    """Schema for creating a new expense or income record."""

    amount: float = Field(..., gt=0, description="金额（元）")
    category: str = Field(..., description="分类")
    record_type: str = Field("支出", description="记录类型：支出 或 收入")
    note: str | None = Field(None, max_length=200, description="备注")
    date: Date = Field(..., description="日期")


class ExpenseResponse(BaseModel):
    """Schema for expense/income record response."""

    id: int
    amount: float
    category: str
    record_type: str
    note: str | None
    date: Date

    model_config = {"from_attributes": True}


class DailyStats(BaseModel):
    """Daily expense statistics."""

    date: Date
    total: float
    count: int


class CategoryStats(BaseModel):
    """Per-category expense statistics."""

    category: str
    total: float
    count: int
    color: str = ""
    emoji: str = ""
    pct: float = 0.0


class MonthlyStats(BaseModel):
    """Monthly expense statistics."""

    year: int
    month: int
    total: float
    by_category: list[CategoryStats]
    by_day: list[DailyStats]


class DashboardStats(BaseModel):
    """Monthly dashboard: income vs expense breakdown."""

    year: int
    month: int
    total_income: float
    total_expense: float
    net: float
    income_by_category: list[CategoryStats]
    expense_by_category: list[CategoryStats]
