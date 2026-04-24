# This file contains the health check route.
# We use this to confirm that the backend is running properly.

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Health check")
def health_check() -> dict:
    return {
        "success": True,
        "message": "API is healthy",
        "data": {
            "status": "ok"
        }
    }