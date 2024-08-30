from typing import Optional, List

from pydantic import BaseModel, ConfigDict
from datetime import datetime


# Shared properties
class UserGroupBase(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Properties to receive via API on creation
class CreateUserGroupSchema(UserGroupBase):
    name: str


# Properties to receive via API on update
class UpdateUserGroupSchema(UserGroupBase):
    name: Optional[str] = None


# Shared properties at relationship
class RelateUserGroupSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None


# Properties shared by models stored in DB
class UserGroupInDBBase(UserGroupBase):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None


# Additional properties to return via API
class UserGroupSchema(UserGroupInDBBase):
    pass


# Custom response return via API
class ResponseUserGroup(BaseModel):
    status: bool = True
    items: Optional[List[UserGroupSchema]] = None
    item: Optional[UserGroupSchema] = None
