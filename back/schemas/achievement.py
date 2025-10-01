from pydantic import BaseModel
from datetime import date
from typing import Optional

class AchievementResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: date

    class Config:
        from_attributes = True
