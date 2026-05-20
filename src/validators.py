from pydantic import BaseModel, Field
from typing import List

class InstagramCaptionSchema(BaseModel):
    caption: str = Field(description="El texto principal del post.")
    hashtags: List[str] = Field(description="Lista de hashtags optimizados.")
    cta: str = Field(description="Llamado a la acción explícito.")
    platform: str = Field(default="instagram")