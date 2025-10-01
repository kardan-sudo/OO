from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from typing import List, Optional
from models.trip import WalkingRoute
from schemas.trip import WalkingRouteCreate, RouteFilter

class WalkingRouteCRUD:
    async def create_walking_route(
        self, 
        db: AsyncSession, 
        route_data: WalkingRouteCreate
    ) -> WalkingRoute:
        db_route = WalkingRoute(**route_data.dict())
        db.add(db_route)
        await db.commit()
        await db.refresh(db_route)
        return db_route

    async def get_walking_route(
        self, 
        db: AsyncSession, 
        route_id: int
    ) -> Optional[WalkingRoute]:
        stmt = select(WalkingRoute).where(WalkingRoute.id == route_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_walking_routes(
        self,
        db: AsyncSession,
        filters: Optional[RouteFilter] = None
    ) -> List[WalkingRoute]:
        stmt = select(WalkingRoute)
        
        if filters:
            conditions = []
            
            # Фильтр по протяженности
            if filters.min_distance is not None:
                conditions.append(WalkingRoute.distance_km >= filters.min_distance)
            if filters.max_distance is not None:
                conditions.append(WalkingRoute.distance_km <= filters.max_distance)
            
            # Фильтр по времени
            if filters.min_duration is not None:
                conditions.append(WalkingRoute.duration_minutes >= filters.min_duration)
            if filters.max_duration is not None:
                conditions.append(WalkingRoute.duration_minutes <= filters.max_duration)
            
            # Фильтр по количеству интересных мест
            if filters.min_points is not None:
                conditions.append(WalkingRoute.points_of_interest_count >= filters.min_points)
            
            # Фильтр по сложности
            if filters.difficulty:
                conditions.append(WalkingRoute.difficulty == filters.difficulty)
            
            if conditions:
                stmt = stmt.where(and_(*conditions))
        
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_walking_routes_count(
        self,
        db: AsyncSession,
        filters: Optional[RouteFilter] = None
    ) -> int:
        stmt = select(func.count(WalkingRoute.id))
        
        if filters:
            conditions = []
            
            if filters.min_distance is not None:
                conditions.append(WalkingRoute.distance_km >= filters.min_distance)
            if filters.max_distance is not None:
                conditions.append(WalkingRoute.distance_km <= filters.max_distance)
            
            if filters.min_duration is not None:
                conditions.append(WalkingRoute.duration_minutes >= filters.min_duration)
            if filters.max_duration is not None:
                conditions.append(WalkingRoute.duration_minutes <= filters.max_duration)
            
            if filters.min_points is not None:
                conditions.append(WalkingRoute.points_of_interest_count >= filters.min_points)
            
            if filters.difficulty:
                conditions.append(WalkingRoute.difficulty == filters.difficulty)
            
            if conditions:
                stmt = stmt.where(and_(*conditions))
        
        result = await db.execute(stmt)
        return result.scalar_one()
    
walking_routes_crud = WalkingRouteCRUD()