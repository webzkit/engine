from sqlalchemy.orm import Session
from crud import user_crud, user_group_crud
import schemas
from sqlalchemy_utils import database_exists, create_database

from config import settings
from .session import engine


def init_database():
    if not database_exists(engine.url):
        create_database(engine.url)
        print("New Database Created")
        print(database_exists(engine.url))
    else:
        print("Database Already Exists")


def init_data_database(db: Session) -> None:
    # Tables drop all before create
    # Base.metadata.drop_all(bind=engine)

    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    create_init_group(db)
    create_init_user(db)


def create_init_group(db: Session) -> None:
    group_insert = schemas.CreateUserGroupSchema(
        name="Supper Admin"
    )

    user_group_crud.create(db, obj_in=group_insert)


def create_init_user(db: Session) -> None:
    user = user_crud.get_by_email(
        db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_insert = schemas.CreateUserSchema(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name=settings.FIRST_SUPERUSER_FULLNAME,
            is_superuser=True,
            user_group_id=1
        )

        user_crud.create(db, obj_in=user_insert)
