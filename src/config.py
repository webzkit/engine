import os
from typing import Optional, Dict, Any, List, Union
from pydantic import BaseSettings, EmailStr, PostgresDsn, validator, AnyHttpUrl


''' Project setting '''


class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_ENV", "App-Name")
    APP_API_PREFIX: str = os.getenv("APP_API_PREFIX", "/api/v1")
    APP_DOMAIN: str = os.getenv("APP_DOMAIN", "http://zkit.local")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_PORT: str = os.getenv("APP_PORT", "80")

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES", 10)
    REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv(
        "REFRESH_TOKEN_EXPIRE_MINUTES", 15)
    TOKEN_VERIFY_EXPIRE = os.getenv(
        "TOKEN_VERIFY_EXPIRE", False)

    BACKEND_CORS_ORIGINS: Union[List[AnyHttpUrl], str] = os.getenv(
        "BACKEND_CORS_ORIGINS", [])

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str = os.getenv("SQL_HOST", "")
    POSTGRES_USER: str = os.getenv("SQL_USER", "")
    POSTGRES_PASSWORD: str = os.getenv("SQL_PASSWORD", "")
    POSTGRES_DB: str = os.getenv("SQL_DB", "")
    POSTGRES_PORT: str = os.getenv("SQL_PORT", "")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER", ""),
            port=values.get("POSTGRES_PORT", ""),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # via sent mail
    EMAILS_ENABLED: bool = False

    # Init data user
    FIRST_SUPERUSER: EmailStr | str = 'info@zkit.com'
    FIRST_SUPERUSER_PASSWORD: str = "123456"
    FIRST_SUPERUSER_FULLNAME: str = 'Zkit'
    USERS_OPEN_REGISTRATION: bool = False

    # Service Image
    PREFERED_STORAGE: str = os.getenv('PREFERED_STORAGE', 'local')
    IMAGE_THUMBNAIL: Union[bool, str] = os.getenv("IMAGE_THUMBNAIL", False)
    SAVE_ORIGINAL: Union[bool, str] = os.getenv("SAVE_ORIGINAL", False)
    IMAGE_AllOWED_FILE_FORMAT: str = os.getenv(
        "IMAGE_AllOWED_FILE_FORMAT", "png,jpeg,jpg,webp")
    IMAGE_ORIGINAL_LOCAL_PATH: str = os.getenv(
        "IMAGE_ORIGINAL_LOCAL_PATH", "static/pictures/original/")
    IMAGE_THUMBNAIL_LOCAL_PATH: str = os.getenv(
        "IMAGE_THUMBNAIL_LOCAL_PATH", "static/pictures/thumbnail/")
    QR_IMAGE_LOCAL_PATH: str = os.getenv("QR_IMAGE_LOCAL_PATH", "/static/qr/")
    QR_IMAGE_LOGO_PATH: str = os.getenv(
        "QR_IMAGE_LOGO_PATH", "static/logo/logo.png")
    IMAGE_CONVERTING_PREFERED_FORMAT: str = os.getenv(
        "IMAGE_CONVERTING_PREFERED_FORMAT", "png")
    IMAGE_OPTIMIZATION_USING: str = os.getenv(
        "IMAGE_OPTIMIZATION_USING", "pillow-simd")
    THUMBNAIL_MAX_WIDTH: Union[int, str] = os.getenv(
        "IMAGE_OPTIMIZATION_USING", 320)
    QR_IMAGE_WITH_LOGO: Union[bool, str] = os.getenv(
        "QR_IMAGE_WITH_LOGO", False)


settings = Settings()
