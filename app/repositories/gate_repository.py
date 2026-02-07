from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models import Gate, Connection
from app.schemas.gate import GateDetailResponse, ConnectionResponse


class GateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_gate_with_connections(self, gate_id: str) -> Optional[GateDetailResponse]:
        result = await self.session.execute(
            select(Gate).where(Gate.gate_id == gate_id.upper())
        )
        gate = result.scalar_one_or_none()

        if not gate:
            return None

        connections_result = await self.session.execute(
            select(Connection, Gate)
            .join(Gate, Connection.to_gate_id == Gate.gate_id)
            .where(Connection.from_gate_id == gate_id.upper())
        )

        connections = [
            ConnectionResponse(
                target_gate_id=conn.to_gate_id,
                target_gate_name=target_gate.gate_name,
                distance_hu=conn.distance_hu
            )
            for conn, target_gate in connections_result.all()
        ]

        return GateDetailResponse(
            gate_id=gate.gate_id,
            gate_name=gate.gate_name,
            connections=connections
        )
