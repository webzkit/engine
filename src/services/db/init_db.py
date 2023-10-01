from sqlalchemy.orm import Session
import services.crud
import schemas

from config import settings
from .base import Base
from .session import engine


def init_db(db: Session) -> None:
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

    services.crud.user_group_crud.create(db, obj_in=group_insert)


def create_init_user(db: Session) -> None:
    user = services.crud.user_crud.get_by_email(
        db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_insert = schemas.CreateUserSchema(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name=settings.FIRST_SUPERUSER_FULLNAME,
            is_superuser=True,
            user_group_id=1
        )

        services.crud.user_crud.create(db, obj_in=user_insert)
