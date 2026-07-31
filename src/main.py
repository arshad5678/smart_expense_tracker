from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

from src.routes import router as api_router

app = FastAPI(
    title="Smart Expense Tracker API",
    version="1.0.0",
    description="REST API for managing personal expenses.",
)

# Configure CORS middleware to allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API routes router with the /api prefix
app.include_router(api_router, prefix="/api")


@app.get("/")
def read_root() -> Dict[str, str]:
    """Root endpoint to check if the API server is running.

    Returns:
        Dict[str, str]: A dictionary containing a greeting and API status.
    """
    return {"message": "Smart Expense Tracker API", "status": "running"}
