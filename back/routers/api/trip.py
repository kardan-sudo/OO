from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from schemas.trip import RouteFilter, WalkingRouteCreate, WalkingRouteListResponse, WalkingRouteResponse
from routers.crud.trip import walking_routes_crud

walking_route_router = APIRouter(prefix="/walking-routes", tags=["walking-routes"])



# Создать маршрут
@walking_route_router.post("/", response_model=WalkingRouteResponse, status_code=status.HTTP_201_CREATED)
async def create_walking_route(
    route_data: WalkingRouteCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Создать новый прогулочный маршрут
    """
    try:
        route = await walking_routes_crud.create_walking_route(db, route_data)
        return route
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating route: {str(e)}"
        )

# Получить список маршрутов с фильтрацией
@walking_route_router.get("/", response_model=WalkingRouteListResponse)
async def get_walking_routes(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Смещение"),
    limit: int = Query(20, ge=1, le=100, description="Лимит"),
    min_distance: Optional[float] = Query(None, ge=0, description="Минимальная протяженность (км)"),
    max_distance: Optional[float] = Query(None, ge=0, description="Максимальная протяженность (км)"),
    min_duration: Optional[int] = Query(None, ge=0, description="Минимальное время (мин)"),
    max_duration: Optional[int] = Query(None, ge=0, description="Максимальное время (мин)"),
    min_points: Optional[int] = Query(None, ge=0, description="Минимальное количество интересных мест"),
    difficulty: Optional[str] = Query(None, description="Сложность маршрута (easy, medium, hard)"),
    only_verified: bool = Query(True, description="Только проверенные маршруты"),
):
    """
    Получить список прогулочных маршрутов с фильтрацией
    """
    # Создаем объект фильтра
    filters = RouteFilter(
        min_distance=min_distance,
        max_distance=max_distance,
        min_duration=min_duration,
        max_duration=max_duration,
        min_points=min_points,
        difficulty=difficulty,
        only_verified=only_verified
    )
    
    routes = await walking_routes_crud.get_walking_routes(
        db=db,
        skip=skip,
        limit=limit,
        filters=filters
    )
    
    total = await walking_routes_crud.get_walking_routes_count(db=db, filters=filters)
    
    return WalkingRouteListResponse(
        items=routes,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )