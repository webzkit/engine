from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class PlaceProvinceBase(BaseModel):
    name: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CreatePlaceProvinceSchema(PlaceProvinceBase):
    name: str


class UpdatePlaceProvinceSchema(PlaceProvinceBase):
    name: Optional[str] = None


# relationship
class RelatePlaceProvinceSchema(BaseModel):
    name: Optional[str] = None

    class Config:
        orm_mode = True


class PlaceProvinceInDBBase(PlaceProvinceBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class PlaceProvinceSchema(PlaceProvinceInDBBase):
    pass


class ResponsePlaceProvince(BaseModel):
    status: bool = True
    items: Optional[List[PlaceProvinceSchema]] = None
    item: Optional[PlaceProvinceSchema] = None
