import ffmpeg
from PIL import Image
from pathlib import Path
from fastapi import HTTPException, status
from ..helpers.alena import local_savings
from ..helpers.uniqueFileName import generate_unique_name
from config import settings


def resize_image(temp_stored_file: Path, extension: str, thumbnail: bool, desired_extension: str):
    if not thumbnail and not settings.SAVE_ORIGINAL == 'True':
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Save original is disabled, contact admin'
        )

    local_savings(images=True)

    if settings.IMAGE_OPTIMIZATION_USING == 'ffmpeg':
        return resize_image_pillow_ffmpeg(temp_stored_file, extension, thumbnail, desired_extension)

    return resize_image_pillow_simd(temp_stored_file, extension, thumbnail, desired_extension)


def resize_image_pillow_simd(temp_stored_file: Path, extension: str, thumbnail: bool, desired_extension: str):
    try:
        origin, thumb = generate_unique_name(extension, desired_extension)
        img = Image.open(temp_stored_file)
        if settings.SAVE_ORIGINAL == 'True':
            img.save(Path(settings.IMAGE_ORIGINAL_LOCAL_PATH + origin).absolute())
        else:
            origin = None
        if thumbnail:
            resize_width = int(settings.THUMBNAIL_MAX_WIDTH)
            width_percent = (resize_width / float(img.size[0]))
            height_size = int((float(img.size[1]) * float(width_percent)))
            img.thumbnail((resize_width, height_size), Image.BICUBIC)
            img.save(Path(settings.IMAGE_THUMBNAIL_LOCAL_PATH + thumb).absolute())
        else:
            thumb = None
        return {
            'original': origin,
            'thumbnail': thumb
        }
    except:
        raise HTTPException(status_code=503, detail="Image manipulation failed using pillow-SIMD")


def resize_image_pillow_ffmpeg(temp_stored_file: Path, extension: str, thumbnail: bool, desired_extension: str):
    try:
        origin, thumb = generate_unique_name(extension, desired_extension)
        # Save original (reduces size magically)
        if settings.SAVE_ORIGINAL == 'True':
            (
                ffmpeg.input(temp_stored_file)
                    .output(settings.IMAGE_ORIGINAL_LOCAL_PATH + origin)
                    .run(quiet=True)
            )
        else:
            origin = None
        if thumbnail:
            # Resize and Save
            (
                ffmpeg.input(temp_stored_file)
                    .filter("scale", settings.THUMBNAIL_MAX_WIDTH, "-1")
                    .output(settings.IMAGE_THUMBNAIL_LOCAL_PATH + thumb)
                    .run(quiet=True)
            )
        else:
            thumb = None
        return {
            'original': origin,
            'thumbnail': thumb
        }
    except:
        raise HTTPException(status_code=503, detail="Image manipulation failed using FFMPEG")
