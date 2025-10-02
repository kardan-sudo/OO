from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update, delete
from typing import List, Optional
from models.picturesque import ScenicSpot

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
        query = select(ScenicSpot)
        
        if only_verified:
            query = query.where(ScenicSpot.is_verified == True)
            
        if spot_type:
            # Если DB ENUM lowercase, конвертируй: query = query.where(ScenicSpot.spot_type == spot_type.lower())
            query = query.where(ScenicSpot.spot_type == spot_type)
            
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_scenic_spots_count(
        self,
        db: AsyncSession,
        spot_type: Optional[str] = None,
        only_verified: bool = True
    ) -> int:
        query = select(func.count(ScenicSpot.id))
        
        if only_verified:
            query = query.where(ScenicSpot.is_verified == True)
            
        if spot_type:
            # Если DB ENUM lowercase, конвертируй: query = query.where(ScenicSpot.spot_type == spot_type.lower())
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
        skip: int = 0,  # Добавлено
        limit: int = None  # Добавлено (None для всех, если не указано)
    ) -> List[ScenicSpot]:
        """Получить список непроверенных мест с пагинацией"""
        query = select(ScenicSpot).where(
            ScenicSpot.is_verified == False  # Только непроверенные
        )
            
        query = query.order_by(ScenicSpot.id.desc())
        
        # Добавлена пагинация
        if limit is not None:
            query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_unverified_scenic_spots_count(
        self,
        db: AsyncSession,
    ) -> int:
        """Получить количество непроверенных мест"""
        query = select(func.count(ScenicSpot.id)).where(
            ScenicSpot.is_verified == False  # Только непроверенные
        )
            
        result = await db.execute(query)
        return result.scalar_one()

    async def delete_scenic_spot(self, db: AsyncSession, spot_id: int) -> bool:
        """
        Удалить живописное место по ID
        Возвращает True если удалено, False если не найдено
        """
        # Сначала проверяем существование места
        spot = await self.get_scenic_spot(db, spot_id)
        if not spot:
            return False
        
        # Выполняем удаление
        stmt = delete(ScenicSpot).where(ScenicSpot.id == spot_id)
        await db.execute(stmt)
        await db.commit()
        
        return True

scenic_spot_crud = ScenicSpotCRUD()
