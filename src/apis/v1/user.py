from typing import Annotated, Any, Union
from fastapi import APIRouter, Depends, HTTPException, Header, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import get_password_hash
from crud.user import crud_user as crud
from core import message
from core.helpers.utils import parse_query_str
from fastapi.responses import JSONResponse
from schemas.user import (
    UserRead,
    UserCreate,
    UserCreateInternal,
    UserUpdate,
)
from apis.deps import async_get_db
from core.paginated import (
    paginated_response,
    compute_offset,
    PaginatedListResponse,
    SingleResponse,
)
from models.group import Group
from schemas.group import GroupRelationship

# from core.helpers.cache import cache

router = APIRouter()


@router.get(
    "",
    response_model=PaginatedListResponse[UserRead],
    status_code=status.HTTP_200_OK,
)
# @cache(
#    key_prefix="users:results:items_per_page_{items_per_page}:page_{page}",
#    expiration=3600,
#    resource_id_name="page",
# )
async def gets(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 100,
) -> Any:
    users_data = await crud.get_multi_joined(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=UserRead,
        join_model=Group,  # pyright: ignore
        join_prefix="group_",
        join_schema_to_select=GroupRelationship,
        is_deleted=False,
        nest_joins=True,
    )

    response: dict[str, Any] = paginated_response(
        crud_data=users_data, page=page, items_per_page=items_per_page
    )

    return response


@router.get(
    "/{id}", response_model=SingleResponse[UserRead], status_code=status.HTTP_200_OK
)
# @cache(key_prefix="users:result", expiration=3600, resource_id_type=int)
async def get(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    id: int,
) -> Any:
    result = await crud.get_joined(
        db=db,
        schema_to_select=UserRead,
        id=id,
        is_deleted=False,
        join_model=Group,  # pyright: ignore
        join_prefix="group_",
        join_schema_to_select=GroupRelationship,
        nest_joins=True,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND
        )

    return {"data": result}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    user: UserCreate,
) -> Response:
    has_email = await crud.exists(db=db, email=user.email)
    if has_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=message.ITEM_ALREADY_EXISTS
        )

    has_username = await crud.exists(db=db, username=user.username)
    if has_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=message.ITEM_ALREADY_EXISTS
        )

    user_internal_dict = user.model_dump()
    user_internal_dict["hashed_password"] = get_password_hash(
        password=user_internal_dict["password"]
    )
    del user_internal_dict["password"]

    user_internal = UserCreateInternal(**user_internal_dict)
    await crud.create(db=db, object=user_internal)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.CREATE_SUCCEED}
    )


@router.put("/{id}", status_code=status.HTTP_200_OK)
# @cache(key_prefix="users:result", resource_id_type=int)
async def update(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    id: int,
    requestData: UserUpdate,
) -> Response:
    has_user = await crud.exists(db=db, id=id)

    if not has_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND
        )

    await crud.update(db=db, object=requestData, id=id)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.UPDATE_SUCCEED}
    )


@router.delete("/soft/{id}", status_code=status.HTTP_200_OK)
# @cache("users:result", resource_id_name="id")
async def soft_delete(
    request: Request,
    id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    request_init_data: Annotated[Union[str, None], Header()] = None,
) -> Response:
    result: Union[UserRead, Any] = await crud.get(
        db=db, schema_to_select=UserRead, id=id
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND
        )

    current_user = parse_query_str(request_init_data)
    if dict(result).get("id") == int(current_user.get("id", 0)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not enough permision"
        )

    await crud.delete(db=db, id=id)

    # TODO remove token
    # await blacklist_token(token=token, db=db)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.DELETE_SUCCEED}
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
# @cache("users:result", resource_id_type=int)
async def delete(
    request: Request,
    id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    request_init_data: Annotated[Union[str, None], Header()] = None,
) -> Response:
    result: Union[UserRead, Any] = await crud.get(
        db=db, schema_to_select=UserRead, id=id
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND
        )

    current_user = parse_query_str(request_init_data)
    if dict(result).get("id") == int(current_user.get("id", 0)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not enough permision"
        )

    await crud.db_delete(db=db, id=id)

    # TODO remove token
    # await blacklist_token(token=token, db=db)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.DELETE_SUCCEED}
    )
