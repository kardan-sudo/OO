from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    event_type = Column(String(50), nullable=False, index=True)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    address = Column(String(300), nullable=False)
    x_coordinate = Column(Float, nullable=False)
    y_coordinate = Column(Float, nullable=False)
    rating = Column(Float, default=0.0)
    organizer = Column(String(150), nullable=False)
    description = Column(Text)
    description_summ = Column(Text)
    website = Column(String(200))
    phone = Column(String(20))
    is_verified = Column(Boolean, default=False)
    
    ratings = relationship("Rating", back_populates="event", cascade="all, delete")
    comments = relationship("Comment", back_populates="event", cascade="all, delete")

class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    
    event = relationship("Event", back_populates="ratings")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, nullable=False)
    comment_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    event = relationship("Event", back_populates="comments")
