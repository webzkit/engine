from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.base_class import Base


class DistrictModel(Base):
    __tablename__ = 'place_districts'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    place_province_id = Column(Integer, ForeignKey(
        'place_provinces.id', ondelete="CASCADE"), nullable=False)

    is_active = Column(Boolean, default=True)

    place_province = relationship(
        "ProvinceModel", backref='place_districts', uselist=False)
