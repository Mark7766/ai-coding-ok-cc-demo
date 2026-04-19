from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.services.expense_service import expense_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/expenses", tags=["expenses"])


@router.delete("/{expense_id}")
async def delete_expense(expense_id: int, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Delete an expense by ID.

    Args:
        expense_id: The ID of the expense to delete.
        db: Injected async database session.

    Returns:
        JSON confirmation message.

    Raises:
        HTTPException: 404 if expense not found.
    """
    deleted = await expense_service.delete(db, expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"status": "ok"}
