from typing import Any, Optional
from fastapi import APIRouter, Depends, Query, File, UploadFile

from models import UserModel
from routes import deps
from config import settings
from services.filemanagers.uploadFile import handle_upload
from services.filemanagers.qrcode import handle_qr_code

router = APIRouter()


@router.post("/image")
async def image(
    thumbnail: Optional[str] = Query(
        settings.IMAGE_THUMBNAIL,
        description='True/False depending your needs',
        regex='^(True|False)$'
    ),
    file: UploadFile = File(...),
    current_user: UserModel = Depends(deps.get_current_active_superuser)
) -> Any:

    return handle_upload(True if thumbnail == 'True' else False, file)


@router.post("/qr-image", tags=["image"])
async def text_to_generate_qr_image(
        qr_text: str = Query(
            ...,
            description='Provide text to generate qr image',
        ),
        with_logo: Optional[str] = Query(
            settings.QR_IMAGE_WITH_LOGO,
            description='True/False depending your needs default is {}'.format(
                settings.QR_IMAGE_WITH_LOGO),
            regex='^(True|False)$'
        ),
        current_user: UserModel = Depends(deps.get_current_active_superuser)):

    return handle_qr_code(qr_text, True if with_logo == 'True' else False)
