from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from models.user import User
from schemas.users import UserCreate, UserUpdate, UserLogin
from typing import Optional
from datetime import date, timedelta

class UserCRUD:
    async def create_user(self, db: AsyncSession, user: UserCreate) -> Optional[User]:
        db_user = User(**user.dict())
        db.add(db_user)
        try:
            await db.commit()
            await db.refresh(db_user)
            return db_user
        except IntegrityError:
            await db.rollback()
            return None  # Username already exists

    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> Optional[User]:
        stmt = select(User).filter(User.id == user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        stmt = select(User).filter(User.username == username)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_user(self, db: AsyncSession, user_id: int, user_update: UserUpdate) -> Optional[User]:
        db_user = await self.get_user_by_id(db, user_id)
        if not db_user:
            return None
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def authenticate_user(self, db: AsyncSession, user_login: UserLogin) -> Optional[User]:
        user = await self.get_user_by_username(db, user_login.username)
        if not user or user.password != user_login.password:
            return None
        
        # Обновляем last_login и consecutive_days
        today = date.today()
        if user.last_login is None:
            consecutive_days = 1
        elif user.last_login == today - timedelta(days=1):
            consecutive_days = user.consecutive_days + 1
        else:
            consecutive_days = 1
        
        # Обновляем поля
        stmt = (
            update(User)
            .where(User.id == user.id)
            .values(last_login=today, consecutive_days=consecutive_days)
        )
        await db.execute(stmt)
        await db.commit()
        await db.refresh(user)
        return user

user_crud = UserCRUD()
