from app.core.db import create_db
from fastapi import (
    FastAPI,
)
from app.api.v1.api import api_router as api_router_v1
from app.core.config import settings
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
import logging
import sys

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout)])

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("startup fastapi")
    create_db()
    yield
    # shutdown
    print("shutdown fastapi")
    


# Core Application Instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set all CORS origins enabled
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
async def root():
    """
    An example "Hello world" FastAPI route.
    """
    # if oso.is_allowed(user, "read", message):
    return {"message": "Hello World"}


# Add Routers
app.include_router(api_router_v1, prefix=settings.API_V1_STR)
