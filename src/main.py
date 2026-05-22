from config.settings import DEVELOPMENT_MODE
from src.openai_client import generate_openai_response

import json
import time

from pydantic import ValidationError

from config.database import get_db_connection
from src.validators import InstagramCaptionSchema


FORCE_INVALID_OUTPUT = False  # Cambia a True para probar validación de output inválido


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


def log_security_event(
    brand_id: int,
    prompt_id: int,
    product_data: dict,
    runtime_prompt: str,
    raw_output_received: dict,
    model_used: str,
    execution_time: float,
    security_flag: str
) -> None:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO ai_logs (
            brand_id,
            prompt_id,
            raw_input_data,
            final_prompt_sent,
            raw_output_received,
            model_used,
            execution_time_seconds,
            input_tokens,
            output_tokens,
            total_tokens,
            cost_usd,
            security_flag
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """,
        (
            brand_id,
            prompt_id,
            json.dumps(product_data),
            runtime_prompt,
            json.dumps(raw_output_received),
            model_used,
            execution_time,
            0,
            0,
            0,
            0,
            security_flag
        )
    )

    conn.commit()
    cur.close()
    conn.close()


def check_daily_budget(brand_id: int, daily_limit: float) -> None:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COALESCE(SUM(cost_usd), 0)
        FROM ai_logs
        WHERE brand_id = %s
          AND created_at >= CURRENT_DATE;
        """,
        (brand_id,)
    )

    today_cost = float(cur.fetchone()[0])

    cur.close()
    conn.close()

    if today_cost >= daily_limit:
        raise RuntimeError(
            f"Brand {brand_id}: límite diario de ${daily_limit} alcanzado. "
            f"Gasto actual: ${today_cost:.6f}."
        )

    print(f"💰 Daily budget OK: ${today_cost:.6f} / ${daily_limit:.2f}")


def calculate_cost(model_name: str, input_tokens: int, output_tokens: int) -> float:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT input_cost_per_1k, output_cost_per_1k
        FROM api_pricing
        WHERE model_name = %s
        ORDER BY id DESC
        LIMIT 1;
        """,
        (model_name,)
    )

    pricing = cur.fetchone()

    cur.close()
    conn.close()

    if not pricing:
        raise ValueError(f"No pricing found for model: {model_name}")

    input_cost_per_1k, output_cost_per_1k = pricing

    cost = (
        (input_tokens / 1000) * float(input_cost_per_1k)
        + (output_tokens / 1000) * float(output_cost_per_1k)
    )

    return round(cost, 6)


def run_dynamic_runtime(brand_id: int):

    start_time = time.time()

    brand, prompt = load_runtime_context(brand_id)

    if not brand:
        raise ValueError(f"No existe brand_id={brand_id}")

    if not prompt:
        raise ValueError("No hay prompt activo")

    brand_id, brand_name, brand_config = brand
    prompt_id, prompt_name, version, system_instruction = prompt

    daily_budget_usd = float(brand_config.get("daily_budget_usd", 1.0))

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

    try:
        if not DEVELOPMENT_MODE:
            check_daily_budget(
                brand_id=brand_id,
                daily_limit=daily_budget_usd
            )

    except RuntimeError as error:
        execution_time = round(time.time() - start_time, 2)

        log_security_event(
            brand_id=brand_id,
            prompt_id=prompt_id,
            product_data=product_data,
            runtime_prompt=runtime_prompt,
            raw_output_received={
                "error": "budget_exceeded",
                "message": "Execution stopped by budget guard before provider call."
            },
            model_used="budget_guard",
            execution_time=execution_time,
            security_flag="budget_exceeded"
        )

        print("\n🛑 Budget Guard detenido")
        print(str(error))
        return

    if DEVELOPMENT_MODE:
        print("🤖 [LLM Runtime] Mode: DEVELOPMENT")
    else:
        print("🤖 [LLM Runtime] Mode: PRODUCTION")

    provider_response = generate_openai_response(
        runtime_prompt=runtime_prompt,
        use_real_api=not DEVELOPMENT_MODE
    )

    raw_output = provider_response["output"]
    usage = provider_response["usage"]
    model_used = provider_response["model_used"]

    if FORCE_INVALID_OUTPUT:
        raw_output["hashtags"] = "#esto_deberia_fallar"

    try:
        validated_output = InstagramCaptionSchema(**raw_output)

    except ValidationError as error:
        execution_time = round(time.time() - start_time, 2)

        log_security_event(
            brand_id=brand_id,
            prompt_id=prompt_id,
            product_data=product_data,
            runtime_prompt=runtime_prompt,
            raw_output_received={
                "error": "invalid_output",
                "raw_output": raw_output,
                "validation_error": str(error)
            },
            model_used=model_used,
            execution_time=execution_time,
            security_flag="invalid_output"
        )

        print("\n🛑 Invalid Output detenido")
        print("El output no cumple el schema Pydantic.")
        print(error)
        return

    execution_time = round(time.time() - start_time, 2)

    cost_usd = calculate_cost(
        model_name=model_used,
        input_tokens=usage["input_tokens"],
        output_tokens=usage["output_tokens"]
    )

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO ai_logs (
            brand_id,
            prompt_id,
            raw_input_data,
            final_prompt_sent,
            raw_output_received,
            model_used,
            execution_time_seconds,
            input_tokens,
            output_tokens,
            total_tokens,
            cost_usd,
            security_flag
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """,
        (
            brand_id,
            prompt_id,
            json.dumps(product_data),
            runtime_prompt,
            json.dumps(validated_output.model_dump()),
            model_used,
            execution_time,
            usage["input_tokens"],
            usage["output_tokens"],
            usage["total_tokens"],
            cost_usd,
            None
        )
    )

    conn.commit()

    cur.close()
    conn.close()

    print("\n✅ Runtime + Security Flag Layer OK")

    print(f"\nBrand: {brand_name}")
    print(f"Prompt: {prompt_name} {version}")
    print(f"Tiempo de ejecución: {execution_time}s")
    print(f"Model used: {model_used}")

    print("\n--- USAGE METADATA ---")
    print(f"Input tokens: {usage['input_tokens']}")
    print(f"Output tokens: {usage['output_tokens']}")
    print(f"Total tokens: {usage['total_tokens']}")

    print("\n--- COST METADATA ---")
    print(f"Cost USD: ${cost_usd}")
    print(f"Daily budget limit: ${daily_budget_usd}")

    print("\n--- SECURITY ---")
    print("Security flag: None")

    print("\n--- OUTPUT VALIDADO ---")
    print(
        json.dumps(
            validated_output.model_dump(),
            indent=2,
            ensure_ascii=False
        )
    )


if __name__ == "__main__":
    run_dynamic_runtime(brand_id=1)