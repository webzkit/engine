from os import getenv
from typing import Optional, Any, List, Union
from pydantic import EmailStr, PostgresDsn, field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings

''' Project setting '''


class Settings(BaseSettings):
    USER_APP_NAME: str = ""
    USER_APP_API_PREFIX: str = ""
    USER_APP_DOMAIN: str = ""
    USER_APP_ENV: str = ""
    USER_APP_PORT: str = ""

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 15
    TOKEN_VERIFY_EXPIRE: bool = False

    BACKEND_CORS_ORIGINS: Union[List[AnyHttpUrl], str] = getenv(
        "BACKEND_CORS_ORIGINS", [])

    @field_validator("BACKEND_CORS_ORIGINS")
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
            host=getenv("POSTGRES_HOST", ""),
            port=int(getenv("POSTGRES_PORT", "5432")),
            path=f"{getenv('USER_APP_DB') or '/'}",
        )

    # via sent mail
    EMAIL_ENABLED: bool = False

    # Init data user
    FIRST_SUPERUSER: EmailStr | str = 'info@zkit.com'
    FIRST_SUPERUSER_PASSWORD: str = "123456"
    FIRST_SUPERUSER_FULLNAME: str = 'Zkit'
    USERS_OPEN_REGISTRATION: bool = False


settings = Settings()
