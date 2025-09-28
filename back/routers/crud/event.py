from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, update
from sqlalchemy.orm import selectinload  # Если нужны eager loads, опционально
from back.models import events as event
from back.schemas import events
from typing import List, Optional

# CRUD для мероприятий
async def create_event(db: AsyncSession, event_obj: events.EventCreate) -> event.Event:
    db_event = event.Event(**event_obj.dict())
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event

async def get_events(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100,
    filters: Optional[events.EventFilter] = None
) -> List[event.Event]:
    # Используем select() вместо query()
    stmt = select(event.Event)
    
    if filters:
        if filters.event_type:
            stmt = stmt.filter(event.Event.event_type == filters.event_type)
        if filters.start_date_from:
            stmt = stmt.filter(event.Event.start_date >= filters.start_date_from)
        if filters.start_date_to:
            stmt = stmt.filter(event.Event.start_date <= filters.start_date_to)
        if filters.min_rating:
            stmt = stmt.filter(event.Event.rating >= filters.min_rating)
        if filters.organizer:
            stmt = stmt.filter(event.Event.organizer.ilike(f"%{filters.organizer}%"))
    
    # Добавляем offset/limit
    stmt = stmt.offset(skip).limit(limit)
    
    # Выполняем async запрос
    result = await db.execute(stmt)
    return list(result.scalars().all())  # Возвращаем список объектов

async def get_event(db: AsyncSession, event_id: int) -> Optional[event.Event]:
    stmt = select(event.Event).filter(event.Event.id == event_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()  # Или .first() если используете scalars()

# CRUD для оценок
async def create_rating(db: AsyncSession, rating: events.RatingCreate) -> Optional[event.Rating]:
    # Проверяем, существует ли мероприятие (async)
    stmt = select(event.Event).filter(event.Event.id == rating.event_id)
    result = await db.execute(stmt)
    event_exists = result.scalar_one_or_none()
    if not event_exists:
        return None
    
    # Проверяем, не оценивал ли пользователь уже это мероприятие
    stmt = select(event.Rating).filter(
        and_(event.Rating.event_id == rating.event_id, 
             event.Rating.user_id == rating.user_id)
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
        db_rating = event.Rating(**rating.dict())
        db.add(db_rating)
        await db.commit()
        await db.refresh(db_rating)
        existing_rating = db_rating  # Для возврата
    
    # Обновляем рейтинг мероприятия
    await update_event_rating(db, rating.event_id)
    return existing_rating

async def update_event_rating(db: AsyncSession, event_id: int):
    """Обновляет рейтинг мероприятия"""
    
    # Вычисляем средний рейтинг (async)
    stmt = select(func.avg(event.Rating.rating)).filter(
        event.Rating.event_id == event_id
    )
    result = await db.execute(stmt)
    avg_rating = result.scalar()
    
    # Обновляем рейтинг мероприятия
    stmt = select(event.Event).filter(event.Event.id == event_id)
    result = await db.execute(stmt)
    event_obj = result.scalar_one_or_none()
    if event_obj:
        if avg_rating is not None:
            event_obj.rating = round(float(avg_rating), 2)  # float() для безопасности
        else:
            event_obj.rating = 0.0
        await db.commit()

async def get_ratings_by_event(db: AsyncSession, event_id: int) -> List[event.Rating]:
    stmt = select(event.Rating).filter(event.Rating.event_id == event_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())

# CRUD для комментариев
async def create_comment(db: AsyncSession, comment: events.CommentCreate) -> Optional[event.Comment]:
    # Проверяем, существует ли мероприятие
    stmt = select(event.Event).filter(event.Event.id == comment.event_id)
    result = await db.execute(stmt)
    event_exists = result.scalar_one_or_none()
    if not event_exists:
        return None
    
    db_comment = event.Comment(**comment.dict())
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

async def get_comments_by_event(db: AsyncSession, event_id: int) -> List[event.Comment]:
    stmt = select(event.Comment).filter(event.Comment.event_id == event_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def delete_comment(db: AsyncSession, comment_id: int, user_id: int) -> bool:
    stmt = select(event.Comment).filter(
        and_(event.Comment.id == comment_id, event.Comment.user_id == user_id)
    )
    result = await db.execute(stmt)
    comment = result.scalar_one_or_none()
    
    if comment:
        await db.delete(comment)
        await db.commit()
        return True
    return False
