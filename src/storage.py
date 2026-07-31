"""Storage and persistence layer for the Smart Expense Tracker API.

This module handles loading and saving expenses from/to a JSON file located
in the project root directory, and utility functions for ID generation.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

# Locate the storage file at the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STORAGE_FILE = PROJECT_ROOT / "expenses.json"


def load_expenses() -> List[Dict[str, Any]]:
    """Read expenses from the expenses.json file.

    If the file does not exist, it creates the file initialized with an empty
    list `[]`. If the file is empty or contains invalid JSON, it returns an
    empty list.

    Returns:
        List[Dict[str, Any]]: A list of expense dictionaries.
    """
    if not STORAGE_FILE.exists():
        try:
            with open(STORAGE_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)
        except OSError:
            # Handle potential file writing exceptions (e.g. permission error)
            pass
        return []

    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []


def save_expenses(expenses: List[Dict[str, Any]]) -> None:
    """Save the list of expense dictionaries back to expenses.json.

    Args:
        expenses (List[Dict[str, Any]]): A list of expense dictionaries to persist.
    """
    try:
        with open(STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=4)
    except OSError:
        # Handle file-related exceptions gracefully
        pass


def get_next_id(expenses: List[Dict[str, Any]]) -> int:
    """Get the next available unique integer ID for an expense.

    If the list is empty, returns 1. Otherwise, returns the maximum ID + 1.

    Args:
        expenses (List[Dict[str, Any]]): A list of expense dictionaries.

    Returns:
        int: The next available integer ID.
    """
    if not expenses:
        return 1

    existing_ids = []
    for expense in expenses:
        if isinstance(expense, dict) and "id" in expense:
            val = expense["id"]
            if isinstance(val, (int, float)):
                existing_ids.append(int(val))
            elif isinstance(val, str) and val.isdigit():
                existing_ids.append(int(val))

    return max(existing_ids) + 1 if existing_ids else 1
