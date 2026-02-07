import math

from app.schemas.transport import TransportResponse, VehicleType


class TransportService:
    PERSONAL_COST_PER_AU = 0.30
    PERSONAL_CAPACITY = 4
    HSTC_COST_PER_AU = 0.45
    HSTC_CAPACITY = 5
    PARKING_COST_PER_DAY = 5.0

    async def calculate_transport_cost(self, distance: float, passengers: int, parking_days: int) -> TransportResponse:
        personal_cost = self._calculate_personal_transport_cost(distance, passengers, parking_days)
        hstc_cost = self._calculate_hstc_transport_cost(distance, passengers)

        if personal_cost <= hstc_cost:
            return TransportResponse(
                vehicle_type=VehicleType.PERSONAL,
                cost=personal_cost,
                distance=distance,
                passengers=passengers,
                parking_days=parking_days,
            )
        else:
            return TransportResponse(
                vehicle_type=VehicleType.HSTC,
                cost=hstc_cost,
                distance=distance,
                passengers=passengers,
                parking_days=parking_days,
            )

    def _calculate_personal_transport_cost(self, distance: float, passengers: int, parking_days: int) -> float:
        num_vehicles = math.ceil(passengers / self.PERSONAL_CAPACITY)
        fuel_cost = distance * self.PERSONAL_COST_PER_AU * num_vehicles
        parking_cost = parking_days * self.PARKING_COST_PER_DAY * num_vehicles
        return fuel_cost + parking_cost

    def _calculate_hstc_transport_cost(self, distance: float, passengers: int) -> float:
        num_vehicles = math.ceil(passengers / self.HSTC_CAPACITY)
        return distance * self.HSTC_COST_PER_AU * num_vehicles
