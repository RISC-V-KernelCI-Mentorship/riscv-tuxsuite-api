from fastapi import APIRouter
from app.api.v1.endpoints import (
    builds, tests, sync, tuxsuite_callbacks
)

api_router = APIRouter()
api_router.include_router(tuxsuite_callbacks.router, prefix="/tuxsuite/callback", tags=["tuxsuite callbacks"])
api_router.include_router(tests.router, prefix="/tests", tags=["tests"])
api_router.include_router(builds.router, prefix="/builds", tags=["builds"])
api_router.include_router(sync.router, prefix="/sync", tags=["sync"])
