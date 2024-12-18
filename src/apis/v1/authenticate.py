from typing import Annotated, Any, Union
from fastapi import Body, Header, Request, status, APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud.user import crud_user as crud
from schemas.user import Login, UserRead as Read, UserReadLogin
from core.security import verify_password
from core.paginated.schemas import SingleResponse
from apis.deps import async_get_db
from models.group import Group
from schemas.group import GroupRelationship
from core.helpers.utils import parse_query_str


router = APIRouter()


@router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=SingleResponse[Read]
)
async def login(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    data_request: Annotated[Login, Body()],
) -> Any:
    result: Union[Read, Any] = await crud.get_joined(
        db=db,
        schema_to_select=UserReadLogin,
        email=data_request.email,
        join_model=Group,  # pyright: ignore
        join_prefix="group_",
        join_schema_to_select=GroupRelationship,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not verify_password(data_request.password, dict(result)["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is wrong."
        )

    return {"data": result}


@router.post(
    "/logout", status_code=status.HTTP_200_OK, response_model=SingleResponse[Read]
)
async def logout(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    request_init_data: Annotated[Union[str, None], Header()] = None,
) -> Any:
    current_user = parse_query_str(request_init_data)
    id = int(current_user.get("id", 0))
    result = await crud.get_joined(
        db=db,
        schema_to_select=Read,
        id=id,
        is_deleted=False,
        join_model=Group,  # pyright: ignore
        join_prefix="group_",
        join_schema_to_select=GroupRelationship,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return {"data": result}
