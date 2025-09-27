from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.sql import func
from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)  # ФИО (полное имя)
    date_of_birth = Column(Date, nullable=False)  # Дата рождения
    username = Column(String, unique=True, nullable=False, index=True)  # Логин (уникальный)
    password = Column(String, nullable=False)  # Пароль
    is_organizer = Column(Boolean, default=False)  # Организатор или нет
    is_representative = Column(Boolean, default=False)  # Представитель или нет
    
    created_at = Column(Date, default=func.now())  # Дата создания
    updated_at = Column(Date, default=func.now(), onupdate=func.now())  # Дата обновления
