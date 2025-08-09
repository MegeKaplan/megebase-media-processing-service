import os
from utils.file import is_image, is_video
from services.image_processor import process_image_async
from services.video_processor import process_video_async


async def process_file_async(filename, media_id, raw_file_path="/tmp/raw", processed_file_path="/tmp/processed", processing_config=None):
    os.makedirs(processed_file_path, exist_ok=True)

    if is_image(filename):
        return await process_image_async(
            filename,
            media_id,
            raw_file_path=raw_file_path,
            processed_file_path=processed_file_path,
            processing_config=processing_config,
        )

    elif is_video(filename):
        return await process_video_async(
            filename,
            media_id,
            raw_file_path=raw_file_path,
            processed_file_path=processed_file_path,
        )
