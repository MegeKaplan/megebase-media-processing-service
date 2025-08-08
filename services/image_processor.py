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
    with Image.open(os.path.join(raw_file_path, filename)) as img:
        img = img.convert("RGB")
        img.save(
            os.path.join(
                processed_file_path,
                remove_file_extension(filename) + "." + image_config["format"],
            ),
            image_config["format"],
            quality=image_config["quality"],
        )


async def process_image_async(
    filename, raw_file_path="/tmp/raw", processed_file_path="/tmp/processed"
):
    await asyncio.to_thread(
        process_image,
        filename,
        raw_file_path=raw_file_path,
        processed_file_path=processed_file_path,
    )
