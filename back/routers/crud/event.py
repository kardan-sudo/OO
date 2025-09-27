from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
import models
import schemas
from typing import List, Optional

# CRUD для мероприятий
def create_event(db: Session, event: schemas.EventCreate) -> models.Event:
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    filters: Optional[schemas.EventFilter] = None
) -> List[models.Event]:
    query = db.query(models.Event)
    
    if filters:
        if filters.event_type:
            query = query.filter(models.Event.event_type == filters.event_type)
        if filters.start_date_from:
            query = query.filter(models.Event.start_date >= filters.start_date_from)
        if filters.start_date_to:
            query = query.filter(models.Event.start_date <= filters.start_date_to)
        if filters.min_rating:
            query = query.filter(models.Event.rating >= filters.min_rating)
        if filters.organizer:
            query = query.filter(models.Event.organizer.ilike(f"%{filters.organizer}%"))
    
    query = query.order_by(models.Event.rating.desc())

    return query.offset(skip).limit(limit).all()

def get_event(db: Session, event_id: int) -> Optional[models.Event]:
    return db.query(models.Event).filter(models.Event.id == event_id).first()

# CRUD для оценок
def create_rating(db: Session, rating: schemas.RatingCreate) -> models.Rating:
    # Проверяем, существует ли мероприятие
    event = db.query(models.Event).filter(models.Event.id == rating.event_id).first()
    if not event:
        return None
    
    # Проверяем, не оценивал ли пользователь уже это мероприятие
    existing_rating = db.query(models.Rating).filter(
        and_(models.Rating.event_id == rating.event_id, 
             models.Rating.user_id == rating.user_id)
    ).first()
    
    if existing_rating:
        # Обновляем существующую оценку
        existing_rating.rating = rating.rating
        db.commit()
        db.refresh(existing_rating)
    else:
        # Создаем новую оценку
        db_rating = models.Rating(**rating.dict())
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
    
    # Обновляем рейтинг мероприятия
    update_event_rating(db, rating.event_id)
    return existing_rating if existing_rating else db_rating

def update_event_rating(db: Session, event_id: int):
    """Обновляет рейтинг мероприятия"""
    
    # Вычисляем средний рейтинг
    avg_rating = db.query(func.avg(models.Rating.rating)).filter(
        models.Rating.event_id == event_id
    ).scalar()
    
    # Обновляем рейтинг мероприятия
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event:
        if avg_rating is not None:
            event.rating = round(avg_rating, 2)
        else:
            event.rating = 0.0
        db.commit()

def get_ratings_by_event(db: Session, event_id: int) -> List[models.Rating]:
    return db.query(models.Rating).filter(models.Rating.event_id == event_id).all()

# CRUD для комментариев
def create_comment(db: Session, comment: schemas.CommentCreate) -> Optional[models.Comment]:
    # Проверяем, существует ли мероприятие
    event = db.query(models.Event).filter(models.Event.id == comment.event_id).first()
    if not event:
        return None
    
    db_comment = models.Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_by_event(db: Session, event_id: int) -> List[models.Comment]:
    return db.query(models.Comment).filter(models.Comment.event_id == event_id).all()

def delete_comment(db: Session, comment_id: int, user_id: int) -> bool:
    comment = db.query(models.Comment).filter(
        and_(models.Comment.id == comment_id, models.Comment.user_id == user_id)
    ).first()
    
    if comment:
        db.delete(comment)
        db.commit()
        return True
    return False