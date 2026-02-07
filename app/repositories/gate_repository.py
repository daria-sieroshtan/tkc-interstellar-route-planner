from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Connection, Gate
from app.schemas.gate import ConnectionResponse, GateDetailResponse, GateResponse, RouteSegment


class GateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_gates(self) -> list[GateResponse]:
        result = await self.session.execute(select(Gate))
        gates = result.scalars().all()
        return [GateResponse.model_validate(gate) for gate in gates]

    async def gate_exists(self, gate_id: str) -> bool:
        result = await self.session.execute(select(Gate).where(Gate.gate_id == gate_id.upper()))
        return result.scalar_one_or_none() is not None

    async def get_gate_with_connections(self, gate_id: str) -> GateDetailResponse | None:
        result = await self.session.execute(select(Gate).where(Gate.gate_id == gate_id.upper()))
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
                distance_hu=conn.distance_hu,
            )
            for conn, target_gate in connections_result.all()
        ]

        return GateDetailResponse(gate_id=gate.gate_id, gate_name=gate.gate_name, connections=connections)

    async def get_all_connections(self) -> list[RouteSegment]:
        result = await self.session.execute(select(Connection))
        connections = result.scalars().all()
        return [
            RouteSegment(
                from_gate_id=conn.from_gate_id,
                to_gate_id=conn.to_gate_id,
                distance_hu=conn.distance_hu,
            )
            for conn in connections
        ]
