from app.core.config import settings
from app.services.supabase import supabase_client
from .exceptions import (
    RecognitionError,
    ImageUnreadableError,
    PerfumeNotFoundError,
    ServiceError
)
from .vision.protocol import VisionProvider

if settings.AI_PROVIDER == "gemini":
    from .vision.gemini import GeminiVisionProvider
    _vision: VisionProvider = GeminiVisionProvider(api_key=settings.AI_API_KEY)
elif settings.AI_PROVIDER == "openrouter":
    from .vision.openrouter import OpenRouterVisionProvider
    _vision: VisionProvider = OpenRouterVisionProvider(api_key=settings.OPENROUTER_API_KEY)
else:
    raise ServiceError(f"Unknown AI provider: {settings.AI_PROVIDER}")

async def scan_perfume(image_bytes: bytes):
    try:
        brand, name = await _vision.identify(image_bytes)
    except RecognitionError:
        raise
    except Exception as e:
        raise ServiceError("Failed to connect to the AI service.")

    try:
        response = supabase_client.table("perfumes") \
            .select("id, name, brand") \
            .ilike("name", f"%{name}%") \
            .or_(f"brand.ilike.%{brand}%,name.ilike.%{brand}%") \
            .execute()

        if not response.data:
            raise PerfumeNotFoundError(f"Perfume '{brand} {name}' identified but not found in database.")

        perfume = response.data[0]
        perfume["name"] = perfume.get("name", "").strip()
        perfume["brand"] = perfume.get("brand", "").strip()
        return perfume

    except RecognitionError:
        raise
    except Exception as e:
        raise ServiceError("Database connection error.")
