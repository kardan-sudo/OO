from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

DATABASE_URL_ASYNC = DATABASE_URL.replace("psycopg2", "asyncpg") if DATABASE_URL else None

engine = create_async_engine(DATABASE_URL_ASYNC, echo=True)  # echo=True для логов SQL-запросов (выключи в продакшене)

class Base(DeclarativeBase):
    pass

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
