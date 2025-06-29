from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from crud.user import crud_user as crud
from core import message
from schemas.user import (
    UserRead,
)
from apis.deps import async_get_db, get_current_user
from core.paginated import (
    SingleResponse,
)
from models.group import Group
from schemas.group import GroupRelationship

router = APIRouter()


@router.get(
    "",
    response_model=SingleResponse[UserRead],
    status_code=status.HTTP_200_OK,
)
async def get(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[dict, Depends(get_current_user)] = {},
) -> Any:
    user_id = int(current_user.get("id", 0))

    result = await crud.get_joined(
        db=db,
        schema_to_select=UserRead,
        id=user_id,
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
