from requests import Response
from app.file_service import file_service
from fastapi import Depends, HTTPException, status, Query, APIRouter, UploadFile, File, Response, Form
from sqlalchemy.ext.asyncio import AsyncSession  # Изменено для async
from sqlalchemy import select
from typing import List, Optional
from datetime import datetime
from models.events import Event
from schemas import events as events_schemas
from routers.crud.event import event_crud
from fastapi import Response, status
from database.database import get_db

event_router = APIRouter(prefix="/events", tags=["events"])

@event_router.post("/", response_model=events_schemas.EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    title: str = Form(...),
    event_type: str = Form(...),
    start_date: datetime = Form(...),  # FastAPI автоматически парсит ISO-строку в datetime
    end_date: datetime = Form(...),
    address: str = Form(...),
    x_coordinate: float = Form(...),
    y_coordinate: float = Form(...),
    organizer: str = Form(...),
    description: Optional[str] = Form(None),
    website: str = Form(...),
    phone: str = Form(...),
    photo: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    """Создать мероприятие с возможностью загрузки фото"""
    # Создаём объект EventCreate из полей формы (Pydantic автоматически валидирует, включая валидатор end_date)
    event_data = events_schemas.EventCreate(
        title=title,
        event_type=event_type,
        start_date=start_date,
        end_date=end_date,
        address=address,
        x_coordinate=x_coordinate,
        y_coordinate=y_coordinate,
        organizer=organizer,
        description=description,
        website=website,
        phone=phone
    )
    
    # Создаем мероприятие
    db_event = await event_crud.create_event(db=db, event_obj=event_data)
    
    # Если есть фото - сохраняем его
    if photo:
        success = await file_service.save_event_photo(db_event.id, photo)
        if success:
            await event_crud.update_event_has_photo(db, db_event.id, True)
            # Обновляем объект чтобы вернуть актуальные данные
            await db.refresh(db_event)
    
    return db_event

@event_router.get("/", response_model=events_schemas.EventListResponse)
async def read_events(
    event_type: Optional[str] = Query(None, description="Тип мероприятия"),
    start_date_from: Optional[datetime] = Query(None, description="Начало периода"),
    start_date_to: Optional[datetime] = Query(None, description="Конец периода"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Минимальный рейтинг"),
    organizer: Optional[str] = Query(None, description="Организатор"),
    db: AsyncSession = Depends(get_db)
):
    filters = events_schemas.EventFilter(
        event_type=event_type,
        start_date_from=start_date_from,
        start_date_to=start_date_to,
        min_rating=min_rating,
        organizer=organizer
    )
    events = await event_crud.get_events(db, filters=filters)
    
    total = await event_crud.get_events_count(db, filters=filters)
    
    return events_schemas.EventListResponse(
        items=events,
        total=total
    )
    
@event_router.get("/unverified", response_model=events_schemas.EventListResponse)
async def get_unverified_events(
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список непроверенных событий для модерации
    """
    events = await event_crud.get_unverified_events(
        db=db
    )
    
    total = await event_crud.get_unverified_events_count(db=db)
    
    return events_schemas.EventListResponse(
        items=events,
        total=total
    )
    
@event_router.get("/top_current", response_model=List[events_schemas.EventResponse])
async def get_current_events(
    db: AsyncSession = Depends(get_db),
):
    """
    Получить мероприятия, которые проводятся в данный момент,
    отсортированные по убыванию рейтинга
    """
    current_time = datetime.now()
    
    # Строим базовый запрос
    query = select(Event).where(
        Event.start_date <= current_time,
        Event.end_date >= current_time
    )
    query = query.order_by(Event.rating.desc())
    
    result = await db.execute(query)
    events = result.scalars().all()
    
    return events

@event_router.get("/{event_id}", response_model=events_schemas.EventResponse)
async def read_event(event_id: int, db: AsyncSession = Depends(get_db)):
    """Получить мероприятие по ID"""
    db_event = await event_crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

# Обновить статус проверки события
@event_router.put("/{event_id}/verification", response_model=events_schemas.EventResponse)
async def update_event_verification(
    event_id: int,
    verification_data: events_schemas.VerificationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Обновить статус проверки события (модерация)
    """
    updated_event = await event_crud.update_event_verification(
        db=db,
        event_id=event_id,
        is_verified=verification_data.is_verified
    )
    
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    return updated_event

# Удалить событие
@event_router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Удалить событие
    """
    success = await event_crud.delete_event(db=db, event_id=event_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Роуты для оценок
@event_router.post("/ratings/", response_model=events_schemas.Rating, status_code=status.HTTP_201_CREATED)
async def create_rating(rating: events_schemas.RatingCreate, db: AsyncSession = Depends(get_db)):  # Добавлено async, изменён тип db
    db_rating = await event_crud.create_rating(db=db, rating=rating)  # Добавлено await
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_rating

# Роуты для комментариев
@event_router.post("/comments/", response_model=events_schemas.Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: events_schemas.CommentCreate, db: AsyncSession = Depends(get_db)):  # Добавлено async, изменён тип db
    db_comment = await event_crud.create_comment(db=db, comment=comment)  # Добавлено await
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_comment

@event_router.get("/{event_id}/comments", response_model=List[events_schemas.Comment])
async def read_event_comments(event_id: int, db: AsyncSession = Depends(get_db)):  # Добавлено async, изменён тип db
    comments = await event_crud.get_comments_by_event(db, event_id=event_id)  # Добавлено await
    return comments

@event_router.delete("/comments/{comment_id}")
async def delete_comment(  # Добавлено async
    comment_id: int, 
    user_id: int = Query(..., description="ID пользователя"), 
    db: AsyncSession = Depends(get_db)  # Изменён тип db
):
    success = await event_crud.delete_comment(db, comment_id=comment_id, user_id=user_id)  # Добавлено await
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found or you don't have permission to delete it")
    return {"message": "Comment deleted successfully"}

@event_router.get("/{event_id}", response_model=events_schemas.EventDetail)
async def read_event(event_id: int, db: AsyncSession = Depends(get_db)):  # Добавлено async, изменён тип db
    db_event = await event_crud.get_event(db, event_id=event_id)  # Добавлено await
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event