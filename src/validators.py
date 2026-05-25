from typing import List

from pydantic import BaseModel


class InstagramCaptionSchema(BaseModel):
    caption: str
    hashtags: List[str]
    cta: str
    platform: str
    tone_check: str