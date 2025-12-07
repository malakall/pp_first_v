from app.dao.base import BaseDAO
from app.ml.models import Heatmap


class HeatmapDAO(BaseDAO):
    model = Heatmap
