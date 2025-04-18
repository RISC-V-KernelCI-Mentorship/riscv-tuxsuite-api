import os
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from enum import Enum


class ModeEnum(str, Enum):
    development = "development"
    production = "production"
    testing = "testing"


class Settings(BaseSettings, extra='ignore'):
    PROJECT_NAME: str = "app"
    BACKEND_CORS_ORIGINS: list[str] | list[AnyHttpUrl]
    MODE: ModeEnum = ModeEnum.development
    DB_URL: str = "sqlite:///database.db"
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"
    BASE_URL: str = "https://9e1e-152-230-99-209.ngrok-free.app"


    class Config:
        case_sensitive = True
        env_file = os.path.expanduser("../../.env")


settings = Settings()
