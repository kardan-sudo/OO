from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from sqlalchemy.exc import IntegrityError
from models.user import RepresentationRequest, User
from schemas.users import RepresentationRequestCreate, RequestStatus, UserCreate, UserUpdate, UserLogin
from typing import List, Optional
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

class RepresentationRequestCRUD:
    async def create_request(
        self, 
        db: AsyncSession, 
        request_data: RepresentationRequestCreate
    ) -> RepresentationRequest:
        # Проверяем, есть ли уже активная заявка у пользователя
        existing_request = await db.execute(
            select(RepresentationRequest).where(
                RepresentationRequest.user_id == request_data.user_id,
                RepresentationRequest.status == RequestStatus.PENDING
            )
        )
        if existing_request.scalar_one_or_none():
            raise ValueError("User already has a pending request")
        
        db_request = RepresentationRequest(**request_data.dict())
        db.add(db_request)
        await db.commit()
        await db.refresh(db_request)
        return db_request
    
    async def get_pending_requests(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[RepresentationRequest]:
        stmt = (
            select(RepresentationRequest)
            .join(User)
            .where(RepresentationRequest.status == RequestStatus.PENDING)
            .order_by(RepresentationRequest.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())
    
    async def get_pending_requests_count(self, db: AsyncSession) -> int:
        stmt = select(func.count(RepresentationRequest.id)).where(
            RepresentationRequest.status == RequestStatus.PENDING
        )
        result = await db.execute(stmt)
        return result.scalar_one()
    
    async def get_request_by_id(
        self, 
        db: AsyncSession, 
        request_id: int
    ) -> Optional[RepresentationRequest]:
        stmt = (
            select(RepresentationRequest)
            .join(User)
            .where(RepresentationRequest.id == request_id)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def update_request_status(
        self, 
        db: AsyncSession, 
        request_id: int, 
        status: RequestStatus
    ) -> Optional[RepresentationRequest]:
        # Получаем заявку
        request = await self.get_request_by_id(db, request_id)
        if not request:
            return None
        
        # Обновляем статус
        stmt = (
            update(RepresentationRequest)
            .where(RepresentationRequest.id == request_id)
            .values(status=status)
        )
        await db.execute(stmt)
        
        # Если заявка подтверждена, обновляем статус пользователя
        if status == RequestStatus.APPROVED:
            user_stmt = (
                update(User)
                .where(User.id == request.user_id)
                .values(is_representative=True)
            )
            await db.execute(user_stmt)
        
        await db.commit()
        return await self.get_request_by_id(db, request_id)

representation_request_crud = RepresentationRequestCRUD()

user_crud = UserCRUD()