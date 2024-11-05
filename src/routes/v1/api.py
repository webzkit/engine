from fastapi import APIRouter

#from .endpoints import user_group
from .endpoints import user

#from .endpoints import authenticate


api_router = APIRouter()

#api_router.include_router(
#   authenticate.router, prefix="/authenticate", tags=["Authorization"]
#)

api_router.include_router(user.router, prefix="/users", tags=["User"])
#api_router.include_router(user_group.router, prefix="/user-groups", tags=["User Group"])
