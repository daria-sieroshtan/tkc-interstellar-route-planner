from unittest.mock import AsyncMock

import pytest

from app.repositories.gate_repository import GateRepository
from app.schemas.gate import RouteSegment
from app.services.route_service import RouteService


@pytest.fixture
def mock_repository():
    return AsyncMock(spec=GateRepository)


@pytest.fixture
def route_service(mock_repository):
    return RouteService(mock_repository)


@pytest.fixture
def all_gate_connections():
    return [
        # SOL connections
        RouteSegment(from_gate_id="SOL", to_gate_id="RAN", distance_hu=100.0),
        RouteSegment(from_gate_id="SOL", to_gate_id="PRX", distance_hu=90.0),
        RouteSegment(from_gate_id="SOL", to_gate_id="SIR", distance_hu=100.0),
        RouteSegment(from_gate_id="SOL", to_gate_id="ARC", distance_hu=200.0),
        RouteSegment(from_gate_id="SOL", to_gate_id="ALD", distance_hu=250.0),
        # PRX connections
        RouteSegment(from_gate_id="PRX", to_gate_id="SOL", distance_hu=90.0),
        RouteSegment(from_gate_id="PRX", to_gate_id="SIR", distance_hu=100.0),
        RouteSegment(from_gate_id="PRX", to_gate_id="ALT", distance_hu=150.0),
        # SIR connections
        RouteSegment(from_gate_id="SIR", to_gate_id="SOL", distance_hu=80.0),
        RouteSegment(from_gate_id="SIR", to_gate_id="PRX", distance_hu=10.0),
        RouteSegment(from_gate_id="SIR", to_gate_id="CAS", distance_hu=200.0),
        # CAS connections
        RouteSegment(from_gate_id="CAS", to_gate_id="SIR", distance_hu=200.0),
        RouteSegment(from_gate_id="CAS", to_gate_id="PRO", distance_hu=120.0),
        # PRO connections
        RouteSegment(from_gate_id="PRO", to_gate_id="CAS", distance_hu=80.0),
        # DEN connections
        RouteSegment(from_gate_id="DEN", to_gate_id="PRO", distance_hu=5.0),
        RouteSegment(from_gate_id="DEN", to_gate_id="ARC", distance_hu=2.0),
        RouteSegment(from_gate_id="DEN", to_gate_id="FOM", distance_hu=8.0),
        RouteSegment(from_gate_id="DEN", to_gate_id="RAN", distance_hu=100.0),
        RouteSegment(from_gate_id="DEN", to_gate_id="ALD", distance_hu=3.0),
        # RAN connections
        RouteSegment(from_gate_id="RAN", to_gate_id="SOL", distance_hu=100.0),
        # ARC connections
        RouteSegment(from_gate_id="ARC", to_gate_id="SOL", distance_hu=500.0),
        RouteSegment(from_gate_id="ARC", to_gate_id="DEN", distance_hu=120.0),
        # FOM connections
        RouteSegment(from_gate_id="FOM", to_gate_id="PRX", distance_hu=10.0),
        RouteSegment(from_gate_id="FOM", to_gate_id="DEN", distance_hu=20.0),
        RouteSegment(from_gate_id="FOM", to_gate_id="ALS", distance_hu=9.0),
        # ALT connections
        RouteSegment(from_gate_id="ALT", to_gate_id="FOM", distance_hu=140.0),
        RouteSegment(from_gate_id="ALT", to_gate_id="VEG", distance_hu=220.0),
        # VEG connections
        RouteSegment(from_gate_id="VEG", to_gate_id="ARC", distance_hu=220.0),
        RouteSegment(from_gate_id="VEG", to_gate_id="ALD", distance_hu=580.0),
        # ALD connections
        RouteSegment(from_gate_id="ALD", to_gate_id="SOL", distance_hu=200.0),
        RouteSegment(from_gate_id="ALD", to_gate_id="ALS", distance_hu=160.0),
        RouteSegment(from_gate_id="ALD", to_gate_id="VEG", distance_hu=320.0),
        # ALS connections
        RouteSegment(from_gate_id="ALS", to_gate_id="ALT", distance_hu=1.0),
        RouteSegment(from_gate_id="ALS", to_gate_id="ALD", distance_hu=1.0),
    ]


@pytest.mark.asyncio
async def test_direct_connection_route(route_service, mock_repository, all_gate_connections):
    # Arrange
    mock_repository.gate_exists.side_effect = lambda gate_id: gate_id in ["SOL", "PRX"]
    mock_repository.get_all_connections.return_value = all_gate_connections

    # Act
    result = await route_service.calculate_cheapest_route("SOL", "PRX")

    # Assert
    assert result is not None
    assert result.start_gate_id == "SOL"
    assert result.end_gate_id == "PRX"
    assert result.total_distance_hu == 180.0
    assert result.total_cost == 18.0
    assert len(result.path) == 2

    assert result.path[0].from_gate_id == "SOL"
    assert result.path[0].to_gate_id == "PRX"
    assert result.path[0].distance_hu == 90.0

    assert result.path[1].from_gate_id == "PRX"
    assert result.path[1].to_gate_id == "SOL"
    assert result.path[1].distance_hu == 90.0


