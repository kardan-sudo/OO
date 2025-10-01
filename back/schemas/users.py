from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    full_name: str
    date_of_birth: date
    username: str
    password: str
    is_organizer: bool = False
    is_representative: bool = False

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_organizer: Optional[bool] = None
    is_representative: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    full_name: str
    date_of_birth: date
    username: str
    is_organizer: bool
    is_representative: bool
    created_at: date
    updated_at: date
    last_login: Optional[date] = None
    consecutive_days: int

    class Config:
        from_attributes = True
