from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession
from db.session import SessionLocal
from db.database import local_session

def get_db() -> AsyncSession:
    try:
        db = local_session()
        yield db
    finally:
        db.close()  # type: ignore
