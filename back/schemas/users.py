from enum import Enum
from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    full_name: str
    email: str
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
    email: str
    date_of_birth: date
    username: str
    is_organizer: bool
    is_representative: bool
    last_login: Optional[date] = None
    consecutive_days: int

    class Config:
        from_attributes = True

class UserID(BaseModel):
    id: int
    
class RequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class RepresentationRequestBase(BaseModel):
    position: str
    organization: str

class RepresentationRequestCreate(RepresentationRequestBase):
    user_id: int

class RepresentationRequestUpdate(BaseModel):
    status: RequestStatus

class RepresentationRequestResponse(RepresentationRequestBase):
    id: int
    user_id: int
    status: RequestStatus
    
    class Config:
        from_attributes = True

class RepresentationRequestWithUserResponse(RepresentationRequestResponse):
    user_full_name: str
    user_email: Optional[str] = None  # Если есть email в модели User

class RepresentationRequestList(BaseModel):
    items: List[RepresentationRequestWithUserResponse]
    total: int