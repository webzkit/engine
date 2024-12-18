from sqlalchemy.ext.asyncio import AsyncSession
from db.database import local_session


async def async_get_db() -> AsyncSession:  # pyright: ignore
    async_session = local_session
    async with async_session() as db:  # type: ignore
        # db = local_session()
        yield db  # type: ignore
