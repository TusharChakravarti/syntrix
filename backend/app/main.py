from fastapi import FastAPI
from app.core.config import settings
from app.api.routes.health import router as health_router
from app.api.routes.users import router as user_router
from app.api.routes.organization import router as organization_router
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug= settings.debug

)

app.include_router(health_router)
app.include_router(user_router)
app.include_router(organization_router)

@app.get("/")
def root():
    return{
        "message":"Welcome to Syntrix API",
        "status":"running"
    }

@app.get("/health")
def health_check():
    return {"status":"health"}
