from ..base import CRUDBase

from models.places.province import ProvinceModel
from schemas.place.province import CreatePlaceProvinceSchema, UpdatePlaceProvinceSchema


class PlaceProvinceCRUD(CRUDBase[ProvinceModel, CreatePlaceProvinceSchema, UpdatePlaceProvinceSchema]):
    pass


place_province_crud = PlaceProvinceCRUD(ProvinceModel)
