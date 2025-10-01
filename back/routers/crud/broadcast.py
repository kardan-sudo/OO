from sqlalchemy.orm import Session
from sqlalchemy import and_, extract
from datetime import date
from models import user, broadcast
from typing import List

def get_active_users(db: Session) -> List[user.User]:
    """Получить всех активных пользователей"""
    return db.query(user.User).filter(user.User.is_active == True).all()

def get_memorial_dates_by_date(db: Session, target_date: date) -> List[broadcast.MemorialDate]:
    """Получить памятные даты для конкретной даты (без учета года)"""
    return db.query(broadcast.MemorialDate).filter(
        and_(
            extract('month', broadcast.MemorialDate.date) == target_date.month,
            extract('day', broadcast.MemorialDate.date) == target_date.day,
            broadcast.MemorialDate.is_active == True
        )
    ).all()
