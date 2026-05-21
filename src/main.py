import json
import time

from config.database import get_db_connection
from src.validators import InstagramCaptionSchema


def load_runtime_context(brand_id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, brand_name, brand_config FROM brands WHERE id = %s;",
        (brand_id,)
    )
    brand = cur.fetchone()

    cur.execute(
        """
        SELECT id, prompt_name, version, system_instruction
        FROM prompts
        WHERE prompt_name = %s AND is_active = TRUE
        LIMIT 1;
        """,
        ("instagram_caption_generator",)
    )
    prompt = cur.fetchone()

    cur.close()
    conn.close()

    return brand, prompt


def run_dynamic_runtime(brand_id: int):
    start_time = time.time()

    brand, prompt = load_runtime_context(brand_id)

    if not brand:
        raise ValueError(f"No existe brand_id={brand_id}")

    if not prompt:
        raise ValueError("No hay prompt activo")

    brand_id, brand_name, brand_config = brand
    prompt_id, prompt_name, version, system_instruction = prompt

    product_data = {
        "name": "Ficus Lyrata",
        "details": "Hojas grandes premium."
    }

    runtime_prompt = f"""
SYSTEM INSTRUCTION:
{system_instruction}

BRAND CONFIG:
{json.dumps(brand_config, ensure_ascii=False, indent=2)}

PRODUCT DATA:
{json.dumps(product_data, ensure_ascii=False, indent=2)}
"""

    mock_output = {
        "caption": f"La magia botánica del {product_data['name']} ya está aquí. Ideal para tu rincón favorito.",
        "hashtags": ["plantparents", "urbanjungle", "plantasmagicas"],
        "cta": brand_config["cta_default"]
    }

    validated_output = InstagramCaptionSchema(**mock_output)
    execution_time = round(time.time() - start_time, 2)

    print("\n✅ Runtime dinámico + validación Pydantic OK")
    print(f"\nBrand: {brand_name}")
    print(f"Prompt: {prompt_name} {version}")
    print(f"Tiempo de ejecución: {execution_time}s")

    print("\n--- RUNTIME PROMPT ---")
    print(runtime_prompt)

    print("\n--- OUTPUT VALIDADO ---")
    print(json.dumps(validated_output.model_dump(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    run_dynamic_runtime(brand_id=1)