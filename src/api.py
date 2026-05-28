from fastapi import FastAPI
from pydantic import BaseModel

from src.runtime_pipeline import run_generation_pipeline


app = FastAPI(
    title="AI Operational Middleware API",
    version="0.1.0",
)


class GenerateRequest(BaseModel):
    brand_id: int
    name: str
    details: str


@app.get("/")
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "AI Operational Middleware",
    }


@app.post("/generate")
def generate_content(request: GenerateRequest) -> dict:
    output = run_generation_pipeline(
        brand_id=request.brand_id,
        raw_product_data={
            "name": request.name,
            "details": request.details,
        },
    )

    return output