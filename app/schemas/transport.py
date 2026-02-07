from enum import StrEnum

from pydantic import BaseModel, Field


class VehicleType(StrEnum):
    PERSONAL = "Personal Transport"
    HSTC = "HSTC Transport"


class TransportResponse(BaseModel):
    vehicle_type: VehicleType = Field(..., description="Type of vehicle")
    cost: float = Field(..., description="Total cost in GBP")
    distance: float = Field(..., description="Distance in Astronomical Units (AU)")
    passengers: int = Field(..., description="Number of passengers")
    parking_days: int = Field(..., description="Number of days of parking")

    class Config:
        json_schema_extra = {
            "example": {
                "vehicle_type": "Personal Transport",
                "cost": 5.30,
                "distance": 1.0,
                "passengers": 2,
                "parking_days": 0,
            }
        }
