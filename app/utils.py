import os
import re
import subprocess

from loguru import logger
from parsel import Selector


def xpath(text: str, query: str) -> Selector:
    return Selector(text=text).xpath(query=query)


def process_video(data):
    try:
        video_link, video_id = get_video_info(data.html)

        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        file_ts = os.path.join(parent_dir, f"{video_id}.ts")
        file_mp4 = os.path.join(parent_dir, f"{video_id}.mp4")

        download_ts(video_link, file_ts)
        convert_ts_to_mp4(file_ts, file_mp4)

        return {
            "status": "success",
            "message": "Операция по скачиванию проведена успешно",
        }

    except Exception as e:
        logger.error(f"Ошибка при обработке видео: {e}")
        raise
    finally:
        if file_ts and os.path.exists(file_ts):
            os.remove(file_ts)
            logger.info("Временный .ts файл удален")


def get_video_info(data: str) -> str:
    """Парсит линку."""
    video_link_from_data = xpath(data, "//video[@class='vjs-tech']/@poster").get()
    video_link = re.sub(r"preview.webp", "index.m3u8", video_link_from_data)
    video_id = re.search(r"(?<=\.ru\/).+?(?=\/)", video_link)[0]
    return video_link, video_id


def download_ts(video_link, file_ts):
    """Скачивает видео в формате TS."""
    try:
        command = ["yt-dlp", "--hls-prefer-native", "-o", file_ts, video_link]
        subprocess.run(command, check=True)
        logger.info("Видео успешно скачано в TS формате")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Не удалось скачать видео по ссылке: {video_link}") from e


def convert_ts_to_mp4(file_ts, file_mp4):
    """Конвертирует TS в MP4."""
    try:
        convert_command = ["MP4Box", "-add", file_ts, file_mp4]
        subprocess.run(convert_command, check=True)
        logger.info("Видео успешно сконвертировано в MP4")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Не удалось конвертировать файл {file_ts} в MP4") from e
