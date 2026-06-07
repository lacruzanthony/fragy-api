from google.genai import Client, types
from app.services.exceptions import ImageUnreadableError, ServiceError
from app.services.vision.protocol import VisionProvider
from app.services.vision.prompts import PERFUME_EXPERT_PROMPT


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
