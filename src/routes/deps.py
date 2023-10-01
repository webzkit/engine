from datetime import datetime
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from services import crud
import models
import schemas
from services.core.security import (
    ALGORITHM,
    PUBLIC_KEY
)
from config import settings
from services.db.session import SessionLocal
from services import crud

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.APP_API_PREFIX}/oauth/login"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()  # type: ignore


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.UserModel:
    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": settings.TOKEN_VERIFY_EXPIRE}
        )

        token_data = schemas.TokenPayload(**payload)
    except (PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    result_token = crud.token_crud.get_by_access_token(
        db, access_token=token_data.payload["token"])  # type: ignore

    if result_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    if datetime.now() >= result_token.expires:
        crud.token_crud.remove(db=db, id=result_token.id)  # type: ignore

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expire"
        )

    user = crud.user_crud.get(db, id=result_token.user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    return user


def get_current_active_user(
    current_user: models.UserModel = Depends(get_current_user),
) -> models.UserModel:
    if not crud.user_crud.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    return current_user


def get_current_active_superuser(
    current_user: models.UserModel = Depends(get_current_user),
) -> models.UserModel:
    if not crud.user_crud.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="The user doesn't have enough privileges"
        )

    return current_user
