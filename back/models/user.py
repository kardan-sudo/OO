from sqlalchemy import Column, Integer, String, Boolean, Date, Table, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base

# Ассоциативная таблица для many-to-many связи (User <-> Achievement)
user_achievements = Table(
    'user_achievements',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('achievement_id', Integer, ForeignKey('achievements.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=True)  # ФИО (полное имя)
    full_name = Column(String, nullable=False)  # ФИО (полное имя)
    date_of_birth = Column(Date, nullable=False)  # Дата рождения
    username = Column(String, unique=True, nullable=False, index=True)  # Логин (уникальный)
    password = Column(String, nullable=False)  # Пароль (открытый)
    is_organizer = Column(Boolean, default=False)  # Организатор или нет
    is_representative = Column(Boolean, default=False)  # Представитель или нет
    last_login = Column(Date, nullable=True)  # Дата последнего входа
    consecutive_days = Column(Integer, default=0)  # Дни подряд

    # Relationship для достижений (many-to-many)
    achievements = relationship(
        "Achievement",
        secondary=user_achievements,
        back_populates="users"
    )
    
    representation_requests = relationship(
        "RepresentationRequest", 
        back_populates="user",
        cascade="all, delete"
    )

class RequestStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class RepresentationRequest(Base):
    __tablename__ = "representation_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    position = Column(String(200), nullable=False)  # Должность
    organization = Column(String(200), nullable=False)  # Организация
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING, index=True)
    
    # Связь с пользователем
    user = relationship("User", back_populates="representation_requests")
