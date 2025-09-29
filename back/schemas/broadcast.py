from pydantic import BaseModel
from datetime import date
from typing import Optional

class MemorialDateBase(BaseModel):
    date: date
    title: str
    description: Optional[str] = None

class MemorialDateCreate(MemorialDateBase):
    pass

class MemorialDateResponse(MemorialDateBase):
    id: int
    
    class Config:
        from_attributes = True