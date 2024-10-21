from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


# Shared properties
class UserGroupBase(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50, examples=["Supper Admin"])]
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Properties to receive via API on creation
class CreateUserGroupSchema(UserGroupBase):
    pass


# Properties to receive via API on update
class UpdateUserGroupSchema(UserGroupBase):
    name: Annotated[
        str, Field(min_length=3, max_length=50, examples=["Supper Admin"], default=None)
    ]


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
