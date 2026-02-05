from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import leads
from app.database.mongo import db
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()
    yield
    db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.include_router(leads.router)

@app.get("/")
async def root():
    return {"message": "Lead Management API is running"}
