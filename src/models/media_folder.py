from sqlalchemy import Boolean, Column, Integer, String
from services.db.base_class import Base


class MediaFolderModel(Base):
    __tablename__ = 'media_folders'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
