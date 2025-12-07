from ultralytics import YOLO
import cv2
import numpy as np
import os
from pathlib import Path

VIDEO_DIR = Path(os.getenv("VIDEO_DIR", "videos"))
OUT_DIR = Path(os.getenv("OUT_DIR", "heatmaps"))
MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "yolov8n.pt")
FRAME_STEP = int(os.getenv("FRAME_STEP", "3"))
PERSON_CLASS_ID = int(os.getenv("PERSON_CLASS_ID", "0"))
CONF_THRESH = float(os.getenv("CONF_THRESH", "0.4"))

OUT_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

model = YOLO(MODEL_PATH)


def build_heatmap_for_video(video_path: Path) -> Path | None:
    print(f"Обработка видео: {video_path}")

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"Не удалось открыть видео: {video_path}")
        return None

    ret, frame = cap.read()
    if not ret:
        print(f"Пустое или битое видео: {video_path}")
        cap.release()
        return None

    h, w = frame.shape[:2]

    heat = np.zeros((h, w), dtype=np.float32)
    background_accum = np.zeros_like(frame, dtype=np.float32)

    frame_idx = 0
    used_frames = 0

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1
        if frame_idx % FRAME_STEP != 0:
            continue

        used_frames += 1

        results = model(frame, verbose=False)[0]

        for box in results.boxes:
            cls_id = int(box.cls)
            conf = float(box.conf)

            if cls_id != PERSON_CLASS_ID or conf < CONF_THRESH:
                continue

            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)

            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(w - 1, x2)
            y2 = min(h - 1, y2)

            heat[y1:y2, x1:x2] += 1.0

        background_accum += frame.astype(np.float32)

    cap.release()

    if used_frames == 0:
        print(f"По факту не использовали ни одного кадра: {video_path}")
        return None

    background_avg = (background_accum / used_frames).astype(np.uint8)

    max_val = float(heat.max())
    if max_val < 1e-6:
        print(f"Не найдено людей (или очень мало) в видео: {video_path}")
        return None

    heat_norm = heat / max_val
    heat_img = (heat_norm * 255).astype(np.uint8)

    heat_img = cv2.GaussianBlur(heat_img, (0, 0), sigmaX=15, sigmaY=15)
    heat_color = cv2.applyColorMap(heat_img, cv2.COLORMAP_JET)

    overlay = cv2.addWeighted(background_avg, 0.5, heat_color, 0.7, 0)

    out_path = OUT_DIR / f"{video_path.stem}_heatmap.jpg"
    cv2.imwrite(str(out_path), overlay)

    print(f"Сохранено: {out_path}")
    return out_path
