from sqlalchemy import Boolean, Column, Integer, Interval, String
from db.base_class import Base


class ProvinceModel(Base):
    __tablename__ = 'place_provinces'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
