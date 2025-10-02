from pydantic import BaseModel
from datetime import date
from typing import List

class MemorialDateResponse(BaseModel):
    id: int
    date: date
    title: str
    
    class Config:
        from_attributes = True