@pytest.mark.asyncio
async def test_multi_hop_route_finds_shortest_path(route_service, mock_repository, all_gate_connections):
    # Round trip: SOL -> ALS -> SOL
    # Outbound: SOL -> ARC -> DEN -> FOM -> ALS (337 HU)
    # Inbound: ALS -> ALD -> SOL (201 HU)
    # Total: 538 HU

    # Arrange
    mock_repository.gate_exists.side_effect = lambda gate_id: gate_id in ["SOL", "ALS"]
    mock_repository.get_all_connections.return_value = all_gate_connections

    # Act
    result = await route_service.calculate_cheapest_route("SOL", "ALS")

    # Assert
    assert result is not None
    assert result.start_gate_id == "SOL"
    assert result.end_gate_id == "ALS"
    assert result.total_distance_hu == 538.0
    assert result.total_cost == pytest.approx(53.8)
    assert len(result.path) == 6

    # Outbound path
    assert result.path[0].from_gate_id == "SOL"
    assert result.path[0].to_gate_id == "ARC"
    assert result.path[0].distance_hu == 200.0

    assert result.path[1].from_gate_id == "ARC"
    assert result.path[1].to_gate_id == "DEN"
    assert result.path[1].distance_hu == 120.0

    assert result.path[2].from_gate_id == "DEN"
    assert result.path[2].to_gate_id == "FOM"
    assert result.path[2].distance_hu == 8.0

    assert result.path[3].from_gate_id == "FOM"
    assert result.path[3].to_gate_id == "ALS"
    assert result.path[3].distance_hu == 9.0

    # Inbound path
    assert result.path[4].from_gate_id == "ALS"
    assert result.path[4].to_gate_id == "ALD"
    assert result.path[4].distance_hu == 1.0

    assert result.path[5].from_gate_id == "ALD"
    assert result.path[5].to_gate_id == "SOL"
    assert result.path[5].distance_hu == 200.0


@pytest.mark.asyncio
async def test_case_insensitive_gate_codes(route_service, mock_repository, all_gate_connections):
    # Arrange
    mock_repository.gate_exists.side_effect = lambda gate_id: gate_id in ["SOL", "PRX"]
    mock_repository.get_all_connections.return_value = all_gate_connections

    # Act
    result = await route_service.calculate_cheapest_route("sol", "prx")

    # Assert
    assert result is not None
    assert result.start_gate_id == "SOL"
    assert result.end_gate_id == "PRX"
    assert result.total_distance_hu == 180.0


@pytest.mark.asyncio
async def test_non_existent_start_gate(route_service, mock_repository, all_gate_connections):
    # Arrange
    mock_repository.gate_exists.side_effect = lambda gate_id: gate_id == "PRX"
    mock_repository.get_all_connections.return_value = all_gate_connections

    # Act
    result = await route_service.calculate_cheapest_route("INVALID", "PRX")

    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_non_existent_end_gate(route_service, mock_repository, all_gate_connections):
    # Arrange
    mock_repository.gate_exists.side_effect = lambda gate_id: gate_id == "SOL"
    mock_repository.get_all_connections.return_value = all_gate_connections

    # Act
    result = await route_service.calculate_cheapest_route("SOL", "INVALID")

    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_both_gates_non_existent(route_service, mock_repository, all_gate_connections):
    # Arrange
    mock_repository.gate_exists.return_value = False
    mock_repository.get_all_connections.return_value = all_gate_connections

    # Act
    result = await route_service.calculate_cheapest_route("INVALID1", "INVALID2")

    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_no_path_exists_between_gates(route_service, mock_repository):
    # Arrange
    isolated_connections = [
        RouteSegment(from_gate_id="GATE_A", to_gate_id="GATE_C", distance_hu=10.0),
        RouteSegment(from_gate_id="GATE_B", to_gate_id="GATE_D", distance_hu=10.0),
    ]
    mock_repository.gate_exists.return_value = True
    mock_repository.get_all_connections.return_value = isolated_connections

    # Act
    result = await route_service.calculate_cheapest_route("GATE_A", "GATE_B")

    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_same_start_and_end_gate(route_service, mock_repository, all_gate_connections):
    # Arrange
    mock_repository.gate_exists.return_value = True
    mock_repository.get_all_connections.return_value = all_gate_connections

    # Act
    result = await route_service.calculate_cheapest_route("SOL", "SOL")

    # Assert
    # Should return a valid result with zero distance
    assert result is not None
    assert result.start_gate_id == "SOL"
    assert result.end_gate_id == "SOL"
    assert result.total_distance_hu == 0.0
    assert result.total_cost == 0.0
    assert len(result.path) == 0


@pytest.mark.asyncio
async def test_empty_connections_graph(route_service, mock_repository):
    # Arrange
    mock_repository.gate_exists.return_value = True
    mock_repository.get_all_connections.return_value = []

    # Act
    result = await route_service.calculate_cheapest_route("SOL", "PRX")

    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_one_way_connection_only(route_service, mock_repository):
    # Arrange
    one_way_connections = [
        RouteSegment(from_gate_id="GATE_A", to_gate_id="GATE_B", distance_hu=10.0),
    ]
    mock_repository.gate_exists.return_value = True
    mock_repository.get_all_connections.return_value = one_way_connections

    # Act
    result = await route_service.calculate_cheapest_route("GATE_A", "GATE_B")

    # Assert
    assert result is None
