from .base import CRUDBase

from models.media_folder import MediaFolderModel
from schemas.media_folder import CreateMediaFolderSchema, UpdateMediaFolderSchema


class CRUDMediaFolder(CRUDBase[MediaFolderModel, CreateMediaFolderSchema, UpdateMediaFolderSchema]):
    pass


media_folder_crud = CRUDMediaFolder(MediaFolderModel)
