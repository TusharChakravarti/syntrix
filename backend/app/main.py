from fastapi import FastAPI
from app.core.config import settings
from app.api.routes.health import router as health_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug= settings.debug

)

app.include_router(health_router)

@app.get("/")
def root():
    return{
        "message":"Welcome to Syntrix API",
        "status":"running"
    }

@app.get("/health")
def health_check():
    return {"status":"health"}
