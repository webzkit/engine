from fastapi import APIRouter

from .endpoints import user_groups
from .endpoints import users
from .endpoints import oauth
from .endpoints import media_folders
from .endpoints import media_files
from .endpoints import media_upload

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

api_router.include_router(
    media_folders.router,
    prefix="/media/folders",
    tags=["media_folders"]
)

api_router.include_router(
    media_files.router,
    prefix="/media/files",
    tags=["media_files"]
)

api_router.include_router(
    media_upload.router,
    prefix="/media/uploads",
    tags=["media_uploads"]
)
