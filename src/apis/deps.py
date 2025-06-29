from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import local_session
from core.helpers.utils import parse_query_str


async def async_get_db() -> AsyncSession:  # pyright: ignore
    async_session = local_session
    async with async_session() as db:  # type: ignore
        # db = local_session()
        yield db  # type: ignore


async def get_current_user(
    request: Request,
    # request_init_data: Annotated[Union[str, None], Header()] = None,
) -> dict:
    request_init_data = str(request.headers.get("request-init-data"))

    return parse_query_str(request_init_data)
