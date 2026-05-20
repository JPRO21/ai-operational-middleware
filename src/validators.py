from pydantic import BaseModel
from typing import List


class InstagramCaptionSchema(BaseModel):
    caption: str
    hashtags: List[str]
    cta: str