from google.genai import Client, types
from app.core.config import settings
from app.services.supabase import supabase_client
from .exceptions import (
    RecognitionError,
    ImageUnreadableError,
    PerfumeNotFoundError,
    ServiceError
)

client = Client(api_key=settings.AI_API_KEY)

PERFUME_EXPERT_PROMPT = """
You are a high-end niche perfumery expert and visual analyst. Your task is to identify the perfume in this image with surgical precision.

Follow these steps logically:
1. BRAND IDENTIFICATION: Look for the logo or coat of arms. Is it the distinct Parfums de Marly raised horses?
2. COLOR ANALYSIS: This is critical. 
- If the bottle is deep navy blue/matte blue, it is LAYTON.
- If the bottle is metallic brown/copper/dark red, it is HEROD.
- If the bottle is silver/grey, it is PEGASUS.
3. TEXTUAL CLUES: Try to read any text on the front label or the base of the bottle.
4. FINAL VERIFICATION: Does the color match the characteristic bottle for that specific model?

Return ONLY the Brand and Name in this format: "Brand | Name" (e.g., "Parfums de Marly | Layton").
If you are absolutely unable to identify the bottle, return "Unknown".
Do not provide descriptions or apologies. If unsure, provide your best expert guess based on the bottle color.
"""

async def scan_perfume(image_bytes: bytes):
    try:
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/jpeg"
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash-lite-preview-02-05",
            contents=[PERFUME_EXPERT_PROMPT, image_part]
        )
        
        text = response.text.strip() if response.text else ""
        
        if not text or "Unknown" in text:
            raise ImageUnreadableError("Could not identify the perfume from the image.")
            
        brand, _, name = text.partition("|")
        brand, name = brand.strip(), name.strip()

    except RecognitionError:
        raise
    except Exception as e:
        print(f"Gemini API Error: {e}")
        raise ServiceError("Failed to connect to the AI service.")

    try:
        response = supabase_client.table("perfumes") \
            .select("id, name") \
            .ilike("name", f"%{name}%") \
            .ilike("brand", f"%{brand}%") \
            .execute()

        if not response.data:
            raise PerfumeNotFoundError(f"Perfume '{brand} {name}' identified but not found in database.")

        return response.data[0]

    except RecognitionError:
        raise
    except Exception as e:
        print(f"Supabase Error: {e}")
        raise ServiceError("Database connection error.")
