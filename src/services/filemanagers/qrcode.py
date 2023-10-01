import os
from fastapi import HTTPException, status

from ..helpers.alena import local_savings
from .generateQr import qr_code_image
from config import settings


def handle_qr_code(text=str, with_logo=bool):
    try:
        local_savings(qr_codes=True)

        qr_code_paths = qr_code_image(text, with_logo)

        if os.environ.get('PREFERED_STORAGE') == 'local':
            qr_code_paths['qr_image'] = settings.APP_DOMAIN + settings.APP_API_PREFIX + \
                                        settings.QR_IMAGE_LOCAL_PATH + \
                                        qr_code_paths['qr_image'] if qr_code_paths.get('qr_image') else None

        qr_code_paths['storage'] = settings.PREFERED_STORAGE

        return qr_code_paths
    except:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='The file format not supported')
