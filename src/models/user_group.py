from sqlalchemy import Boolean, Column, Integer, String
from services.db.base_class import Base


class UserGroupModel(Base):
    __tablename__ = 'user_groups'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    is_active = Column(Boolean(), default=True)
