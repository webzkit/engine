from typing import Annotated, Any, Union
from fastapi import APIRouter, Depends, HTTPException, Header, Response, status
from sqlalchemy.ext.asyncio import AsyncSession, result

from crud.user import crud_user as crud
from config import settings
from core.smtp import mail
from core import message
from fastapi.responses import JSONResponse
from core.paginated import PaginatedListResponse, compute_offset, paginated_response
from schemas.user import UserRead
from routes.deps import async_get_db
from core.paginated import paginated_response, compute_offset, PaginatedListResponse

router = APIRouter()


@router.get(
    "",
    response_model=PaginatedListResponse[UserRead],
    status_code=status.HTTP_200_OK,
)
async def gets(
    db:Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 100,
) -> Any:
    users_data = await crud.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=UserRead,
        is_deleted=False
    )

    response: dict[str, Any] = paginated_response(crud_data=users_data, page=page, items_per_page=items_per_page)

    return response


@router.get("/{id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    id: int,
) -> Any:
    result = await crud.get(
        db=db, schema_to_select=UserRead, id=id, is_deleted=False
    )

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND)

    return result


"""
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
"""
