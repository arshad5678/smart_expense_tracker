# AI Usage Notes

This document describes how AI assistance was utilized during the development of the Smart Expense Tracker API, what work was completed manually, and how generated suggestions were reviewed, adjusted, or discarded.

## 1. AI-Assisted Work

AI assistance was leveraged to accelerate drafting, design pattern selection, and documentation generation. Specifically, AI helped with:
- **FastAPI Project Structure**: Setting up the standard modular framework (`main.py`, `routes.py`, `models.py`, `storage.py`).
- **Pydantic Model Generation**: Initial drafting of `ExpenseCreate` and `Expense` validation schemas.
- **Storage Layer Suggestions**: Outlining read/write file utilities for local data persistence.
- **Endpoint Implementation Guidance**: Drafting request/response handler templates for CRUD operations.
- **Test Case Generation**: Scaffolding the 6 unit tests with `pytest` and `TestClient`.
- **README Drafting**: Constructing initial outlines for setup and API documentation tables.

All generated code was thoroughly reviewed and validated before being merged into the codebase.

## 2. Manual Work

The developer maintained ownership of the project assembly, verification, and critical debugging. Manual tasks included:
- **Project Setup & Environment Configuration**: Recreating the virtual environment locally to fix broken paths and setting up dependencies.
- **Running & Debugging**: Resolving issues where parallel FastAPI instances bound to active ports.
- **Interactive Verification**: Manual testing of each API endpoint using Swagger UI (`/docs`).
- **Import Troubleshooting**: Diagnosing and implementing correct Python type annotations and packages.
- **JSON Storage Validation**: Verifying that `expenses.json` was correctly written, reformatted, and maintained clean arrays.
- **API Response Review**: Inspecting HTTP headers, status codes, and structural compatibility of serialized outputs.
- **Test Execution**: Invoking `pytest` and verifying that all suite components executed successfully.

## 3. Changes Made to AI-Generated Code

Several key corrections were applied to AI drafts to meet quality standards:
- **Resolved Type-Annotation Collision**: Corrected a Pydantic V2 error where naming a field `date` and using `date: date` type annotation caused namespace clashes. Resolved it by utilizing `import datetime` and setting the type as `datetime.date`.
- **Typing Adjustments**: Added missing imports (`Any`, `List`, `Optional`) to prevent runtime module loader crashes.
- **Simplified Storage Path Resolution**: Anchored path tracking dynamically relative to `__file__` using `pathlib.Path` so file loading is independent of CWD execution contexts.
- **Improved Documentation & Comments**: Enhanced docstrings to explicitly state return types and potential exceptions.

## 4. AI Suggestions Not Used

During exploration, AI proposed several database, containerization, and authentication architectures, including:
- **Relational Databases** (SQLite, PostgreSQL via SQLAlchemy)
- **Authentication Mechanisms** (JWT, OAuth2 flows)
- **Containerization** (Docker configs)

These suggestions were **intentionally omitted** to strictly align with assignment instructions, which explicitly called for flat-file JSON storage and kept scope limited to a lightweight FastAPI skeleton.

## 5. Validation

End-to-end functionality was validated through:
- **FastAPI Server Tests**: Verifying successful startup and handling of queries locally.
- **Swagger UI Inspection**: Interacting with POST, GET, Summary, and DELETE requests directly through the OpenAPI playground.
- **Pytest Suite Runs**: Ensuring 6 out of 6 tests passed successfully.
- **Persistence Audits**: Directly viewing `expenses.json` to verify proper structural output, string-serialized dates, and ID incrementation.
