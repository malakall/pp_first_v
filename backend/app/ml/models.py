from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from app.database import Base


class Heatmap(Base):
    __tablename__ = "heatmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    task_id = Column(String, unique=True, nullable=False) 
    video_filename = Column(String, nullable=False)
    image_filename = Column(String, nullable=True)         

    created_at = Column(DateTime(timezone=True), server_default=func.now())
