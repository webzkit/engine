import qrcode
from PIL import Image
from ..helpers.uniqueFileName import generate_unique_name
from config import settings


def qr_code_image(text=str, with_logo=bool):
    print(with_logo)
    qr_image_pil = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        border=2,
    )

    qr_image_pil.add_data(text)
    qr_image_pil.make()

    qr_image = qr_image_pil.make_image().convert('RGB')
    if with_logo:
        logo = Image.open(settings.QR_IMAGE_LOGO_PATH)
        qr_image.paste(logo, ((qr_image.size[0] - logo.size[0]) // 2, (qr_image.size[1] - logo.size[1]) // 2))

    qr_unique_name = generate_unique_name('png')[0]
    qr_image.save(settings.QR_IMAGE_LOCAL_PATH + qr_unique_name)

    return {
        'qr_image': qr_unique_name
    }
