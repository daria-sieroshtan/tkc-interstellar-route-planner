from fastapi import APIRouter, Depends, Query

from app.dependencies import get_transport_service
from app.schemas.transport import TransportResponse
from app.services.transport_service import TransportService

router = APIRouter()


@router.get("/{distance}", response_model=TransportResponse)
async def calculate_transport_cost(
    distance: float,
    passengers: int = Query(..., ge=1, description="Number of passengers"),
    parking: int = Query(0, ge=0, description="Number of days of parking required"),
    service: TransportService = Depends(get_transport_service),
) -> TransportResponse:
    return await service.calculate_transport_cost(distance, passengers, parking)
