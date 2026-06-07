import base64
import anthropic
from app.services.exceptions import ImageUnreadableError, ServiceError
from app.services.vision.protocol import VisionProvider
from app.services.vision.prompts import PERFUME_EXPERT_PROMPT


class DeepSeekVisionProvider(VisionProvider):
    def __init__(self, api_key: str, model: str = "deepseek-v4-pro"):
        self._client = anthropic.Anthropic(
            api_key=api_key,
            base_url="https://api.deepseek.com/anthropic"
        )
        self._model = model

    async def identify(self, image_bytes: bytes) -> tuple[str, str]:
        try:
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")

            message = self._client.messages.create(
                model=self._model,
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_b64
                                }
                            },
                            {
                                "type": "text",
                                "text": PERFUME_EXPERT_PROMPT
                            }
                        ]
                    }
                ]
            )

            print(f"DeepSeek content types: {[type(b).__name__ for b in message.content]}")
            for block in message.content:
                print(f"  block type={block.type}, dir={[a for a in dir(block) if not a.startswith('_')]}")

            text = ""
            for block in message.content:
                if block.type == "text":
                    text = getattr(block, "text", "").strip()
                    break

            print(f"DeepSeek extracted text: '{text}'")

            if not text or "Unknown" in text:
                raise ImageUnreadableError("Could not identify the perfume from the image.")

            brand, _, name = text.partition("|")
            return brand.strip(), name.strip()

        except (ImageUnreadableError, ServiceError):
            raise
        except Exception as e:
            print(f"DeepSeek API Error: {e}")
            raise ServiceError("Failed to connect to the AI service.")
