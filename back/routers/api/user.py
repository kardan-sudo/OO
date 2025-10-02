from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from schemas.users import RepresentationRequestCreate, RepresentationRequestList, RepresentationRequestResponse, RepresentationRequestUpdate, RepresentationRequestWithUserResponse, RequestStatus, UserCreate, UserResponse, UserLogin, UserID
from routers.crud.user import user_crud
from schemas.achievement import AchievementResponse
from routers.crud.achievement import achievement_crud
from typing import List
from routers.crud.user import representation_request_crud
from utils.sender import email_sender

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
    
@user_router.post("/requests", response_model=RepresentationRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_representation_request(
    request: RepresentationRequestCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать заявку на представительство"""
    try:
        db_request = await representation_request_crud.create_request(db, request)
        return db_request
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@user_router.get("/requests/pending", response_model=RepresentationRequestList)
async def get_pending_requests(db: AsyncSession = Depends(get_db)
):
    """Получить список всех неподтвержденных заявок"""
    requests = await representation_request_crud.get_pending_requests(db)
    
    # Преобразуем в response с информацией о пользователе
    requests_with_user = []
    for request in requests:
        request_dict = RepresentationRequestWithUserResponse.from_orm(request)
        request_dict.user_full_name = request.user.full_name
        requests_with_user.append(request_dict)
    
    total = await representation_request_crud.get_pending_requests_count(db)
    
    return RepresentationRequestList(
        items=requests_with_user,
        total=total
    )

@user_router.patch("/requests/{request_id}", response_model=RepresentationRequestResponse)
async def update_request_status(
    request_id: int,
    update_data: RepresentationRequestUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Обновить статус заявки (подтвердить/отклонить)"""
    # Получаем текущую заявку
    current_request = await representation_request_crud.get_request_by_id(db, request_id)
    if not current_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )
    
    # Обновляем статус
    updated_request = await representation_request_crud.update_request_status(
        db, request_id, update_data.status
    )
    
    if not updated_request:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update request"
        )
    
    # Отправляем email уведомление
    try:
        # Предполагаем, что у пользователя есть email поле (можно добавить в модель User)
        # user_email = current_request.user.email  
        user_email = current_request.user.email  # Заглушка
        
        if update_data.status == RequestStatus.APPROVED:
            await email_sender.send_request_approved_notification(
                user_email=user_email,
                user_name=current_request.user.full_name,
                position=current_request.position,
                organization=current_request.organization
            )
        elif update_data.status == RequestStatus.REJECTED:
            await email_sender.send_request_rejected_notification(
                user_email=user_email,
                user_name=current_request.user.full_name
            )
    except Exception as e:
        print(f"Failed to send email notification: {e}")
        # Не прерываем выполнение если email не отправился
    
    return updated_request