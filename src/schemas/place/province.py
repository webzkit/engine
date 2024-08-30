from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


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
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None


class PlaceProvinceInDBBase(PlaceProvinceBase):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None


class PlaceProvinceSchema(PlaceProvinceInDBBase):
    pass


class ResponsePlaceProvince(BaseModel):
    status: bool = True
    items: Optional[List[PlaceProvinceSchema]] = None
    item: Optional[PlaceProvinceSchema] = None
