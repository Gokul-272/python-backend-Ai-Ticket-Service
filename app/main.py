# from fastapi import FastAPI
# from app.api.v1.tickets import router as ticket_router

# app = FastAPI(
#     title="Ticket Management API",
# )
# app.include_router(ticket_router)

# @app.get("/")
# def home():
#     return {
#         "message": "Welcome to AI Service Desk - python backend task"
#     }


from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.tickets import router as ticket_router
from app.core.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Shutdown logic (if needed later)


app = FastAPI(
    title="AI Service Desk",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


app.include_router(ticket_router)