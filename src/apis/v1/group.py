from typing import Annotated, Any, Union
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from crud.group import crud_group as crud
from core import message
from fastapi.responses import JSONResponse
from core.paginated import PaginatedListResponse, compute_offset, paginated_response
from schemas.group import (
    GroupRead as Read,
    GroupCreate as Create,
    GroupCreateInternal as CreateInernal,
    GroupUpdate as Update,
)
from apis.deps import async_get_db
from core.paginated import (
    paginated_response,
    compute_offset,
    PaginatedListResponse,
    SingleResponse,
)

router = APIRouter()


@router.get(
    "",
    response_model=PaginatedListResponse[Read],
    status_code=status.HTTP_200_OK,
)
async def gets(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 100,
) -> Any:
    users_data = await crud.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=Read,
        is_deleted=False,
    )

    response: dict[str, Any] = paginated_response(
        crud_data=users_data, page=page, items_per_page=items_per_page
    )

    return response


@router.get(
    "/{id}", response_model=SingleResponse[Read], status_code=status.HTTP_200_OK
)
async def get(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    id: int,
) -> Any:
    result = await crud.get(db=db, schema_to_select=Read, id=id, is_deleted=False)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND
        )

    return {"data": result}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    data_request: Create,
) -> Response:
    exists = await crud.exists(db=db, name=data_request.name)
    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=message.ITEM_ALREADY_EXISTS
        )

    data_internal_dict = data_request.model_dump()

    data_internal = CreateInernal(**data_internal_dict)
    await crud.create(db=db, object=data_internal)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.CREATE_SUCCEED}
    )


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    id: int,
    data_request: Update,
) -> Response:
    exists = await crud.exists(db=db, id=id)

    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND
        )

    await crud.update(db=db, object=data_request, id=id)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.UPDATE_SUCCEED}
    )


@router.delete("/soft/{id}", status_code=status.HTTP_200_OK)
async def soft_delete(
    id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> Response:
    result: Union[Read, Any] = await crud.get(db=db, schema_to_select=Read, id=id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND
        )

    await crud.delete(db=db, id=id)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.DELETE_SUCCEED}
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete(
    id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> Response:
    result: Union[Read, Any] = await crud.get(db=db, schema_to_select=Read, id=id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND
        )

    await crud.db_delete(db=db, id=id)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.DELETE_SUCCEED}
    )
