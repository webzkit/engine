from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime

from .media_folder import RelateMediaFolderSchema

# Shared properties


class MediaFileBase(BaseModel):
    name: Optional[str] = None
    path: Optional[str] = None
    kind: Optional[str] = None
    folder_id: int
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Properties to receive via API on creation
class CreateMediaFileSchema(MediaFileBase):
    name: str
    path: str
    kind: str


# Properties to receive via API on update
class UpdateMediaFileSchema(MediaFileBase):
    name: str
    path: str
    kind: str


# Shared properties at relationship
class RelateMediaFileSchema(BaseModel):
    name: Optional[str] = None
    path: Optional[str] = None

    class Config:
        orm_mode = True


# Properties shared by models stored in DB
class MediaFileInDBBase(MediaFileBase):
    id: Optional[int] = None
    folder: RelateMediaFolderSchema

    class Config:
        orm_mode = True


# Additional properties to return via API
class MediaFileSchema(MediaFileInDBBase):
    pass


# Custom response return via API
class ResponseMediaFile(BaseModel):
    status: bool = True
    items: Optional[List[MediaFileSchema]] = None
    item: Optional[MediaFileSchema] = None
