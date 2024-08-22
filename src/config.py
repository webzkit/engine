from os import getenv
from typing import Optional, Any, List, Union
from pydantic import EmailStr, PostgresDsn, field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings

''' Project setting '''


class Settings(BaseSettings):
    APP_NAME: str = getenv("APP_ENV", "App-Name")
    APP_API_PREFIX: str = getenv("APP_API_PREFIX", "/api/v1")
    APP_DOMAIN: str = getenv("APP_DOMAIN", "http://zkit.local")
    APP_ENV: str = getenv("APP_ENV", "development")
    APP_PORT: str = getenv("APP_PORT", "80")

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 15
    TOKEN_VERIFY_EXPIRE: bool = False

    BACKEND_CORS_ORIGINS: Union[List[AnyHttpUrl], str] = getenv(
        "BACKEND_CORS_ORIGINS", [])

    @ field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI")
    def db_connection(cls, v: Optional[str]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=getenv("POSTGRES_USER"),
            password=getenv("POSTGRES_PASSWORD"),
            host=getenv("SQL_HOST", ""),
            port=int(getenv("POSTGRES_PORT", "5432")),
            path=f"{getenv('POSTGRES_DB') or '/'}",
        )

    # via sent mail
    EMAILS_ENABLED: bool = False

    # Init data user
    FIRST_SUPERUSER: EmailStr | str = 'info@zkit.com'
    FIRST_SUPERUSER_PASSWORD: str = "123456"
    FIRST_SUPERUSER_FULLNAME: str = 'Zkit'
    USERS_OPEN_REGISTRATION: bool = False


settings = Settings()
