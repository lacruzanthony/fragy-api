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
else:
    raise ServiceError(f"Unknown AI provider: {settings.AI_PROVIDER}")

async def scan_perfume(image_bytes: bytes):
    try:
        brand, name = await _vision.identify(image_bytes)
    except RecognitionError:
        raise
    except Exception as e:
        print(f"Vision API Error: {e}")
        raise ServiceError("Failed to connect to the AI service.")

    try:
        response = supabase_client.table("perfumes") \
            .select("id, name") \
            .ilike("name", f"%{name}%") \
            .or_(f"brand.ilike.%{brand}%,name.ilike.%{brand}%") \
            .execute()

        if not response.data:
            raise PerfumeNotFoundError(f"Perfume '{brand} {name}' identified but not found in database.")

        return response.data[0]

    except RecognitionError:
        raise
    except Exception as e:
        print(f"Supabase Error: {e}")
        raise ServiceError("Database connection error.")
