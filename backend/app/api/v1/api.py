from fastapi import APIRouter

from app.api.v1.routes.accounts import router as accounts_router
from app.api.v1.routes.activities import router as activities_router
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.dashboard import router as dashboard_router
from app.api.v1.routes.deals import router as deals_router
from app.api.v1.routes.document import router as documents_router
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.notes import router as notes_router
from app.api.v1.routes.protected import router as protected_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router)
api_router.include_router(protected_router)
api_router.include_router(accounts_router)
api_router.include_router(deals_router)
api_router.include_router(activities_router)
api_router.include_router(notes_router)
api_router.include_router(dashboard_router)
api_router.include_router(documents_router)