from typing import Annotated, Any, Union
from fastapi import Body, status, APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud.user import crud_user as crud
from schemas.user import Login, UserRead as Read, UserReadLogin
from core.security import verify_password
from core.paginated.schemas import SingleResponse
from routes.deps import async_get_db


router = APIRouter()


@router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=SingleResponse[Read]
)
async def login(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    data_request: Annotated[Login, Body()],
) -> Any:
    result: Union[Read, Any] = await crud.get(
        db=db, schema_to_select=UserReadLogin, email=data_request.email
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
