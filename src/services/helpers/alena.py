"""
    Alena will manage directories
"""

from pathlib import Path
from config import settings


def local_savings(images=False, qr_codes=False):
    if images:
        Path(settings.IMAGE_ORIGINAL_LOCAL_PATH).mkdir(parents=True, exist_ok=True)
        Path(settings.IMAGE_THUMBNAIL_LOCAL_PATH).mkdir(parents=True, exist_ok=True)
    elif qr_codes:
        Path(settings.QR_IMAGE_LOCAL_PATH).mkdir(parents=True, exist_ok=True)
