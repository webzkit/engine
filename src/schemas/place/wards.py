from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from schemas.place.district import RelatePlaceDistrictSchema


class PlaceWardsBase(BaseModel):
    name: Optional[str] = None
    place_district_id: int
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CreatePlaceWardsSchema(PlaceWardsBase):
    name: str
    place_district_id: int


class UpdatePlaceWardsSchema(PlaceWardsBase):
    name: Optional[str] = None
    place_district_id: Optional[int] = None


class PlaceWardsInDBBase(PlaceWardsBase):
    id: Optional[int] = None
    place_district: RelatePlaceDistrictSchema

    class Config:
        orm_mode = True


class PlaceWardsSchema(PlaceWardsInDBBase):
    pass


class ResponsePlaceWards(BaseModel):
    status: bool = True
    items: Optional[List[PlaceWardsSchema]] = None
    item: Optional[PlaceWardsSchema] = None
