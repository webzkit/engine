from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


from .user_group import RelateUserGroupSchema


# Shared properties
class UserBase(BaseModel):
    email: str
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    user_group_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None

    group: RelateUserGroupSchema


# request validate
class CreateUserSchema(UserBase):
    password: str


class UpdateUserSchema(UserBase):
    password: Optional[str] = None


class LoginForm(BaseModel):  # nopa
    email: EmailStr = "info@zkit.com"
    password: str = "123456"


# Response via API


class UserSchema(UserInDBBase):
    pass
