from ..base import CRUDBase

from models.places.wards import WardsModel
from schemas.place.wards import CreatePlaceWardsSchema, UpdatePlaceWardsSchema


class PlaceWardsCRUD(CRUDBase[WardsModel, CreatePlaceWardsSchema, UpdatePlaceWardsSchema]):
    pass


place_wards_crud = PlaceWardsCRUD(WardsModel)
