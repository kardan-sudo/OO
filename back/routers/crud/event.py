from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, update, delete
from models.events import Event, Rating, Comment
from schemas import events
from typing import List, Optional
from sqlalchemy.orm import selectinload  # импорт в начале файла

# CRUD для мероприятий

class EventCRUD:
    async def create_event(self, db: AsyncSession, event_obj: events.EventCreate) -> Event:
        db_event = Event(**event_obj.dict())
        db.add(db_event)
        await db.commit()
        await db.refresh(db_event)
        return db_event

    async def get_events(
        self,  # Добавлен self
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[events.EventFilter] = None
    ) -> List[Event]:
        # Используем select() вместо query()
        stmt = select(Event)
        
        if filters:
            if filters.event_type:
                stmt = stmt.filter(Event.event_type == filters.event_type)
            if filters.start_date_from:
                stmt = stmt.filter(Event.start_date >= filters.start_date_from)
            if filters.start_date_to:
                stmt = stmt.filter(Event.start_date <= filters.start_date_to)
            if filters.min_rating:
                stmt = stmt.filter(Event.rating >= filters.min_rating)
            if filters.organizer:
                stmt = stmt.filter(Event.organizer.ilike(f"%{filters.organizer}%"))
        
        # Добавляем offset/limit
        stmt = stmt.offset(skip).limit(limit)
        
        # Выполняем async запрос
        result = await db.execute(stmt)
        return list(result.scalars().all())  # Возвращаем список объектов



    async def get_event(self, db: AsyncSession, event_id: int) -> Optional[Event]:
        stmt = (
            select(Event)
            .options(
                selectinload(Event.ratings),
                selectinload(Event.comments)
            )
            .filter(Event.id == event_id)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_unverified_events(
        self,  # Уже есть
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Event]:
        """Получить список непроверенных событий"""
        stmt = select(Event).where(
            Event.is_verified == False
        ).order_by(Event.id.desc()).offset(skip).limit(limit)
        
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_events_count(
        self,
        db: AsyncSession,
        filters: Optional[events.EventFilter] = None
    ) -> int:
        """Получить общее количество событий с учетом фильтров"""
        stmt = select(func.count(Event.id))
        
        if filters:
            if filters.event_type:
                stmt = stmt.filter(Event.event_type == filters.event_type)
            if filters.start_date_from:
                stmt = stmt.filter(Event.start_date >= filters.start_date_from)
            if filters.start_date_to:
                stmt = stmt.filter(Event.start_date <= filters.start_date_to)
            if filters.min_rating:
                stmt = stmt.filter(Event.rating >= filters.min_rating)
            if filters.organizer:
                stmt = stmt.filter(Event.organizer.ilike(f"%{filters.organizer}%"))
        
        result = await db.execute(stmt)
        return result.scalar_one()

    async def get_unverified_events_count(self, db: AsyncSession) -> int:  # Добавлен self
        """Получить количество непроверенных событий"""
        stmt = select(func.count(Event.id)).where(
            Event.is_verified == False
        )
        
        result = await db.execute(stmt)
        return result.scalar_one()
    
    async def update_event_verification(
        self,  # Уже есть
        db: AsyncSession, 
        event_id: int, 
        is_verified: bool
    ) -> Optional[Event]:
        """Обновить статус проверки события"""
        # Проверяем существование события
        existing_event = await self.get_event(db, event_id)
        if not existing_event:
            return None
        
        # Обновляем статус проверки
        stmt = (
            update(Event)
            .where(Event.id == event_id)
            .values(is_verified=is_verified)
        )
        await db.execute(stmt)
        await db.commit()
        
        # Возвращаем обновленный объект
        return await self.get_event(db, event_id)
    
    async def delete_event(self, db: AsyncSession, event_id: int) -> bool:  # Добавлен self
        """Удалить событие"""
        # Проверяем существование события
        existing_event = await self.get_event(db, event_id)
        if not existing_event:
            return False
        
        # Удаляем событие
        stmt = delete(Event).where(Event.id == event_id)
        await db.execute(stmt)
        await db.commit()
        
        return True
    
    # CRUD для оценок
    async def create_rating(self, db: AsyncSession, rating: events.RatingCreate) -> Optional[Rating]:  # Добавлен self
        # Проверяем, существует ли мероприятие (async)
        stmt = select(Event).filter(Event.id == rating.event_id)
        result = await db.execute(stmt)
        event_exists = result.scalar_one_or_none()
        if not event_exists:
            return None
        
        # Проверяем, не оценивал ли пользователь уже это мероприятие
        stmt = select(Rating).filter(
            and_(Rating.event_id == rating.event_id, 
                Rating.user_id == rating.user_id)
        )
        result = await db.execute(stmt)
        existing_rating = result.scalar_one_or_none()
        
        if existing_rating:
            # Обновляем существующую оценку (используем update или прямое присваивание)
            existing_rating.rating = rating.rating
            await db.commit()
            await db.refresh(existing_rating)
        else:
            # Создаем новую оценку
            db_rating = Rating(**rating.dict())
            db.add(db_rating)
            await db.commit()
            await db.refresh(db_rating)
            existing_rating = db_rating  # Для возврата
        
        # Обновляем рейтинг мероприятия
        await self.update_event_rating(db, rating.event_id)  # event_crud -> self
        return existing_rating

    async def update_event_rating(self, db: AsyncSession, event_id: int):  # Добавлен self
        """Обновляет рейтинг мероприятия"""
        
        # Вычисляем средний рейтинг (async)
        stmt = select(func.avg(Rating.rating)).filter(
            Rating.event_id == event_id
        )
        result = await db.execute(stmt)
        avg_rating = result.scalar()
        
        # Обновляем рейтинг мероприятия
        stmt = select(Event).filter(Event.id == event_id)
        result = await db.execute(stmt)
        event_obj = result.scalar_one_or_none()
        if event_obj:
            if avg_rating is not None:
                event_obj.rating = round(float(avg_rating), 2)  # float() для безопасности
            else:
                event_obj.rating = 0.0
            await db.commit()

    async def get_ratings_by_event(self, db: AsyncSession, event_id: int) -> List[Rating]:  # Добавлен self
        stmt = select(Rating).filter(Rating.event_id == event_id)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    # CRUD для комментариев
    async def create_comment(self, db: AsyncSession, comment: events.CommentCreate) -> Optional[Comment]:  # Добавлен self
        # Проверяем, существует ли мероприятие
        stmt = select(Event).filter(Event.id == comment.event_id)
        result = await db.execute(stmt)
        event_exists = result.scalar_one_or_none()
        if not event_exists:
            return None
        
        db_comment = Comment(**comment.dict())
        db.add(db_comment)
        await db.commit()
        await db.refresh(db_comment)
        return db_comment

    async def get_comments_by_event(self, db: AsyncSession, event_id: int) -> List[Comment]:  # Добавлен self
        stmt = select(Comment).filter(Comment.event_id == event_id)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def delete_comment(self, db: AsyncSession, comment_id: int, user_id: int) -> bool:  # Добавлен self
        stmt = select(Comment).filter(
            and_(Comment.id == comment_id, Comment.user_id == user_id)
        )
        result = await db.execute(stmt)
        comment = result.scalar_one_or_none()
        
        if comment:
            await db.delete(comment)
            await db.commit()
            return True
        return False

event_crud = EventCRUD()
