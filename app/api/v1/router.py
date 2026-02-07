from fastapi import APIRouter
from app.api.v1.endpoints import transport, gates

api_router = APIRouter()

api_router.include_router(transport.router, prefix="/transport", tags=["Transport"])
api_router.include_router(gates.router, prefix="/gates", tags=["Gates"])
