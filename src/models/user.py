from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_group_id = Column(
        Integer, ForeignKey("user_groups.id", ondelete="CASCADE"), nullable=False
    )
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    group = relationship("UserGroupModel", backref="users", uselist=False)
