from datetime import timedelta
from datetime import datetime
from typing import Any, Union

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from crud import user_crud, token_crud
from routes import deps
from config import settings
from core import security
from schemas import UserSchema as ResponseSchema
from models import UserModel


router = APIRouter()


@router.get("/me", response_model=ResponseSchema, response_model_exclude={"items"})
def logged(
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    return current_user


@router.post("/login")
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    remember: Union[str, bool] = Query(
        True,
        description='True/False depending your needs',
        regex='^(True|False)$'
    )
) -> Any:
    """
        OAuth2 compatible token login, get an access token for future requests
    """

    user = user_crud.authenticate(
        db, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect email or password")
    elif not user_crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    access_token_expires = timedelta(
        minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    refresh_token_expires = timedelta(
        minutes=int(settings.REFRESH_TOKEN_EXPIRE_MINUTES))

    token_access = security.create_token(
        user.id, expire_delta=access_token_expires)

    token_refresh = security.create_token(
        user.id, expire_delta=refresh_token_expires)

    access_token = security.create_access_token(
        {"token": token_access}, expires_delta=access_token_expires)

    refresh_token = security.create_access_token(
        {"token": token_refresh}, expires_delta=refresh_token_expires)

    remember = True if (remember == 'True' or remember == True) else False

    if remember:
        token_crud.create(db, obj_in={  # type: ignore
            "client_id": "web app",
            "user_id": user.id,
            "access_token": token_access,
            "refresh_token": token_refresh,
            "expires": datetime.now() + access_token_expires,
        })

    return {
        "status": True,
        "message": "Login succeed",
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post('/logout')
def logout():
    return {
        "status": True,
        "message": 'Logout succeed'
    }
