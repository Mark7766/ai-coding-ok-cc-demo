from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Expense(Base):
    """Expense record model."""

    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    record_type: Mapped[str] = mapped_column(String(10), nullable=False, server_default="支出")
    note: Mapped[str | None] = mapped_column(String(200), nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"Expense(id={self.id}, amount={self.amount}, category={self.category!r}, date={self.date})"
