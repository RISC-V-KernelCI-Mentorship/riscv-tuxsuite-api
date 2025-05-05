import os
from pydantic_settings import BaseSettings, SettingsConfigDict
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
    DB_URL: str
    LOGS_FILE: str
    DEBUG: bool
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"
    KCIDB_SUBMIT_URL: str
    KCIDB_TOKEN: str

    model_config = SettingsConfigDict(env_file="../../.env", case_sensitive=True)


settings = Settings()
