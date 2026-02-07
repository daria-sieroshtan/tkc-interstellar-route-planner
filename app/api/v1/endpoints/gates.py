from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.gate import GateResponse, GateDetailResponse, RouteResponse
from app.repositories.gate_repository import GateRepository
from app.dependencies import get_gate_repository

router = APIRouter()


@router.get("", response_model=List[GateResponse])
async def list_gates():
    # TODO: Implement database query to fetch all gates
    return []


@router.get("/{gate_code}", response_model=GateDetailResponse)
async def get_gate(
    gate_code: str,
    repository: GateRepository = Depends(get_gate_repository)
):
    gate = await repository.get_gate_with_connections(gate_code)

    if not gate:
        raise HTTPException(status_code=404, detail=f"Gate {gate_code} not found")

    return gate


@router.get("/{gate_code}/to/{target_gate_code}", response_model=RouteResponse)
async def calculate_route(gate_code: str, target_gate_code: str):
    # TODO: Implement Dijkstra's algorithm
    raise HTTPException(
        status_code=404,
        detail=f"No route found from {gate_code} to {target_gate_code}"
    )
