# app/ml/router.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from celery.result import AsyncResult
from uuid import uuid4
from pathlib import Path
import shutil

from app.users.models import Users
from app.users.dependencies import get_current_user
from app.ml.dao import HeatmapDAO
from .tasks import celery, generate_heatmap_task
from .heatmap import VIDEO_DIR, OUT_DIR

router = APIRouter(
    prefix="/ml/heatmap",
    tags=["ml"],
)


@router.post("/", summary="Запустить построение тепловой карты")
async def create_heatmap(
    file: UploadFile = File(...),
    current_user: Users = Depends(get_current_user),  
):
    if file.content_type not in (
        "video/mp4",
        "video/avi",
        "video/quicktime",
    ):
        raise HTTPException(status_code=400, detail="Поддерживаются только mp4/avi/mov")

    VIDEO_DIR.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix or ".mp4"
    filename = f"{uuid4().hex}{ext}"
    video_path = VIDEO_DIR / filename

    with open(video_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    task = generate_heatmap_task.delay(filename)

    await HeatmapDAO.add(
        user_id=current_user.id,
        task_id=task.id,
        video_filename=filename,
        image_filename=None,
    )

    return {"task_id": task.id}


@router.get("/{task_id}", summary="Получить статус задачи / тепловую карту")
async def get_heatmap(
    task_id: str,
    current_user: Users = Depends(get_current_user),
):
    heatmap = await HeatmapDAO.find_one_or_none(task_id=task_id)
    if not heatmap or heatmap.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    result = AsyncResult(task_id, app=celery)

    if result.state in ("PENDING", "RECEIVED", "STARTED"):
        return {"status": result.state}

    if result.state == "FAILURE":
        raise HTTPException(status_code=500, detail="Ошибка при построении тепловой карты")

    if result.state == "SUCCESS":
        heatmap_filename = result.result 
        heatmap_path = OUT_DIR / heatmap_filename

        if not heatmap_path.exists():
            raise HTTPException(status_code=404, detail="Файл тепловой карты не найден")

        if not heatmap.image_filename:
            await HeatmapDAO.update(
                heatmap.id,
                image_filename=heatmap_filename,
            )

        return FileResponse(
            path=heatmap_path,
            media_type="image/jpeg",
            filename=heatmap_filename,
        )

    return {"status": result.state}
