from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from schemas.users import UserCreate, UserResponse, UserLogin, UserID
from routers.crud.user import user_crud
from schemas.achievement import AchievementResponse
from routers.crud.achievement import achievement_crud
from typing import List

user_router = APIRouter(prefix="", tags=["users"])

@user_router.post("/user/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Проверяем уникальность username
    existing_user = await user_crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = await user_crud.create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="Registration failed")
    return db_user

@user_router.post("/user/login", response_model=UserResponse)
async def login_user(user_login: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await user_crud.authenticate_user(db, user_login)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user



@user_router.get("/users/{user_id}/achievements", response_model=List[AchievementResponse])
async def get_user_achievements(user_id: int, db: AsyncSession = Depends(get_db)):
    achievements = await achievement_crud.get_user_achievements(db, user_id)
    return achievements

@user_router.post("/user/me", response_model=UserResponse)  # POST для тела
async def get_user_by_id(user: UserID, db: AsyncSession = Depends(get_db)):
    existing_user = await user_crud.get_user_by_id(db, user.id)
    if existing_user:
        return UserResponse.from_orm(existing_user)  # Конвертация
    else:
        raise HTTPException(status_code=400, detail="User not found")