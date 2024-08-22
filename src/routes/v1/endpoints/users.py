from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from crud import user_crud as crud
from schemas import UserSchema as GetSchema
from schemas import ResponseUser as ResponseSchema
from schemas import CreateUserSchema as CreateSchema
from schemas import UpdateUserSchema as UpdateSchema
from models import UserModel
from routes import deps
from config import settings
from core.smtp import mail
from core.response import Response
from core.message import Message

router = APIRouter()


@router.get("", response_model=ResponseSchema, response_model_exclude={"item"})
def gets(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(deps.get_current_active_superuser)
) -> Any:
    # Get All

    results = crud.get_multi(db, skip=skip, limit=limit)

    return ResponseSchema(items=results)


@router.get("/{id}", response_model=ResponseSchema, response_model_exclude={"items"})
def get(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: UserModel = Depends(deps.get_current_active_superuser),
) -> Any:
    # Get by ID

    result = crud.get(db=db, id=id)

    if result is None:
        return Response.message(message=Message.ITEM_NOT_FOUND, status_code=status.HTTP_200_OK, status=False)

    return ResponseSchema(item=result)


@ router.post("", response_model=GetSchema)
def create(
    *,
    db: Session = Depends(deps.get_db),
    request: CreateSchema,
    current_user: UserModel = Depends(deps.get_current_active_superuser)
) -> Any:
    # Create
    print(request)
    result = crud.get_by_email(db, email=request.email)

    if result:
        return Response.message(
            message="The user with this username already exists in the system.",
            status=False
        )

    create_result = crud.create(db, obj_in=request)

    if create_result is None:
        return Response.message(message=Message.CREATE_FAILED, status=False)

    if settings.EMAILS_ENABLED and request.email:
        mail.sent_new_account_email(
            email_to=request.email, password=request.password)

    return Response.message(message=Message.CREATE_SUCCEED, status=True)


@router.put("/{id}", response_model=GetSchema)
def update(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    request: UpdateSchema,
    current_user: UserModel = Depends(deps.get_current_active_superuser)
) -> Any:
    # Update

    result = crud.get(db, id=id)

    if result is None:
        return Response.message(
            status=False,
            message="The user with this username does not exist in the system"
        )

    update_result = crud.update(db, db_obj=result, obj_in=request)

    if update_result is None:
        return Response.message(message=Message.UPDATE_FAILED, status=False)

    return Response.message(message=Message.UPDATE_SUCCEED, status=True)


@router.delete("/{id}")
def delete(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_superuser)
) -> Any:
    # Delete

    result = crud.get(db=db, id=id)

    if result is None:
        return Response.message(message=Message.ITEM_NOT_FOUND, status=False)

    if result.id == current_user.id:
        return Response.message(message="Not enough permissions", status=False, status_code=status.HTTP_403_FORBIDDEN)

    delete_result = crud.remove(db=db, id=id)

    if delete_result is None:
        return Response.message(message=Message.DELETE_FAILED, status=False)

    return Response.message(message=Message.DELETE_SUCCEED, status=True)
