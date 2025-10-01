from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from database.database import Base

class WalkingRoute(Base):
    __tablename__ = "walking_routes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    distance_km = Column(Float, nullable=False)  # Протяженность в км
    duration_minutes = Column(Integer, nullable=False)  # Время в минутах
    points_of_interest_count = Column(Integer, nullable=False, default=0)  # Количество интересных мест
    difficulty = Column(String(50), default="medium")  # easy, medium, hard
    location = Column(String(200))  # Общая локация/район
