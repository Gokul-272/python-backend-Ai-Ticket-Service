from contextlib import asynccontextmanager
from datetime import datetime, timezone
from app.core.middleware import add_response_time
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text
from app.core.cors import setup_cors
from app.api.v1.tickets import router as ticket_router
from app.api.v1.ai import router as ai_router
from app.core.database import AsyncSessionLocal, Base, engine, use_in_memory_fallback
from app.core.exceptions import ServiceDeskException

@asynccontextmanager
async def lifespan(app):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception:
        use_in_memory_fallback()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="AI Service Desk",version="1.0.0",lifespan=lifespan,)
setup_cors(app)
@app.exception_handler(ServiceDeskException)
async def service_desk_exception_handler(request, exc: ServiceDeskException):
    return JSONResponse(status_code=exc.status_code,content={"detail": exc.message})

app.middleware("http")(add_response_time)
@app.get("/")
async def root():
    return {"message": "Welcome to the AI Service Desk API!"}
@app.get("/health")
async def health():
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "service": "AI Service Desk",
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc)
        }
    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "AI Service Desk",
                "version": "1.0.0",
                "timestamp": datetime.now(timezone.utc)
            }
        )

@app.get("/ready")
async def ready():
    return {
        "status": " Ready ,All Set to Goooo!"
    }

app.include_router(ticket_router)
app.include_router(ai_router)