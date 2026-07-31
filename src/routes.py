from fastapi import APIRouter, status, HTTPException
from typing import Any, Dict, List, Optional

from src.models import Expense, ExpenseCreate
from src.storage import load_expenses, save_expenses, get_next_id

router = APIRouter()


@router.get("/health")
def check_health() -> Dict[str, str]:
    """Check the health status of the API.

    Returns:
        Dict[str, str]: A dictionary indicating the health status of the
        service.
    """
    return {"status": "healthy"}


@router.post(
    "/expenses",
    response_model=Expense,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new expense",
    description=(
        "Create a new expense entry, generate a unique integer ID, and persist"
        " it to the storage."
    ),
)
def create_expense(expense_in: ExpenseCreate) -> Expense:
    """Create a new expense record.

    Loads existing expenses, generates a unique ID, builds a new Expense object,
    serializes it to a JSON-compatible dictionary, appends it to the list, saves
    the updated list, and returns the newly created Expense object.
    """
    expenses = load_expenses()
    new_id = get_next_id(expenses)

    new_expense = Expense(id=new_id, **expense_in.model_dump())
    new_expense_dict = new_expense.model_dump(mode="json")

    expenses.append(new_expense_dict)
    save_expenses(expenses)

    return new_expense


@router.get(
    "/expenses",
    response_model=List[Expense],
    summary="Retrieve all expenses",
    description=(
        "Retrieve a list of all expense records, optionally filtered by"
        " category (case-insensitive)."
    ),
)
def get_expenses(category: Optional[str] = None) -> List[Expense]:
    """Retrieve expense records.

    Loads all expenses from storage, optionally filters them by category
    (case-insensitive), and returns the matching expense records.
    """
    raw_expenses = load_expenses()

    if category is not None:
        target_category = category.strip().lower()
        raw_expenses = [
            exp
            for exp in raw_expenses
            if isinstance(exp.get("category"), str)
            and exp["category"].strip().lower() == target_category
        ]

    return [Expense(**e) for e in raw_expenses]


@router.get(
    "/expenses/summary",
    response_model=Dict[str, Any],
    summary="Get expenses summary",
    description=(
        "Calculate and return the overall total spend and a category-wise"
        " breakdown of expenses."
    ),
)
def get_expenses_summary() -> Dict[str, Any]:
    """Retrieve a summary of expenses.

    Calculates the sum of all expenses (overall) and a category-wise
    breakdown of the total spent in each category.

    Returns:
        Dict[str, Any]: A dictionary containing overall spend and by-category spend.
    """
    raw_expenses = load_expenses()

    overall = sum(exp.get("amount", 0.0) for exp in raw_expenses)

    by_category: Dict[str, float] = {}
    for exp in raw_expenses:
        category = exp.get("category")
        amount = exp.get("amount", 0.0)
        if isinstance(category, str):
            by_category[category] = by_category.get(category, 0.0) + amount

    return {"overall": overall, "by_category": by_category}


@router.delete(
    "/expenses/{expense_id}",
    response_model=Dict[str, str],
    summary="Delete an expense",
    description="Remove an expense record by its unique integer ID from the database.",
)
def delete_expense(expense_id: int) -> Dict[str, str]:
    """Delete an expense record.

    Loads all expenses, searches for the expense with the matching ID, removes
    it if found, updates the storage file, and returns a success message.
    Raises HTTPException 404 if the ID does not exist.

    Args:
        expense_id (int): The unique integer ID of the expense to delete.

    Returns:
        Dict[str, str]: A dictionary with a success message.
    """
    expenses = load_expenses()

    target_idx = -1
    for idx, exp in enumerate(expenses):
        if isinstance(exp, dict) and exp.get("id") == expense_id:
            target_idx = idx
            break

    if target_idx == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )

    expenses.pop(target_idx)
    save_expenses(expenses)

    return {"message": "Expense deleted successfully"}




