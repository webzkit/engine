from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

from db.base_class import Base


class TokenModel(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String(50), nullable=True)
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    expires = Column(DateTime, default=datetime.datetime.now())
    last_active = Column(DateTime, default=datetime.datetime.now())
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)

    user = relationship("UserModel", backref="tokens", uselist=False)
