"""
Healthcheck API endpoints.

Provides routes for application health monitoring and status verification.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/healthcheck", status_code=200)
def ping():
    """
    Handle healthcheck requests.

    Returns a simple status confirmation to verify API availability.
    """
    return {"status": "OK"}
