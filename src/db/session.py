from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_engine(f"{settings.SQLALCHEMY_DATABASE_URI}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
