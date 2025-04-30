from fastapi import APIRouter
from app.api.v1.endpoints import (
    builds, tests, tuxsuite, sync
)

api_router = APIRouter()
api_router.include_router(tuxsuite.router, prefix="/tuxsuite", tags=["tuxsuite", "callback"])
api_router.include_router(tests.router, prefix="/tests", tags=["tests"])
api_router.include_router(builds.router, prefix="/builds", tags=["builds"])
api_router.include_router(sync.router, prefix="/sync", tags=["sync"])
