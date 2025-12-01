import type { FormEvent } from "react";
import { useEffect, useState } from "react";
import { apiGet, apiPostForm } from "../api";

export const UploadHeatmapPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [imageSrc, setImageSrc] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setStatus(null);
    setImageSrc(null);
    if (!file) {
      setError("Выберите видео");
      return;
    }
    const form = new FormData();
    form.append("file", file);
    try {
      const data = (await apiPostForm("/ml/heatmap/", form)) as { task_id: string };
      setTaskId(data.task_id);
      setStatus("PENDING");
    } catch (err: any) {
      setError(err.message || "Ошибка загрузки");
    }
  };

  useEffect(() => {
    if (!taskId) return;

    const interval = setInterval(async () => {
      try {
        const res = await apiGet(`/ml/heatmap/${taskId}`);

        if (res instanceof Response) {
          const blob = await res.blob();
          const url = URL.createObjectURL(blob);
          setImageSrc(url);
          setStatus("SUCCESS");
          clearInterval(interval);
        } else {
          const st = (res as any).status;
          setStatus(st);
          if (st === "FAILURE") clearInterval(interval);
        }
      } catch (err: any) {
        setError(err.message || "Ошибка проверки статуса");
        clearInterval(interval);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [taskId]);

  return (
    <div className="card">
      <h2>Загрузка видео для тепловой карты</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="video/mp4,video/avi,video/quicktime"
          onChange={e => setFile(e.target.files?.[0] || null)}
        />
        <button type="submit">Отправить</button>
      </form>
      {error && <div className="error">{error}</div>}
      {taskId && <p>Task ID: {taskId}</p>}
      {status && <p>Статус: {status}</p>}
      {imageSrc && (
        <div>
          <h3>Готовая тепловая карта:</h3>
          <img src={imageSrc} alt="heatmap" style={{ maxWidth: "100%" }} />
        </div>
      )}
    </div>
  );
};
