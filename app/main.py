from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API for calculating interstellar journey costs through the HSTC hyperspace gate network",
    debug=settings.DEBUG,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check"""
    return {
        "status": "operational",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


# Include API routes
app.include_router(api_router)
