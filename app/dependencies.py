from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.repositories.gate_repository import GateRepository
from app.services.route_service import RouteService


def get_gate_repository(session: AsyncSession = Depends(get_db)) -> GateRepository:
    return GateRepository(session)


def get_route_service(repository: GateRepository = Depends(get_gate_repository)) -> RouteService:
    return RouteService(repository)
