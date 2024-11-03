from typing import Annotated, Any, Union
from fastapi import APIRouter, Depends, HTTPException, Header, Response, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from crud import user_crud as crud
from schemas import UserSchema as ResponseSchema
from schemas import CreateUserSchema as CreateSchema
from schemas import UpdateUserSchema as UpdateSchema
from routes import deps
from config import settings
from core.smtp import mail
from core import message
from fastapi.responses import JSONResponse
from core.helpers.utils import parse_query_str
from core.paginated import PaginatedListResponse, compute_offset, paginated_response

router = APIRouter()


@router.get(
    "",
    response_model=PaginatedListResponse[ResponseSchema],
    status_code=status.HTTP_200_OK,
)
def gets(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    results = crud.get_multi(db, skip=skip, limit=limit)
    response: dict[str, Any] = paginated_response(
        crud_data=results, page=skip, items_per_page=limit
    )

    return response


@router.get("/{id}", response_model=ResponseSchema, status_code=status.HTTP_200_OK)
def get(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    result = crud.get(db=db, id=id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND
        )

    return result


@router.post("", status_code=HTTP_201_CREATED)
def create(
    *,
    db: Session = Depends(deps.get_db),
    request: CreateSchema,
) -> Response:
    result = crud.get_by_email(db, email=request.email)

    # Check item already exists
    if result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=message.ITEM_ALREADY_EXISTS
        )

    created = crud.create(db, obj_in=request)

    if not created:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message.CREATE_FAILED
        )

    if settings.EMAIL_ENABLED and request.email:
        mail.sent_new_account_email(email_to=request.email, password=request.password)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.CREATE_SUCCEED}
    )


@router.put("/{id}", status_code=status.HTTP_200_OK)
def update(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    request: UpdateSchema,
) -> Response:
    result = crud.get(db, id=id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND
        )

    crud.update(db, db_obj=result, obj_in=request)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.UPDATE_SUCCEED}
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete(
    id: int,
    db: Session = Depends(deps.get_db),
    request_init_data: Annotated[Union[str, None], Header()] = None,
) -> Response:
    result = crud.get(db=db, id=id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND
        )

    current_user = parse_query_str(request_init_data)
    if result.id == current_user.get("id"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not enough permision"
        )

    deleted = crud.remove(db=db, id=id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message.DELETE_FAILED
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.DELETE_SUCCEED}
    )
