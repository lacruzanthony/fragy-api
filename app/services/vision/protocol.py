from abc import ABC, abstractmethod


class VisionProvider(ABC):
    @abstractmethod
    async def identify(self, image_bytes: bytes) -> tuple[str, str]:
        ...
