from pydantic import BaseModel, Field
from typing import List


class GateResponse(BaseModel):
    gate_id: str
    gate_name: str

    class Config:
        from_attributes = True


class ConnectionResponse(BaseModel):
    # outbound connection from the given gate
    target_gate_id: str
    target_gate_name: str
    distance_hu: float


class GateDetailResponse(BaseModel):
    gate_id: str
    gate_name: str
    connections: List[ConnectionResponse]

    class Config:
        from_attributes = True


class RouteSegment(BaseModel):
    from_gate_id: str
    to_gate_id: str
    distance_hu: float


class RouteResponse(BaseModel):
    start_gate_id: str
    end_gate_id: str
    total_distance_hu: float
    total_cost: float
    path: List[RouteSegment]
