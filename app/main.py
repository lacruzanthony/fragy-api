from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Incluimos todas las rutas bajo el prefijo /api/v1 (ej: /api/v1/perfumes/identify)
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def health():
    return {"message": "Perfume Recognition API is live"}