import os
from abc import ABC, abstractmethod

import fal_client


class ImageProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Devuelve URL de la imagen generada."""
        raise NotImplementedError


def build_image_prompt(profile: dict, producto: str, objective: str) -> str:
    style_modifiers = {
        "MAS_VENTAS": (
            "High-end commercial product photography, studio lighting, "
            "clean background, sharp focus, professional composition."
        ),
        "MAS_INTERACCION": (
            "Authentic lifestyle photography, organic framing, natural lighting, "
            "warm and engaging atmosphere, candid moment."
        ),
        "LANZAR_PRODUCTO": (
            "Hero shot, dramatic studio lighting, modern and premium aesthetic, "
            "striking composition, high detail."
        ),
        "VISIBILIDAD": (
            "Contextual photography, vibrant colors, authentic local environment, "
            "visually compelling storytelling framing."
        ),
    }

    if objective not in style_modifiers:
        raise ValueError(f"Invalid objective: {objective}")

    modifier = style_modifiers[objective]

    return (
        f"Professional social media photo for a business in the {profile['rubro']} industry. "
        f"Product: {producto}. Located in {profile['ciudad']}. "
        f"{modifier} No text, no logos, photorealistic, 8k resolution."
    )


class MockImageProvider(ImageProvider):
    def generate(self, prompt: str) -> str:
        return "https://example.com/mock-instagram-image-1080x1350.jpg"


class FalImageProvider(ImageProvider):
    def __init__(self, model: str = "fal-ai/fast-sdxl"):
        self.model = model

    def generate(self, prompt: str) -> str:
        if not os.getenv("FAL_KEY"):
            raise RuntimeError("FAL_KEY environment variable is not configured.")

        result = fal_client.subscribe(
            self.model,
            arguments={
                "prompt": prompt,
                "image_size": "portrait_4_3",
                "num_images": 1,
            },
        )

        images = result.get("images", [])
        if not images:
            raise RuntimeError("Fal.ai did not return any images.")

        image_url = images[0].get("url")
        if not image_url:
            raise RuntimeError("Fal.ai image response did not include a URL.")

        return image_url