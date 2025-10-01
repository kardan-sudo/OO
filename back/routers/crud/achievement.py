from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.achievement import Achievement
from models.user import user_achievements
from schemas.achievement import AchievementResponse
from typing import List

class AchievementCRUD:
    async def get_user_achievements(self, db: AsyncSession, user_id: int) -> List[AchievementResponse]:
        # Получаем достижения пользователя
        stmt = (
            select(Achievement)
            .join(user_achievements, Achievement.id == user_achievements.c.achievement_id)
            .where(user_achievements.c.user_id == user_id)
        )
        result = await db.execute(stmt)
        achievements = result.scalars().all()
        return [AchievementResponse.from_orm(a) for a in achievements]

achievement_crud = AchievementCRUD()
