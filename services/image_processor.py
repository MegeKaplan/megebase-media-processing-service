from PIL import Image
import os
from utils.file import remove_file_extension
import asyncio

image_config = {
    "quality": 10,
    "format": "webp",
    "width": 480,
}


def process_image(
    filename, raw_file_path="/tmp/raw", processed_file_path="/tmp/processed"
):
    mediaId = remove_file_extension(filename)
    output_file_path = os.path.join(
        processed_file_path,
        mediaId,
        f"{mediaId}_{image_config['width']}p.{image_config['format']}",
    )
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with Image.open(os.path.join(raw_file_path, filename)) as img:
        img = img.convert("RGB")

        aspect_ratio = image_config["width"] / float(img.width)
        new_height = int(float(img.height) * aspect_ratio)
        img = img.resize((image_config["width"], new_height), Image.LANCZOS)

        img.save(
            output_file_path,
            image_config["format"],
            quality=image_config["quality"],
        )
    return os.path.dirname(output_file_path), os.path.basename(output_file_path)


async def process_image_async(
    filename, raw_file_path="/tmp/raw", processed_file_path="/tmp/processed"
):
    return await asyncio.to_thread(
        process_image,
        filename,
        raw_file_path=raw_file_path,
        processed_file_path=processed_file_path,
    )
