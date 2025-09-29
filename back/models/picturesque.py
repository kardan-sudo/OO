from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, Enum
from database import Base
from sqlalchemy.sql import func
import enum


class SpotType(enum.Enum):
    PARK = "park"
    ESTATE = "estate"
    CASTLE = "castle"
    MONUMENT = "monument"
    NATURAL = "natural"
    HISTORICAL = "historical"
    ARCHITECTURAL = "architectural"
    RELIGIOUS = "religious"

class ScenicSpot(Base):
    __tablename__ = "scenic_spots"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Обязательные поля
    title = Column(String(200), nullable=False, index=True)
    spot_type = Column(Enum(SpotType), nullable=False, index=True)
    address = Column(String(300), nullable=False, index=True)
    
    # Координаты для карты и геопоиска - ОБЯЗАТЕЛЬНО
    latitude = Column(Float, nullable=False)  # Широта
    longitude = Column(Float, nullable=False)  # Долгота
    
    # Описание и детали - важно для пользователей
    description = Column(Text)
    short_description = Column(String(500))  # Для превью в списках
    history = Column(Text)  # Историческая справка
    
    # Практическая информация для посетителей
    opening_hours = Column(String(100))  # "9:00-18:00" или "круглосуточно"
    entrance_fee = Column(String(100))  # "бесплатно" или "200-500 руб"
    website = Column(String(200))
    phone = Column(String(20))
    
    # Системные поля
    is_verified = Column(Boolean, default=False)  # Подтверждено модератором
