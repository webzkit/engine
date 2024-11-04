from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from crud import user_crud, user_group_crud
import schemas
from sqlalchemy_utils import database_exists, create_database

from config import settings
from .session import engine
from .database import async_engine as engine


def init_database():
    pass
    """
    if not database_exists(engine.url):
        create_database(engine.url)
        print("New Database Created")
        print(database_exists(engine.url))
    else:
        print("Database Already Exists")
    """


def init_data_database(db: AsyncSession) -> None:
    pass
    #create_init_group(db)
    #create_init_user(db)

"""
def create_init_group(db: AsyncSession) -> None:
    group = user_group_crud.get(db, id=1)
    if group:
        return

    group_insert = schemas.CreateUserGroupSchema(name="Supper Admin")

    user_group_crud.create(db, obj_in=group_insert)


def create_init_user(db: AsyncSession) -> None:
    user = user_crud.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_insert = schemas.CreateUserSchema(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name=settings.FIRST_SUPERUSER_FULLNAME,
            is_superuser=True,
            user_group_id=1,
        )

        user_crud.create(db, obj_in=user_insert)
"""
