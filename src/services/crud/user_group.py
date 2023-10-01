from .base import CRUDBase

from models.user_group import UserGroupModel
from schemas.user_group import CreateUserGroupSchema, UpdateUserGroupSchema


class CRUDUserGroup(CRUDBase[UserGroupModel, CreateUserGroupSchema, UpdateUserGroupSchema]):
    pass


user_group_crud = CRUDUserGroup(UserGroupModel)
