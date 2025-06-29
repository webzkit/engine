from fastapi import APIRouter

from .v1 import user, group, me
from .v1 import authenticate


api_router = APIRouter()

api_router.include_router(
    authenticate.router, prefix="/authenticate", tags=["Authorization"]
)

api_router.include_router(user.router, prefix="/users", tags=["User"])
api_router.include_router(me.router, prefix="/me", tags=["Me"])
api_router.include_router(group.router, prefix="/groups", tags=["Group"])
