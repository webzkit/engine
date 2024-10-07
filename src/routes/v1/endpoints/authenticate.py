from typing import Annotated, Any
from fastapi import Body, status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from routes import deps
from crud import user_crud as crud
from schemas import LoginForm, UserSchema
from core.security import verify_password


router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def login(
    *,
    db: Session = Depends(deps.get_db),
    request: Annotated[LoginForm, Body()],
) -> Any:

    user = crud.get_by_email(db, email=request.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not verify_password(request.password, getattr(user, "hashed_password")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is wrong."
        )

    return user


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout() -> Any:
    return {"detail": "Logout succeed"}
