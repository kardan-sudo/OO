from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base
from models.user import user_achievements

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)  # Название достижения (уникальное)
    description = Column(String, nullable=True)  # Описание

    # Relationship для пользователей (many-to-many)
    users = relationship(
        "User",
        secondary=user_achievements,
        back_populates="achievements"
    )
