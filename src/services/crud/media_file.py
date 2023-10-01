from .base import CRUDBase

from models.media_file import MediaFileModel
from schemas.media_file import CreateMediaFileSchema, UpdateMediaFileSchema


class CRUDMediaFile(CRUDBase[MediaFileModel, CreateMediaFileSchema, UpdateMediaFileSchema]):
    pass


media_file_crud = CRUDMediaFile(MediaFileModel)
