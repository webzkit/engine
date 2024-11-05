from sqlalchemy.ext.asyncio import AsyncSession
from db.database import local_session

async def async_get_db() -> AsyncSession: # pyright: ignore
    try:
        async_session = local_session
        async with async_session() as db:
            db = local_session()
            yield db
    finally:
        db.close()  # type: ignore
