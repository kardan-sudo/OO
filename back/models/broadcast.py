from sqlalchemy import Column, Integer, String, Date, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class MemorialDate(Base):
    __tablename__ = "memorial_dates"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)  # Дата без года (MM-DD)
    title = Column(String(200), nullable=False)