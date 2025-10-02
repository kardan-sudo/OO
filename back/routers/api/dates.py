from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database.database import get_db
from schemas.dates import MemorialDateResponse
from routers.crud.dates import memorial_date_crud

memorial_date_router = APIRouter(prefix="/dates", tags=["memorial-dates"])

@memorial_date_router.get("/all", response_model=List[MemorialDateResponse])
async def get_all_memorial_dates_simple(
    db: AsyncSession = Depends(get_db)
):
    """
    Получить все памятные даты (простой список)
    """
    memorial_dates = await memorial_date_crud.get_all_memorial_dates(db)
    return memorial_dates