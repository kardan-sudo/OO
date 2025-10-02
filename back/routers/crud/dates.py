from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from models.broadcast import MemorialDate

class MemorialDateCRUD:
    async def get_all_memorial_dates(self, db: AsyncSession) -> List[MemorialDate]:
        """Получить все памятные даты"""
        stmt = select(MemorialDate).order_by(MemorialDate.date)
        result = await db.execute(stmt)
        return list(result.scalars().all())
    
    async def get_memorial_dates_count(self, db: AsyncSession) -> int:
        """Получить общее количество памятных дат"""
        stmt = select(func.count(MemorialDate.id))
        result = await db.execute(stmt)
        return result.scalar_one()

memorial_date_crud = MemorialDateCRUD()