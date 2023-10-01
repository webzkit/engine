import shutil
from pathlib import Path
from typing import Any
from tempfile import NamedTemporaryFile
from fastapi import HTTPException, status
import os

from config import settings
from .detectFileExtension import magic_extensions
from .resize import resize_image


def save_file_tmg(upload_file: None, raw_data_file=None, tmg=None) -> Any:
    try:
        if raw_data_file:
            with NamedTemporaryFile(delete=False, suffix=None) as tmp:
                shutil.copyfileobj(raw_data_file.raw, tmg)

        else:
            with NamedTemporaryFile(delete=False, suffix=None) as tmp:
                shutil.copyfileobj(upload_file.file, tmp)

        extension = magic_extensions(Path(tmp.name))
        final_temp_file = tmp.name + extension
        os.rename(Path(tmp.name), final_temp_file)

    except:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Impossible to manipulate the file')

    finally:
        if upload_file:
            upload_file.file.close()
        else:
            raw_data_file.close()

    return Path(final_temp_file), extension


def handle_upload(thumbnail, upload_file: None, raw_data_file=None):
    try:
        tmp_path, file_extension = save_file_tmg(upload_file, raw_data_file)

        if file_extension[1:] in settings.IMAGE_AllOWED_FILE_FORMAT.split(','):
            # save
            image_paths = resize_image(
                tmp_path, file_extension[1:],
                thumbnail,
                settings.IMAGE_CONVERTING_PREFERED_FORMAT
            )

            if settings.PREFERED_STORAGE == 'local':
                image_paths['original'] = settings.IMAGE_ORIGINAL_LOCAL_PATH \
                                         + image_paths['original'] if image_paths.get('original') else None
                image_paths['thumbnail'] = settings.IMAGE_THUMBNAIL_LOCAL_PATH + \
                                          image_paths['thumbnail'] if image_paths.get('thumbnail') else None

            image_paths['storage'] = settings.PREFERED_STORAGE
            image_paths['file_name'] = image_paths['original'].split('/')[-1]

            return image_paths
        else:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='The file format not supported')
    finally:
        # Delete the temp file
        tmp_path.unlink()

