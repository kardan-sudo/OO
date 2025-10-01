from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from typing import List, Optional
from back.models.picturesque import ScenicSpot

class ScenicSpotCRUD:
    async def get_scenic_spot(self, db: AsyncSession, spot_id: int) -> Optional[ScenicSpot]:
        result = await db.execute(select(ScenicSpot).where(ScenicSpot.id == spot_id))
        return result.scalar_one_or_none()
    
    async def get_scenic_spots(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100,
        spot_type: Optional[str] = None,
        only_verified: bool = True
    ) -> List[ScenicSpot]:
        query = select(ScenicSpot).where(ScenicSpot.is_active == True)
        
        if only_verified:
            query = query.where(ScenicSpot.is_verified == True)
            
        if spot_type:
            query = query.where(ScenicSpot.spot_type == spot_type)
            
        query = query.order_by(ScenicSpot.rating.desc()).offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_scenic_spots_count(
        self,
        db: AsyncSession,
        spot_type: Optional[str] = None,
        only_verified: bool = True
    ) -> int:
        query = select(func.count(ScenicSpot.id)).where(ScenicSpot.is_active == True)
        
        if only_verified:
            query = query.where(ScenicSpot.is_verified == True)
            
        if spot_type:
            query = query.where(ScenicSpot.spot_type == spot_type)
            
        result = await db.execute(query)
        return result.scalar_one()
    
    async def create_scenic_spot(self, db: AsyncSession, spot_data: dict) -> ScenicSpot:
        scenic_spot = ScenicSpot(**spot_data)
        db.add(scenic_spot)
        await db.commit()
        await db.refresh(scenic_spot)
        return scenic_spot
    
    async def update_scenic_spot(
        self, 
        db: AsyncSession, 
        spot_id: int, 
        update_data: dict
    ) -> Optional[ScenicSpot]:
        # Сначала проверяем существование места
        spot = await self.get_scenic_spot(db, spot_id)
        if not spot:
            return None
            
        # Обновляем поля
        stmt = (
            update(ScenicSpot)
            .where(ScenicSpot.id == spot_id)
            .values(**update_data)
        )
        await db.execute(stmt)
        await db.commit()
        
        # Возвращаем обновленный объект
        return await self.get_scenic_spot(db, spot_id)
    
    async def get_unverified_scenic_spots(
        self, 
        db: AsyncSession, 
    ) -> List[ScenicSpot]:
        """Получить список непроверенных мест"""
        query = select(ScenicSpot).where(
            ScenicSpot.is_active == True,
            ScenicSpot.is_verified == False  # Только непроверенные
        )
            
        query = query.order_by(ScenicSpot.id.desc())
        
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_unverified_scenic_spots_count(
        self,
        db: AsyncSession,
    ) -> int:
        """Получить количество непроверенных мест"""
        query = select(func.count(ScenicSpot.id)).where(
            ScenicSpot.is_active == True,
            ScenicSpot.is_verified == False  # Только непроверенные
        )
            
        result = await db.execute(query)
        return result.scalar_one()


scenic_spot_crud = ScenicSpotCRUD()