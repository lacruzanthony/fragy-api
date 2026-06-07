import base64
from openai import OpenAI
from app.services.exceptions import ImageUnreadableError, ServiceError
from app.services.vision.protocol import VisionProvider
from app.services.vision.prompts import PERFUME_EXPERT_PROMPT


class OpenRouterVisionProvider(VisionProvider):
    def __init__(self, api_key: str, model: str = "nvidia/nemotron-nano-12b-v2-vl:free"):
        self._client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self._model = model

    async def identify(self, image_bytes: bytes) -> tuple[str, str]:
        try:
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            data_uri = f"data:image/jpeg;base64,{image_b64}"

            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": PERFUME_EXPERT_PROMPT},
                            {"type": "image_url", "image_url": {"url": data_uri}}
                        ]
                    }
                ],
                stream=False,
            )

            print(f"OpenRouter model: {self._model}")
            print(f"OpenRouter response status: {response.choices[0].finish_reason}")
            print(f"OpenRouter raw text: '{response.choices[0].message.content}'")

            text = response.choices[0].message.content.strip()

            if not text or "Unknown" in text:
                raise ImageUnreadableError("Could not identify the perfume from the image.")

            brand, _, name = text.partition("|")
            print(f"OpenRouter parsed -> brand='{brand.strip()}', name='{name.strip()}'")
            return brand.strip(), name.strip()

        except (ImageUnreadableError, ServiceError):
            raise
        except Exception as e:
            print(f"OpenRouter API Error: {e}")
            raise ServiceError("Failed to connect to the AI service.")
