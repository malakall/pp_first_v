import { useEffect, useState } from "react";
import { apiGet } from "../api";

interface HeatmapItem {
  id: number;
  task_id: string;
  video_filename: string;
  image_filename: string | null;
  created_at: string | null;
  image_url: string | null;
}

export const HeatmapHistoryPage = () => {
  const [items, setItems] = useState<HeatmapItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const data = (await apiGet("/ml/heatmap/history")) as HeatmapItem[];
        setItems(data);
      } catch (err: any) {
        setError(err.message || "Ошибка загрузки истории");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="card">
      <h2>Мои тепловые карты</h2>
      {items.length === 0 && <p>Пока нет данных</p>}
      <div className="grid">
        {items.map(h => (
          <div key={h.id} className="heatmap-item">
            <p><b>Видео:</b> {h.video_filename}</p>
            <p><b>Создано:</b> {h.created_at || "—"}</p>
            {h.image_url && (
              <img
                src={`http://localhost:8000${h.image_url}`}
                alt={h.video_filename}
                style={{ maxWidth: "100%" }}
              />
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
