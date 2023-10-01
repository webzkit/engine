from sqlalchemy import ForeignKey, Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from services.db.base_class import Base


class MediaFileModel(Base):
    __tablename__ = 'media_files'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(126), nullable=False)
    path = Column(String(126), nullable=False)
    kind = Column(String(20), default="image")
    folder_id = Column(Integer, ForeignKey(
        'media_folders.id', ondelete="CASCADE"), nullable=False)
    is_active = Column(Boolean, default=True)

    folder = relationship("MediaFolderModel",
                          backref="meida_files", uselist=False)
