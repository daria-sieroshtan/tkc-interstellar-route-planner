from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_gate_repository, get_route_service
from app.repositories.gate_repository import GateRepository
from app.schemas.gate import GateDetailResponse, GateResponse, RouteResponse
from app.services.route_service import RouteService

router = APIRouter()


@router.get("", response_model=list[GateResponse])
async def list_gates(
    repository: GateRepository = Depends(get_gate_repository),
) -> list[GateResponse]:
    return await repository.get_all_gates()


@router.get("/{gate_code}", response_model=GateDetailResponse)
async def get_gate(gate_code: str, repository: GateRepository = Depends(get_gate_repository)) -> GateDetailResponse:
    gate = await repository.get_gate_with_connections(gate_code)

    if not gate:
        raise HTTPException(status_code=404, detail=f"Gate {gate_code} not found")

    return gate


@router.get("/{gate_code}/to/{target_gate_code}", response_model=RouteResponse)
async def calculate_route(
    gate_code: str, target_gate_code: str, service: RouteService = Depends(get_route_service)
) -> RouteResponse:
    route = await service.calculate_cheapest_route(gate_code, target_gate_code)

    if not route:
        raise HTTPException(status_code=404, detail=f"No route found from {gate_code} to {target_gate_code}")

    return route
