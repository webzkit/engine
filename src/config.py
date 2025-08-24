from enum import Enum
from os import getenv
from typing import List, Union
from pydantic import EmailStr, Field, field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

""" Project setting """


class EnviromentOption(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class AppSetting(BaseSettings):
    APP_NAME: str = Field(default="App name")
    APP_API_PREFIX: str = Field(default="/api/v1")
    APP_ENV: Union[EnviromentOption, str] = Field(default="development")

    BACKEND_CORS_ORIGINS: Union[List[AnyHttpUrl], str] = getenv(
        "BACKEND_CORS_ORIGINS", []
    )

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


class RegisterServiceSetting(BaseSettings):
    CONSUL_HOST: str = getenv("CONSUL_HOST", "consul")
    CONSUL_PORT: int = int(getenv("CONSUL_PORT", 8500))
    CONSUL_INTERVAL: str = getenv("CONSUL_INTERVAL", "10s")
    CONSUL_TIMEOUT: str = getenv("CONSUL_TIMEOUT", "5s")

    OTLP_GRPC_ENDPOINT: str = getenv("OTLP_GRPC_ENDPOINT", "tempo:4317")

    SERVICE_NAME: str = getenv("ENGINE_SERVICE_NAME", "engine")
    SERVICE_PORT: int = int(getenv("ENGINE_SERVICE_PORT", 8000))


class PostgresSetting(BaseSettings):
    POSTGRES_USER: str = getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT: int = int(getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = getenv("ENGINE__APP_DB", "engines")
    POSTGRES_SYNC_PREFIX: str = getenv("POSTGRES_SYNC_PREFIX", "postgresql://")
    POSTGRES_ASYNC_PREFIX: str = getenv(
        "POSTGRES_ASYNC_PREFIX", "postgresql+asyncpg://"
    )
    POSTGRES_URI: str = (
        f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


class RedisCacheSetting(BaseSettings):
    REDIS_CACHE_HOST: str = getenv("REDIS_HOST", "redis")
    REDIS_CACHE_PASSWORD: str = getenv("REDIS_PASSWORD", "secret")
    REDIS_CACHE_PORT: int = int(getenv("REDIS_PORT", 6379))

    REDIS_CACHE_URL: str = (
        f"redis://:{REDIS_CACHE_PASSWORD}@{REDIS_CACHE_HOST}:{REDIS_CACHE_PORT}"
    )


class FirstUserSetting(BaseSettings):
    ENABLE_EMAIL_VERIFICATION: bool = Field(default=False)
    ALLOW_REGISTRATION: bool = Field(default=False)

    # Init data user
    FIRST_SUPERUSER_EMAIL: Union[EmailStr, str] = Field(default="email@info.com")
    FIRST_SUPERUSER_USERNAME: str = Field(default="admin")
    FIRST_SUPERUSER_PASSWORD: str = Field(default="password")
    FIRST_SUPERUSER_FULLNAME: str = Field(default="Admin")


class Settings(
    AppSetting,
    PostgresSetting,
    FirstUserSetting,
    RedisCacheSetting,
    RegisterServiceSetting,
):
    model_config = SettingsConfigDict(env_prefix="ENGINE__")
    pass


settings = Settings()
