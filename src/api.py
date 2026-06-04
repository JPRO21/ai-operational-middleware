from fastapi import FastAPI
from pydantic import BaseModel

from src.ice_prompt_builder import build_prompt
from src.image_provider import FalImageProvider, build_image_prompt
from src.openai_client import generate_openai_response
from src.runtime_pipeline import run_generation_pipeline


app = FastAPI(
    title="AI Operational Middleware API",
    version="0.1.0",
)


class GenerateRequest(BaseModel):
    brand_id: int
    name: str
    details: str


class BusinessProfile(BaseModel):
    nombre_negocio: str
    rubro: str
    ciudad: str


class IceGenerateRequest(BaseModel):
    profile: BusinessProfile
    producto: str
    oferta: str = ""
    objective: str


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


@app.post("/generate/text")
def generate_text(request: IceGenerateRequest) -> dict:
    prompt = build_prompt(
        profile=request.profile.model_dump(),
        producto=request.producto,
        oferta=request.oferta,
        objective=request.objective,
    )

    result = generate_openai_response(
        runtime_prompt=prompt,
        use_real_api=True,
    )

    output = result["output"]

    return {
        "caption": output["caption"],
        "hashtags": output["hashtags"],
        "cta": output["cta"],
    }


@app.post("/generate/image")
def generate_image(request: IceGenerateRequest) -> dict:
    prompt = build_image_prompt(
        profile=request.profile.model_dump(),
        producto=request.producto,
        objective=request.objective,
    )

    provider = FalImageProvider()
    image_url = provider.generate(prompt)

    return {
        "url": image_url,
    }