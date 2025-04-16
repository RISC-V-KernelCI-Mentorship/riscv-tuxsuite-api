from fastapi import APIRouter
from app.api.v1.endpoints import (
    tuxsuite, riscv_lab
)

api_router = APIRouter()
api_router.include_router(tuxsuite.router, prefix="/tuxsuite", tags=["callback"])
api_router.include_router(riscv_lab.router, prefix="/riscv-lab", tags=["tests"])
