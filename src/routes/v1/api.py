from fastapi import APIRouter

from .endpoints import user_groups
from .endpoints import users
from .endpoints import oauth

from .endpoints import authenticate


api_router = APIRouter()
# api_router.include_router(oauth.router, prefix="/oauth", tags=["oauth"])

api_router.include_router(
    authenticate.router, prefix="/authenticate", tags=["Authorization"]
)

api_router.include_router(users.router, prefix="/users", tags=["User"])

api_router.include_router(
    user_groups.router, prefix="/user-groups", tags=["User Group"]
)
