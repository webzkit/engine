from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime


from .user_group import RelateUserGroupSchema


# Shared properties
class UserBase(BaseModel):
    email: Annotated[EmailStr, Field(examples=["info@zkit.com"])]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Annotated[
        str | None,
        Field(min_length=3, max_length=50, examples=["Full name"], default=None),
    ]
    user_group_id: Annotated[int, Field(examples=[1])]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None

    group: RelateUserGroupSchema


# request validate
class CreateUserSchema(UserBase):
    password: Annotated[
        str,
        Field(
            pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$",
            examples=["Pa$$w0rd"],
        ),
    ]


class UpdateUserSchema(BaseModel):
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Annotated[
        str | None,
        Field(min_length=3, max_length=50, examples=["Full name"], default=None),
    ]
    user_group_id: Annotated[int, Field(examples=[1])]


class LoginForm(BaseModel):  # nopa
    email: Annotated[EmailStr, Field(examples=["info@zkit.com"])]
    password: Annotated[str, Field(examples=["123456"])]


# Response via API
class UserSchema(UserInDBBase):
    pass
