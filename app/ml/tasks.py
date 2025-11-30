import os
from pathlib import Path
from celery import Celery

from .heatmap import build_heatmap_for_video, VIDEO_DIR, OUT_DIR

BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")

celery = Celery("ml_worker", broker=BROKER_URL, backend=RESULT_BACKEND)


@celery.task(name="generate_heatmap")
def generate_heatmap_task(video_filename: str) -> str:
    """
    video_filename – имя файла в директории VIDEO_DIR.
    Возвращаем имя файла тепловой карты.
    """
    video_path = VIDEO_DIR / video_filename
    out_path = build_heatmap_for_video(video_path)

    if out_path is None:
        raise RuntimeError("Не удалось построить тепловую карту")

    return out_path.name
