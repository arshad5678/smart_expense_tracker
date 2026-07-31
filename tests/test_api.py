import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.storage import save_expenses

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_storage():
    """Reset the expenses storage file to an empty list before each test."""
    save_expenses([])


def test_create_expense():
    """Test creating an expense successfully."""
    payload = {
        "title": "Lunch with client",
        "amount": 25.50,
        "category": "Food",
        "date": "2026-07-31",
    }
    response = client.post("/api/expenses", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], int)
    assert data["title"] == payload["title"]
    assert data["amount"] == payload["amount"]
    assert data["category"] == payload["category"]
    assert data["date"] == payload["date"]


def test_retrieve_all_expenses():
    """Test retrieving all expenses."""
    # First verify it is empty
    response = client.get("/api/expenses")
    assert response.status_code == 200
    assert response.json() == []

    # Create an expense
    payload = {
        "title": "Keyboard",
        "amount": 99.99,
        "category": "Office",
        "date": "2026-07-31",
    }
    create_resp = client.post("/api/expenses", json=payload)
    assert create_resp.status_code == 201
    created_expense = create_resp.json()

    # Retrieve again
    response = client.get("/api/expenses")
    assert response.status_code == 200
    expenses = response.json()
    assert isinstance(expenses, list)
    assert len(expenses) == 1
    assert expenses[0]["id"] == created_expense["id"]
    assert expenses[0]["title"] == "Keyboard"


def test_filter_by_category():
    """Test filtering expenses by category (case-insensitive)."""
    # Create Food expense
    client.post(
        "/api/expenses",
        json={
            "title": "Burgers",
            "amount": 15.00,
            "category": "Food",
            "date": "2026-07-31",
        },
    )
    # Create Travel expense
    client.post(
        "/api/expenses",
        json={
            "title": "Train ticket",
            "amount": 45.00,
            "category": "Travel",
            "date": "2026-07-31",
        },
    )

    # Retrieve only Food (exact category name)
    response = client.get("/api/expenses?category=Food")
    assert response.status_code == 200
    expenses = response.json()
    assert len(expenses) == 1
    assert expenses[0]["category"] == "Food"
    assert expenses[0]["title"] == "Burgers"

    # Retrieve only Food (case-insensitive "food")
    response_lower = client.get("/api/expenses?category=food")
    assert response_lower.status_code == 200
    expenses_lower = response_lower.json()
    assert len(expenses_lower) == 1
    assert expenses_lower[0]["title"] == "Burgers"


def test_expenses_summary():
    """Test retrieve expenses summary calculations."""
    # Create multiple expenses across categories
    client.post(
        "/api/expenses",
        json={
            "title": "Groceries",
            "amount": 50.00,
            "category": "Food",
            "date": "2026-07-30",
        },
    )
    client.post(
        "/api/expenses",
        json={
            "title": "Restaurant",
            "amount": 30.00,
            "category": "Food",
            "date": "2026-07-31",
        },
    )
    client.post(
        "/api/expenses",
        json={
            "title": "Flight ticket",
            "amount": 120.00,
            "category": "Travel",
            "date": "2026-07-31",
        },
    )

    # Retrieve summary
    response = client.get("/api/expenses/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["overall"] == 200.00
    assert data["by_category"]["Food"] == 80.00
    assert data["by_category"]["Travel"] == 120.00


def test_delete_expense():
    """Test deleting an existing expense record."""
    # Create one expense
    create_resp = client.post(
        "/api/expenses",
        json={
            "title": "Lunch",
            "amount": 12.00,
            "category": "Food",
            "date": "2026-07-31",
        },
    )
    assert create_resp.status_code == 201
    expense_id = create_resp.json()["id"]

    # Delete it
    delete_resp = client.delete(f"/api/expenses/{expense_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json() == {"message": "Expense deleted successfully"}

    # Verify list is empty
    list_resp = client.get("/api/expenses")
    assert list_resp.status_code == 200
    assert list_resp.json() == []


def test_delete_non_existing_expense():
    """Test deleting a non-existing expense returns 404."""
    response = client.delete("/api/expenses/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Expense not found"}
