from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, Field
from db.schemas import TimestampSchema, PersistentDeletion


class GroupBase(BaseModel):
    name: Annotated[str, Field(examples=["free"])]


class Group(TimestampSchema, PersistentDeletion, GroupBase):
    pass


class GroupRead(GroupBase):
    id: int
    created_at: datetime


class GroupRelationship(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None


class GroupCreate(GroupBase):
    pass


class GroupCreateInternal(GroupCreate):
    pass


class GroupUpdate(BaseModel):
    name: str | None = None


class GroupUpdateInternal(GroupUpdate):
    updated_at: datetime


class GroupDelete(BaseModel):
    pass
