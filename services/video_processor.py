import asyncio
import os
import subprocess
from utils.file import remove_file_extension

# resolutions = [480, 720, 1080]
resolutions = [480]

video_config = {
    "ffmpeg": {
        # "-vf": "scale=-2:480",
        "-r": "15",
        "-g": "30",
        "-c:v": "libx264",
        "-preset": "ultrafast",
        "-crf": "30",
        # "-b:v": "1M",
        "-c:a": "aac",
        "-b:a": "128k",
        "-flags": "-global_header",
        "-hls_time": "10",
        "-hls_list_size": "0",
        "-y": None,
    },
    "thumbnail": {
        "format": "webp",
        "quality": 10,
        "seek_time": "00:00:02.000",
        "width": 480,
    },
}


def add_id_prefix(media_id, filename):
    return f"{media_id}_{filename}" if media_id else filename


def generate_ffmpeg_command(media_id, input_path, output_path, config, resolution):
    ffmpeg_cmd = ["ffmpeg", "-i", input_path]
    for key, value in config.items():
        if value is not None:
            ffmpeg_cmd.extend([key, value])
    if resolution:
        ffmpeg_cmd.extend(["-vf", f"scale=-2:{resolution}"])
    ffmpeg_cmd.extend(
        [
            "-hls_segment_filename",
            os.path.join(output_path, add_id_prefix(media_id, "segment_%03d.ts")),
        ]
    )
    ffmpeg_cmd.append(os.path.join(output_path, add_id_prefix(media_id, "index.m3u8")))
    return ffmpeg_cmd


def generate_thumbnail(media_id, input_path, output_path, config):
    thumbnail_path = os.path.join(
        output_path,
        add_id_prefix(media_id, f"thumbnail.{config['format']}"),
    )

    # ffmpeg_cmd = [
    #     "ffmpeg",
    #     "-i",
    #     input_path,
    #     "-ss",
    #     config["seek_time"],
    #     "-vframes",
    #     "1",
    #     "-q:v",
    #     str(config["quality"]),
    #     thumbnail_path,
    #     "-y",
    # ]

    ffmpeg_cmd = [
        "ffmpeg",
        "-i",
        input_path,
        "-vf",
        f"thumbnail,scale={config['width']}:-1",
        "-frames:v",
        "1",
        thumbnail_path,
        "-y",
    ]

    subprocess.run(ffmpeg_cmd, check=True)


def process_video(
    filename, raw_file_path="/tmp/raw", processed_file_path="/tmp/processed"
):
    media_id = remove_file_extension(filename)

    input_path = os.path.join(raw_file_path, filename)
    output_path = os.path.join(processed_file_path, media_id)

    os.makedirs(output_path, exist_ok=True)

    generate_thumbnail(media_id, input_path, output_path, video_config["thumbnail"])

    for res in resolutions:
        output_path = os.path.join(output_path, f"{media_id}_{res}p")
        os.makedirs(output_path, exist_ok=True)

        ffmpeg_cmd = generate_ffmpeg_command(
            media_id, input_path, output_path, video_config["ffmpeg"], res
        )
        subprocess.run(ffmpeg_cmd, check=True)

        output_path = os.path.join(processed_file_path, media_id)

    return output_path, None


async def process_video_async(
    filename, raw_file_path="/tmp/raw", processed_file_path="/tmp/processed"
):
    return await asyncio.to_thread(
        process_video,
        filename,
        raw_file_path,
        processed_file_path,
    )
