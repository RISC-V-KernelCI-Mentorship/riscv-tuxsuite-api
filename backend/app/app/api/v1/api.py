from fastapi import APIRouter
from app.api.v1.endpoints import (
    tests, tuxsuite, sync
)

api_router = APIRouter()
api_router.include_router(tuxsuite.router, prefix="/tuxsuite", tags=["tuxsuite", "callback"])
api_router.include_router(tests.router, prefix="/tests", tags=["tests"])
api_router.include_router(sync.router, prefix="/sync", tags=["tsync"])
