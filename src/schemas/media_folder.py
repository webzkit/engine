from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime


# Shared properties
class MediaFolderBase(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Properties to receive via API on creation
class CreateMediaFolderSchema(MediaFolderBase):
    name: str


# Properties to receive via API on update
class UpdateMediaFolderSchema(MediaFolderBase):
    name: str


# Shared properties at relationship
class RelateMediaFolderSchema(BaseModel):
    name: Optional[str] = None

    class Config:
        orm_mode = True


# Properties shared by models stored in DB
class MediaFolderInDBBase(MediaFolderBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class MediaFolderSchema(MediaFolderInDBBase):
    pass


# Custom response return via API
class ResponseMediaFolder(BaseModel):
    status: bool = True
    items: Optional[List[MediaFolderSchema]] = None
    item: Optional[MediaFolderSchema] = None
