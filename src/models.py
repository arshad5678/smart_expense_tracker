"""Models and Schemas module for the Smart Expense Tracker API.

This module contains the Pydantic models used for input validation,
response serialization, and API documentation.
"""

import datetime
from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    """Pydantic model representing the schema for creating an expense."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="The title or brief description of the expense.",
        examples=["Coffee with client"],
    )
    amount: float = Field(
        ...,
        gt=0,
        description="The total cost of the expense. Must be greater than 0.",
        examples=[4.50],
    )
    category: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="The category of the expense.",
        examples=["Food & Dining"],
    )
    date: datetime.date = Field(
        ...,
        description="The date when the expense was incurred (YYYY-MM-DD).",
        examples=["2026-07-31"],
    )


class Expense(ExpenseCreate):
    """Pydantic model representing a persisted expense with a unique identifier."""

    id: int = Field(
        ..., description="The unique identifier of the expense.", examples=[1]
    )
