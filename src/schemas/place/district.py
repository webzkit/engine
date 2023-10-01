from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from schemas.place.province import RelatePlaceProvinceSchema


class PlaceDistrictBase(BaseModel):
    name: Optional[str] = None
    place_province_id: int
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CreatePlaceDistrictSchema(PlaceDistrictBase):
    name: str
    place_province_id: int


class UpdatePlaceDistrictSchema(PlaceDistrictBase):
    name: Optional[str] = None
    place_province_id: Optional[int] = None


# relationship
class RelatePlaceDistrictSchema(BaseModel):
    name: Optional[str] = None
    place_province: RelatePlaceProvinceSchema

    class Config:
        orm_mode = True


class PlaceDistrictInDBBase(PlaceDistrictBase):
    id: Optional[int] = None
    place_province: RelatePlaceProvinceSchema

    class Config:
        orm_mode = True


class PlaceDistrictSchema(PlaceDistrictInDBBase):
    pass


class ResponsePlaceDistrict(BaseModel):
    status: bool = True
    items: Optional[List[PlaceDistrictSchema]] = None
    item: Optional[PlaceDistrictSchema] = None
