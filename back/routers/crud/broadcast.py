from sqlalchemy.orm import Session
from sqlalchemy import and_, extract
from datetime import date
from app import models
from typing import List

def get_active_users(db: Session) -> List[models.User]:
    """Получить всех активных пользователей"""
    return db.query(models.User).filter(models.User.is_active == True).all()

def get_memorial_dates_by_date(db: Session, target_date: date) -> List[models.MemorialDate]:
    """Получить памятные даты для конкретной даты (без учета года)"""
    return db.query(models.MemorialDate).filter(
        and_(
            extract('month', models.MemorialDate.date) == target_date.month,
            extract('day', models.MemorialDate.date) == target_date.day,
            models.MemorialDate.is_active == True
        )
    ).all()
