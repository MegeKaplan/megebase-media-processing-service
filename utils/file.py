IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]
VIDEO_EXTENSIONS = ["mp4", "mov", "mkv", "webm"]


def get_file_extension(filename):
    arr = filename.lower().split(".")
    return arr[-1] if len(arr) > 1 else ""


def remove_file_extension(filename):
    arr = filename.split(".")
    return arr[0] if len(arr) > 1 else filename


def is_image(filename):
    return get_file_extension(filename) in IMAGE_EXTENSIONS


def is_video(filename):
    return get_file_extension(filename) in VIDEO_EXTENSIONS
