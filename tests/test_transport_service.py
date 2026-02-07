import pytest

from app.schemas.transport import VehicleType
from app.services.transport_service import TransportService


@pytest.fixture
def transport_service():
    return TransportService()


@pytest.mark.asyncio
async def test_personal_transport_cheaper_with_no_parking(transport_service):
    # Arrange
    distance = 1.0
    passengers = 1
    parking_days = 0

    # Act
    result = await transport_service.calculate_transport_cost(distance, passengers, parking_days)

    # Assert
    assert result.vehicle_type == VehicleType.PERSONAL
    assert result.cost == 0.30
    assert result.distance == 1.0
    assert result.passengers == 1
    assert result.parking_days == 0


@pytest.mark.asyncio
async def test_hstc_transport_cheaper_with_parking(transport_service):
    # Arrange
    distance = 1.0
    passengers = 1
    parking_days = 5

    # Act
    result = await transport_service.calculate_transport_cost(distance, passengers, parking_days)

    # Assert
    assert result.vehicle_type == VehicleType.HSTC
    assert result.cost == 0.45
    assert result.distance == 1.0
    assert result.passengers == 1
    assert result.parking_days == 5


@pytest.mark.asyncio
async def test_hstc_transport_at_max_capacity(transport_service):
    # Arrange
    distance = 10.0
    passengers = 5
    parking_days = 3

    # Act
    result = await transport_service.calculate_transport_cost(distance, passengers, parking_days)

    # Assert
    assert result.vehicle_type == VehicleType.HSTC
    assert result.cost == 4.50
    assert result.passengers == 5


@pytest.mark.asyncio
async def test_multiple_hstc_vehicles_required(transport_service):
    # Arrange
    distance = 5.0
    passengers = 10
    parking_days = 2

    # Act
    result = await transport_service.calculate_transport_cost(distance, passengers, parking_days)

    # Assert
    assert result.vehicle_type == VehicleType.HSTC
    assert result.cost == 4.50
    assert result.passengers == 10


@pytest.mark.asyncio
async def test_equal_cost_prefers_personal(transport_service):
    # Arrange
    distance = 0.0
    passengers = 1
    parking_days = 0

    # Act
    result = await transport_service.calculate_transport_cost(distance, passengers, parking_days)

    # Assert
    assert result.vehicle_type == VehicleType.PERSONAL
    assert result.cost == 0.0
