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
    filename,
    media_id,
    raw_file_path="/tmp/raw",
    processed_file_path="/tmp/processed",
    processing_config=image_config,
):
    config = processing_config or image_config

    output_file_path = os.path.join(
        processed_file_path,
        media_id,
        f"{remove_file_extension(filename)}.{config['formats'][0]}",
    )
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with Image.open(os.path.join(raw_file_path, filename)) as img:
        img = img.convert("RGB")

        aspect_ratio = config["width"] / float(img.width)
        new_height = int(float(img.height) * aspect_ratio)
        img = img.resize((config["width"], new_height), Image.LANCZOS)

        img.save(
            output_file_path,
            config["formats"][0],
            quality=config["quality"],
        )
    return os.path.dirname(output_file_path), os.path.basename(output_file_path)


async def process_image_async(
    filename,
    media_id,
    raw_file_path="/tmp/raw",
    processed_file_path="/tmp/processed",
    processing_config=None,
):
    return await asyncio.to_thread(
        process_image,
        filename,
        media_id,
        raw_file_path=raw_file_path,
        processed_file_path=processed_file_path,
        processing_config=processing_config,
    )
