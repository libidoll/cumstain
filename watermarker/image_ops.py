import os

import numpy
from PIL import Image, ImageChops, ImageOps, ImageSequence
from moviepy.editor import *


def create_watermark(watermark, opacity):
    # Get alpha mask
    mask = watermark.split()[3]
    # Create a new alpha mask
    new_mask = Image.new("L", watermark.size, int(opacity * 255))
    # Multiply the mask with the new mask
    new_mask = ImageChops.multiply(mask, new_mask)
    # Paste the new mask into the watermark
    watermark.putalpha(new_mask)
    return watermark


def get_coordinates(base_width, base_height, watermark_width, watermark_height, position, margin, scale):
    # Calculate the coordinates of where to place the watermark
    if position == 'Top Left':
        coordinates = (0, 0)
    elif position == 'Top':
        coordinates = (base_width / 2 - watermark_width / 2, 0)
    elif position == 'Top Right':
        coordinates = (base_width - watermark_width, 0)
    elif position == 'Middle Left':
        coordinates = (0, base_height / 2 - watermark_height / 2)
    elif position == 'Middle':
        coordinates = (base_width / 2 - watermark_width / 2, base_height / 2 - watermark_height / 2)
    elif position == 'Middle Right':
        coordinates = (base_width - watermark_width, base_height / 2 - watermark_height / 2)
    elif position == 'Bottom Left':
        coordinates = (0, base_height - watermark_height)
    elif position == 'Bottom':
        coordinates = (base_width / 2 - watermark_width / 2, base_height - watermark_height)
    elif position == 'Bottom Right':
        coordinates = (base_width - watermark_width, base_height - watermark_height)
    else:
        coordinates = (0, 0)

    # Get center of image
    base_center = (base_width / 2, base_height / 2)
    # Get coordinates of watermark
    watermark_coordinates = (coordinates[0] + watermark_width / 2, coordinates[1] + watermark_height / 2)
    # Calculate the distance x and y between the center of the image and the watermark
    distance = (base_center[0] - watermark_coordinates[0], base_center[1] - watermark_coordinates[1])
    # Multiply by margin
    distance = (distance[0] * margin, distance[1] * margin)
    # Add the distance to the coordinates
    coordinates = (int(coordinates[0] + distance[0]), int(coordinates[1] + distance[1]))

    return coordinates


def image_watermark(image, watermark, position, margin, scale):
    watermark_aspect_ratio = watermark.size[0] / watermark.size[1]
    watermark = watermark.resize((int(image.size[0] * scale), int(image.size[0] * scale / watermark_aspect_ratio)))

    coordinates = get_coordinates(image.size[0], image.size[1], watermark.size[0], watermark.size[1], position, margin,
                                  scale)

    image.paste(watermark, coordinates, mask=watermark)


def video_watermark(video, watermark, position, margin, scale):
    watermark_aspect_ratio = watermark.size[0] / watermark.size[1]
    watermark = watermark.resize((int(video.size[0] * scale), int(video.size[0] * scale / watermark_aspect_ratio)))

    coordinates = get_coordinates(video.size[0], video.size[1], watermark.size[0], watermark.size[1], position, margin,
                                  scale)

    watermark_clip = ImageClip(numpy.array(watermark)).set_duration(video.duration).set_pos(coordinates)

    return CompositeVideoClip([video, watermark_clip])


def add_watermark(file, watermark, opacity, position, margin, scale):
    # Backup the image or use the backup if it exists
    # backup_image(file)
    scale = scale / 100
    margin = margin / 100
    opacity = opacity / 100

    watermark = Image.open(watermark).convert("RGBA")

    watermark = create_watermark(watermark, opacity)

    # Check if file is an image
    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        # Open the image
        image = Image.open(file)

        # Rotate the image if it has an EXIF Orientation tag
        image = ImageOps.exif_transpose(image)

        # Overlay the watermark
        image_watermark(image, watermark, position, margin, scale)

        # Get path of image
        path = os.path.dirname(file)
        # Get filename of image
        filename = os.path.basename(file)

        image.save(f'{path}/watermarked_0305_{filename}')
    elif file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm')):
        video = VideoFileClip(file)

        output = video_watermark(video, watermark, position, margin, scale)

        # Get path of image
        path = os.path.dirname(file)
        # Get filename of image
        filename = os.path.basename(file)

        output_file = f'{path}/watermarked_0305_{filename}'

        output.write_videofile(output_file)
