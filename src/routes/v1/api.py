from fastapi import APIRouter

from .endpoints import user_groups
from .endpoints import users
from .endpoints import oauth

from .endpoints.place import province
from .endpoints.place import district
from .endpoints.place import wards


api_router = APIRouter()
api_router.include_router(oauth.router, prefix="/oauth", tags=["oauth"])

api_router.include_router(
    user_groups.router,
    prefix="/user-groups",
    tags=["user-groups"]
)

api_router.include_router(users.router, prefix="/users", tags=["users"])

api_router.include_router(
    province.router,
    prefix="/place/provinces",
    tags=["place_province"]
)

api_router.include_router(
    district.router,
    prefix="/place/districts",
    tags=["place_district"]
)

api_router.include_router(
    wards.router,
    prefix="/place/wards",
    tags=["place_wards"]
)
