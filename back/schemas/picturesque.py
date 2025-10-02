from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

class SpotType(str, Enum):
    PARK = "PARK"
    ESTATE = "ESTATE"
    CASTLE = "CASTLE"
    MONUMENT = "MONUMENT"
    NATURAL = "NATURAL"
    HISTORICAL = "HISTORICAL"
    ARCHITECTURAL = "ARCHITECTURAL"
    RELIGIOUS = "RELIGIOUS"

class ScenicSpotBase(BaseModel):
    id : int
    title: str
    spot_type: SpotType
    address: str
    latitude: float
    longitude: float
    description: Optional[str] = None
    short_description: Optional[str] = None
    history: Optional[str] = None
    opening_hours: Optional[str] = None
    entrance_fee: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    photo_url: str = None  # Добавлено поле photo_url

    @validator('photo_url', pre=True, always=True)
    def compute_photo_url(cls, v, values):
        if 'id' in values:
            return f"http://10.11.121.199:8000/static/scenic/{values['id']}.jpg"
        return None

class ScenicSpotCreate(ScenicSpotBase):
    pass

class ScenicSpotUpdate(BaseModel):
    title: Optional[str] = None
    spot_type: Optional[SpotType] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    history: Optional[str] = None
    opening_hours: Optional[str] = None
    entrance_fee: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None

class ScenicSpotResponse(ScenicSpotBase):
    id: int
    is_verified: bool
    
    class Config:
        from_attributes = True

class ScenicSpotList(BaseModel):
    items: List[ScenicSpotResponse]
    total: int
    
class ScenicSpotVerifyUpdate(BaseModel):
    is_verified: bool

class ScenicSpotAdminUpdate(ScenicSpotVerifyUpdate):
    is_active: Optional[bool] = None