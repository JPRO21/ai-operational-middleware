import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv("config/.env")

MODEL_NAME = "gpt-4.1-mini"


def generate_openai_response(runtime_prompt: str, use_real_api: bool = False) -> dict:

    if not use_real_api:
        print("🧪 Provider Layer usará mock. No se llama a OpenAI.")

        return {
            "output": {
                "caption": "Transforma tu espacio con una planta llena de vida y presencia natural.",
                "hashtags": [
                    "#PlantasDeInterior",
                    "#PlantasMagicas",
                    "#DecoracionNatural"
                ],
                "cta": "Escríbenos para reservar la tuya.",
                "platform": "instagram",
                "tone_check": "Alineado con tono orgánico y emocional."
            },
            "usage": {
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0
            },
            "model_used": "mock-openai-provider"
        }

    print("🌐 Provider Layer usará OpenAI real.")
    print("🌐 Ejecutando llamada real a OpenAI...")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un motor de generación de contenido para ecommerce visual. "
                    "Debes responder únicamente con JSON válido siguiendo exactamente el schema."
                )
            },
            {
                "role": "user",
                "content": runtime_prompt
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "instagram_caption_output",
                "strict": True,
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "caption": {
                            "type": "string"
                        },
                        "hashtags": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "cta": {
                            "type": "string"
                        },
                        "platform": {
                            "type": "string"
                        },
                        "tone_check": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "caption",
                        "hashtags",
                        "cta",
                        "platform",
                        "tone_check"
                    ]
                }
            }
        },
        temperature=0.7
    )

    usage = response.usage
    raw_content = response.choices[0].message.content

    return {
        "output": json.loads(raw_content),
        "usage": {
            "input_tokens": usage.prompt_tokens,
            "output_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens
        },
        "model_used": MODEL_NAME
    }