import logging
import asyncio
from db.init_db import init_data_database
from db.database import local_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("Creating initial data")
    async with local_session() as session:  # pyright: ignore
        await init_data_database(session)

    logger.info("Initial data created")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
