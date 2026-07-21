from fastapi import FastAPI
from app.api.v1.tickets import router as ticket_router

app = FastAPI()
app.include_router(ticket_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to AI Service Desk API"
    }