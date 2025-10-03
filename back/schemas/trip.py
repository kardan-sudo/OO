from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class WalkingRouteBase(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=200, description="Название маршрута")
    description: Optional[str] = Field(None, description="Описание маршрута")
    distance_km: float = Field(..., gt=0, description="Протяженность в км")
    duration_minutes: int = Field(..., gt=0, description="Время в минутах")
    points_of_interest_count: int = Field(0, ge=0, description="Количество интересных мест")
    difficulty: str = Field("medium", description="Сложность маршрута")
    location: Optional[str] = Field(None, max_length=200, description="Локация")
    url: Optional[str] = None
    photo_url: Optional[str] = None

    
    
    @validator('difficulty')
    def validate_difficulty(cls, v):
        allowed_difficulties = ['easy', 'medium', 'hard']
        if v not in allowed_difficulties:
            raise ValueError(f'Difficulty must be one of {allowed_difficulties}')
        return v
    
    @validator('photo_url', pre=True, always=True)
    def compute_photo_url(cls, v, values):
        if 'id' in values:
            return f"http://192.168.3.116:8000/static/routes/{values['id']}.png"
        return None

class WalkingRouteCreate(WalkingRouteBase):
    pass

class WalkingRouteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    distance_km: Optional[float] = Field(None, gt=0)
    duration_minutes: Optional[int] = Field(None, gt=0)
    points_of_interest_count: Optional[int] = Field(None, ge=0)
    difficulty: Optional[str] = None
    location: Optional[str] = None

class WalkingRouteResponse(WalkingRouteBase):
    id: int

    class Config:
        from_attributes = True

class WalkingRouteListResponse(BaseModel):
    items: List[WalkingRouteResponse]
    total: int


class RouteFilter(BaseModel):
    min_distance: Optional[float] = Field(None, ge=0, description="Минимальная протяженность")
    max_distance: Optional[float] = Field(None, ge=0, description="Максимальная протяженность")
    min_duration: Optional[int] = Field(None, ge=0, description="Минимальное время")
    max_duration: Optional[int] = Field(None, ge=0, description="Максимальное время")
    min_points: Optional[int] = Field(None, ge=0, description="Минимальное количество интересных мест")
    difficulty: Optional[str] = Field(None, description="Сложность маршрута")
