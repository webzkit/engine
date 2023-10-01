from ..base import CRUDBase

from models.places.district import DistrictModel
from schemas.place.district import CreatePlaceDistrictSchema, UpdatePlaceDistrictSchema


class PlaceDistrictCRUD(CRUDBase[DistrictModel, CreatePlaceDistrictSchema, UpdatePlaceDistrictSchema]):
    pass


place_district_crud = PlaceDistrictCRUD(DistrictModel)
