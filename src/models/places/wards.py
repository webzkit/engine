from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.base_class import Base


class WardsModel(Base):
    __tablename__ = 'place_wards'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    place_district_id = Column(Integer, ForeignKey(
        "place_districts.id", ondelete="CASCADE"), nullable=False)
    is_active = Column(Boolean, default=True)

    place_district = relationship(
        "DistrictModel", backref="place_wards", uselist=False)
