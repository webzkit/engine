from typing import Optional, List

from pydantic import BaseModel, EmailStr
from datetime import datetime

from .user_group import RelateUserGroupSchema


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr | str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    user_group_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: Optional[int] = None

    group: RelateUserGroupSchema

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class CreateUserSchema(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UpdateUserSchema(UserBase):
    password: Optional[str] = None


# Additional properties to return via API
class UserSchema(UserInDBBase):
    pass

# Custom response return via API


class ResponseUser(BaseModel):
    status: bool = True
    items: Optional[List[UserSchema]] = None
    item: Optional[UserSchema] = None
