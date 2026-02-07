from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.repositories.gate_repository import GateRepository


def get_gate_repository(session: AsyncSession = Depends(get_db)) -> GateRepository:
    return GateRepository(session)
