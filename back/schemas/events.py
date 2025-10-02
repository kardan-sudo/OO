from pydantic import BaseModel, validator
from datetime import datetime
from typing import List, Optional

class EventResponse(BaseModel):
    id: int
    title: str
    event_type: str
    start_date: datetime
    end_date: datetime
    address: str
    x_coordinate: float
    y_coordinate: float
    rating: float
    organizer: str
    website: str
    phone: str
    description: Optional[str] = None
    is_verified: bool = False
    photo_url: str = None  # Добавлено поле photo_url

    @validator('photo_url', pre=True, always=True)
    def compute_photo_url(cls, v, values):
        if 'id' in values:
            return f"http://10.11.121.199:8000/static/events/{values['id']}.jpeg"
        return None
    
    class Config:
        from_attributes = True

class EventBase(BaseModel):
    title: str
    event_type: str
    start_date: datetime
    end_date: datetime
    address: str
    x_coordinate: float
    y_coordinate: float
    organizer: str
    description: Optional[str] = None
    website: str
    phone: str

    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v

class EventCreate(EventBase):
    pass

class EventCreateWithPhoto(BaseModel):
    event_data: EventCreate
    # Фото будет обрабатываться отдельно

class EventUpdate(BaseModel):
    title: Optional[str] = None
    event_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    address: Optional[str] = None
    x_coordinate: Optional[float] = None
    y_coordinate: Optional[float] = None
    organizer: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None

class EventListResponse(BaseModel):
    items: List[EventResponse]
    total: int

class VerificationUpdate(BaseModel):
    is_verified: bool

# Схемы для оценок
class RatingBase(BaseModel):
    rating: int

    @validator('rating')
    def rating_must_be_between_1_and_5(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v

class RatingCreate(RatingBase):
    event_id: int
    user_id: int

class Rating(RatingBase):
    id: int
    event_id: int
    user_id: int
    
    class Config:
        orm_mode = True

# Схемы для комментариев
class CommentBase(BaseModel):
    comment_text: str

class CommentCreate(CommentBase):
    event_id: int
    user_id: int

class Comment(CommentBase):
    id: int
    event_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Схемы для ответов с детализацией
class EventDetail(EventResponse):
    ratings: List[Rating] = []
    comments: List[Comment] = []

# Схемы для фильтрации
class EventFilter(BaseModel):
    event_type: Optional[str] = None
    start_date_from: Optional[datetime] = None
    start_date_to: Optional[datetime] = None
    min_rating: Optional[float] = None
    organizer: Optional[str] = None