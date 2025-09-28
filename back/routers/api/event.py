from fastapi import Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import back.models
from back.schemas import events
import back.routers.crud
from back.database.database import  engine, get_db

from fastapi import APIRouter

event_router = APIRouter()  # Определение роутера здесь


# Роуты для мероприятий
@event_router.post("/events/", response_model=events.Event, status_code=status.HTTP_201_CREATED)
def create_event(event: events.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)

@event_router.get("/events/", response_model=List[events.Event])
def read_events(
    skip: int = 0,
    limit: int = 100,
    event_type: Optional[str] = Query(None, description="Тип мероприятия"),
    start_date_from: Optional[datetime] = Query(None, description="Начало периода"),
    start_date_to: Optional[datetime] = Query(None, description="Конец периода"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Минимальный рейтинг"),
    organizer: Optional[str] = Query(None, description="Организатор"),
    db: Session = Depends(get_db)
):
    filters = events.EventFilter(
        event_type=event_type,
        start_date_from=start_date_from,
        start_date_to=start_date_to,
        min_rating=min_rating,
        organizer=organizer
    )
    events = crud.get_events(db, skip=skip, limit=limit, filters=filters)
    return events

@event_router.get("/events/{event_id}", response_model=events.EventDetail)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

# Роуты для оценок
@event_router.post("/ratings/", response_model=events.Rating, status_code=status.HTTP_201_CREATED)
def create_rating(rating: events.RatingCreate, db: Session = Depends(get_db)):
    db_rating = crud.create_rating(db=db, rating=rating)
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_rating

# @event_router.get("/events/{event_id}/ratings", response_model=List[schemas.Rating])
# def read_event_ratings(event_id: int, db: Session = Depends(get_db)):
#     ratings = crud.get_ratings_by_event(db, event_id=event_id)
#     return ratings

# Роуты для комментариев
@event_router.post("/comments/", response_model=events.Comment, status_code=status.HTTP_201_CREATED)
def create_comment(comment: events.CommentCreate, db: Session = Depends(get_db)):
    db_comment = crud.create_comment(db=db, comment=comment)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_comment

@event_router.get("/events/{event_id}/comments", response_model=List[events.Comment])
def read_event_comments(event_id: int, db: Session = Depends(get_db)):
    comments = crud.get_comments_by_event(db, event_id=event_id)
    return comments

@event_router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, user_id: int = Query(..., description="ID пользователя"), db: Session = Depends(get_db)):
    success = crud.delete_comment(db, comment_id=comment_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found or you don't have permission to delete it")
    return {"message": "Comment deleted successfully"}