from enum import Enum
from os import getenv
from typing import List, Union
from pydantic import EmailStr, field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings

""" Project setting """


class EnviromentOption(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class AppSetting(BaseSettings):
    ENGINE_APP_NAME: str = ""
    ENGINE_APP_API_PREFIX: str = ""
    ENGINE_APP_DOMAIN: str = ""
    ENGINE_APP_ENV: Union[EnviromentOption, str] = getenv(
        "ENGINE_APP_ENV", "development"
    )
    ENGINE_APP_PORT: str = ""

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

    CONSUL_HOST: str = getenv("CONSUL_HOST", "consul")
    CONSUL_PORT: int = int(getenv("CONSUL_PORT", 8500))
    CONTAINER_NAME: str = getenv("CONTAINER_NAME", "engine")


class PostgresSetting(BaseSettings):
    POSTGRES_USER: str = getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT: int = int(getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = getenv("ENGINE_APP_DB", "postgres")
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


class ClientSideCacheSetting(BaseSettings):
    CLIENT_CACHE_MAX_AGE: int = int(getenv("CLIENT_CACHE_MAX_AGE", 60))


class FirstUserSetting(BaseSettings):
    # via sent mail
    EMAIL_ENABLED: bool = False

    # Init data user
    FIRST_SUPERUSER_EMAIL: EmailStr | str = "info@zkit.com"
    FIRST_SUPERUSER_USERNAME: str = "info"
    FIRST_SUPERUSER_PASSWORD: str = "123456"
    FIRST_SUPERUSER_FULLNAME: str = "Zkit"
    USERS_OPEN_REGISTRATION: bool = False


class Settings(
    AppSetting,
    PostgresSetting,
    FirstUserSetting,
    RedisCacheSetting,
    ClientSideCacheSetting,
):
    pass


settings = Settings()
