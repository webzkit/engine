from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, sessionmaker

from config import settings


class Base(DeclarativeBase, MappedAsDataclass):
    pass


DATABASE_URI = settings.POSTGRES_URI
DATABASE_PREFIX = settings.POSTGRES_ASYNC_PREFIX
DATABASE_URL = f"{DATABASE_PREFIX}{DATABASE_URI}"

async_engine = create_async_engine(DATABASE_URL, echo=False, future=True)

local_session = sessionmaker(
    bind=async_engine, # pyright: ignore
    class_=AsyncSession,
    expire_on_commit=False
)


"""
async def async_get_db() -> AsyncSession:  # pyright: ignore
    async_session = local_session
    async with async_session() as db:  # pyright: ignore
        yield db
"""
