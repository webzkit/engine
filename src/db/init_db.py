from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import uuid as uuid_pkg

from config import settings

from models.group import Group
from models.user import User
from core.security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_data_database(db: AsyncSession) -> None:
    await create_init_group(db)
    await create_init_user(db)


async def create_init_group(db: AsyncSession) -> None:
    try:
        name = "Supper Admin"
        query = select(Group).where(Group.name == name)
        result = await db.execute(query)
        group = result.scalar_one_or_none()
        if group is None:
            db.add(Group(name=name))
            await db.commit()
            logger.info(f"Group '{name}' created successfully.")
    except Exception as e:
        logger.error(f"Error creating group: {e}")


async def create_init_user(db: AsyncSession) -> None:
    name = settings.FIRST_SUPERUSER_FULLNAME
    username = settings.FIRST_SUPERUSER_USERNAME
    email = settings.FIRST_SUPERUSER_EMAIL
    hashed_password = get_password_hash(settings.FIRST_SUPERUSER_PASSWORD)
    is_supperuser = True
    group_id = 1
    uuid = uuid_pkg.uuid4()

    try:
        query = select(User).filter_by(email=email)
        result = await db.execute(query)

        user = result.scalar_one_or_none()
        if user is None:
            db.add(
                User(
                    name=name,
                    username=username,
                    email=email,
                    hashed_password=hashed_password,
                    is_superuser=is_supperuser,
                    group_id=group_id,
                    uuid=uuid,
                )
            )

            await db.commit()
            logger.info(f"User '{name}' created successfully.")
    except Exception as e:
        logger.error(f"Error creating user: {e}")
