from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from database.database import get_db
from models.picturesque import ScenicSpot, SpotType
from schemas.picturesque import (
    ScenicSpotCreate, 
    ScenicSpotResponse, 
    ScenicSpotList,
    SpotType as SpotTypeSchema
)
from routers.crud.picturesque import scenic_spot_crud

picturesque_router = APIRouter(prefix="/scenic-spots", tags=["scenic-spots"])

@picturesque_router.get("/", response_model=ScenicSpotList)
async def read_scenic_spots(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Смещение"),
    limit: int = Query(20, ge=1, le=100, description="Лимит"),
    spot_type: Optional[SpotTypeSchema] = Query(None, description="Фильтр по типу места"),
    only_verified: bool = Query(True, description="Только проверенные места")
):
    """
    Получить список живописных мест с пагинацией и фильтрацией
    """
    spots = await scenic_spot_crud.get_scenic_spots(
        db=db,
        skip=skip,
        limit=limit,
        spot_type=spot_type.value if spot_type else None,
        only_verified=only_verified
    )
    
    total = await scenic_spot_crud.get_scenic_spots_count(
        db=db,
        spot_type=spot_type.value if spot_type else None,
        only_verified=only_verified
    )
    
    return ScenicSpotList(
        items=spots,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )

@picturesque_router.post("/", response_model=ScenicSpotResponse, status_code=status.HTTP_201_CREATED)
async def create_scenic_spot(
    spot: ScenicSpotCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Создать новое живописное место
    """
    # Можно добавить проверку на дубликаты по координатам
    existing_spot = await db.execute(
        select(ScenicSpot).where(
            ScenicSpot.latitude == spot.latitude,
            ScenicSpot.longitude == spot.longitude
        )
    )
    if existing_spot.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Место с такими координатами уже существует"
        )
    
    db_spot = await scenic_spot_crud.create_scenic_spot(db, spot.dict())
    return db_spot
