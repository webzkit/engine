from typing import Any
from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from routes import deps
from crud import user_crud as crud
from schemas import LoginForm
router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    db: Session = Depends(deps.get_db),
    request: LoginForm = Depends(),
) -> Any:

    user = crud.authenticate(
        db, email=request.email, password=request.password
    )

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect email or password")
    elif not crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    return {
        "status": True,
        "data": {
            'id': '1',
            'user_type': 'admin'
        }
    }
