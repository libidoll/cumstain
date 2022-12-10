from PIL import Image
from PIL import ImageOps

from watermarker.file_ops import backup_image


def overlay_watermark(image, watermark, corner):
    watermark = Image.open(watermark)
    # Get the size of the watermark
    watermark_width, watermark_height = watermark.size
    # Get the image dimensions

    image_width, image_height = image.size
    # Calculate the coordinates of where to place the watermark
    if corner == 'top-left':
        coordinates = (0, 0)
    elif corner == 'top-right':
        coordinates = (image_width - watermark_width, 0)
    elif corner == 'bottom-left':
        coordinates = (0, image_height - watermark_height)
    elif corner == 'bottom-right':
        coordinates = (image_width - watermark_width, image_height - watermark_height)
    else:
        raise ValueError('Invalid corner position. Should be one of: top-left, top-right, bottom-left, bottom-right')

    # Paste the watermark
    image.paste(watermark, coordinates, mask=watermark)

    return image


def add_watermark(file, watermark, corner):
    # Backup the image or use the backup if it exists
    backup_image(file)

    # Open the image
    image = Image.open(file)

    # Rotate the image if it has an EXIF Orientation tag
    image = ImageOps.exif_transpose(image)

    # Overlay the watermark
    image = overlay_watermark(image, watermark, corner)

    # Save the image
    image.save(f'{file}')
