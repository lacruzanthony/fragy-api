from fastapi import APIRouter
from app.api.routes import perfumes

api_router = APIRouter()

# Registramos el router de perfumes bajo el prefijo /perfumes
api_router.include_router(perfumes.router, prefix="/perfumes", tags=["perfumes"])