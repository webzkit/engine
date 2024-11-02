from typing import Any
from fastapi import Response, APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from crud import user_group_crud as crud
from schemas import UserGroupSchema as ResponseSchema
from schemas import CreateUserGroupSchema as CreateSchema
from schemas import UpdateUserGroupSchema as UpdateSchema
from routes import deps
from core import message

router = APIRouter()


@router.get("", response_model=list[ResponseSchema], status_code=status.HTTP_200_OK)
def gets(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    results = crud.get_multi(db, skip=skip, limit=limit)

    return results


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
    result = crud.create(db, obj_in=request)

    if not result:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=message.CREATE_FAILED)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.UPDATE_SUCCEED}
    )


@router.put("/{id}", response_model=ResponseSchema)
def update(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    request: UpdateSchema,
) -> Response:
    result = crud.get(db, id=id)

    if not result:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND
        )

    crud.update(db, db_obj=result, obj_in=request)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.UPDATE_SUCCEED}
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete(
    id: int,
    db: Session = Depends(deps.get_db),
) -> Response:
    result = crud.get(db=db, id=id)

    if not result:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.DELETE_SUCCEED}
    )
