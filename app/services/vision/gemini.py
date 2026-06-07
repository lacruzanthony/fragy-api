from google.genai import Client, types
from app.services.exceptions import ImageUnreadableError, ServiceError
from app.services.vision.protocol import VisionProvider

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


class GeminiVisionProvider(VisionProvider):
    def __init__(self, api_key: str, model: str = "gemini-3.1-flash-lite"):
        self._client = Client(api_key=api_key)
        self._model = model

    async def identify(self, image_bytes: bytes) -> tuple[str, str]:
        try:
            image_part = types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg"
            )

            response = self._client.models.generate_content(
                model=self._model,
                contents=[PERFUME_EXPERT_PROMPT, image_part]
            )

            text = response.text.strip() if response.text else ""

            if not text or "Unknown" in text:
                raise ImageUnreadableError("Could not identify the perfume from the image.")

            brand, _, name = text.partition("|")
            return brand.strip(), name.strip()

        except (ImageUnreadableError, ServiceError):
            raise
        except Exception as e:
            print(f"Gemini API Error: {e}")
            raise ServiceError("Failed to connect to the AI service.")
