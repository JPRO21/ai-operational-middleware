import json
import time

from pydantic import ValidationError

from config.database import get_db_connection
from config.settings import DEVELOPMENT_MODE

from src.database_runtime import (
    load_runtime_context,
    log_security_event,
    check_daily_budget,
    calculate_cost,
)
from src.openai_client import generate_openai_response
from src.security import sanitize_input
from src.validators import InstagramCaptionSchema


FORCE_INVALID_OUTPUT = False


def get_sample_product_data() -> dict:
    return {
        "name": "Ficus Lyrata",
        "details": "Hojas grandes premium.",
    }


def sanitize_product_data(raw_product_data: dict) -> dict:
    return {
        "name": sanitize_input(raw_product_data["name"]),
        "details": sanitize_input(raw_product_data["details"]),
    }


def assemble_runtime_prompt(
    system_instruction: str,
    brand_config: dict,
    product_data: dict,
) -> str:
    return f"""
SYSTEM INSTRUCTION:
{system_instruction}

BRAND CONFIG:
{json.dumps(brand_config, ensure_ascii=False, indent=2)}

PRODUCT DATA:
{json.dumps(product_data, ensure_ascii=False, indent=2)}
"""


def run_budget_guard(
    brand_id: int,
    daily_budget_usd: float,
) -> None:
    if DEVELOPMENT_MODE:
        return

    check_daily_budget(
        brand_id=brand_id,
        daily_limit=daily_budget_usd,
    )


def execute_provider(runtime_prompt: str) -> dict:
    if DEVELOPMENT_MODE:
        print("🤖 [LLM Runtime] Mode: DEVELOPMENT")
    else:
        print("🤖 [LLM Runtime] Mode: PRODUCTION")

    return generate_openai_response(
        runtime_prompt=runtime_prompt,
        use_real_api=not DEVELOPMENT_MODE,
    )


def validate_provider_output(raw_output: dict) -> InstagramCaptionSchema:
    if FORCE_INVALID_OUTPUT:
        raw_output["hashtags"] = "#esto_deberia_fallar"

    return InstagramCaptionSchema(**raw_output)


def persist_successful_execution(
    brand_id: int,
    prompt_id: int,
    product_data: dict,
    runtime_prompt: str,
    validated_output: InstagramCaptionSchema,
    model_used: str,
    execution_time: float,
    usage: dict,
    cost_usd: float,
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
            json.dumps(validated_output.model_dump()),
            model_used,
            execution_time,
            usage["input_tokens"],
            usage["output_tokens"],
            usage["total_tokens"],
            cost_usd,
            None,
        ),
    )

    conn.commit()
    cur.close()
    conn.close()


def print_success_summary(
    brand_name: str,
    prompt_name: str,
    version: str,
    execution_time: float,
    model_used: str,
    usage: dict,
    cost_usd: float,
    daily_budget_usd: float,
    validated_output: InstagramCaptionSchema,
) -> None:
    print("\n✅ Runtime + Sanitizer + Security Flag Layer OK")

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
            ensure_ascii=False,
        )
    )


def run_generation_pipeline(
    brand_id: int,
    raw_product_data: dict,
) -> dict:
    start_time = time.time()

    brand, prompt = load_runtime_context(brand_id)

    if not brand:
        raise ValueError(f"No existe brand_id={brand_id}")

    if not prompt:
        raise ValueError("No hay prompt activo")

    brand_id, brand_name, brand_config = brand
    prompt_id, prompt_name, version, system_instruction = prompt

    daily_budget_usd = float(
        brand_config.get("daily_budget_usd", 1.0)
    )

    try:
        product_data = sanitize_product_data(raw_product_data)

    except ValueError as error:
        execution_time = round(time.time() - start_time, 2)

        log_security_event(
            brand_id=brand_id,
            prompt_id=prompt_id,
            product_data=raw_product_data,
            runtime_prompt="",
            raw_output_received={
                "error": "injection_attempt",
                "message": str(error),
            },
            model_used="input_sanitizer",
            execution_time=execution_time,
            security_flag="injection_attempt",
        )

        raise

    runtime_prompt = assemble_runtime_prompt(
        system_instruction=system_instruction,
        brand_config=brand_config,
        product_data=product_data,
    )

    try:
        run_budget_guard(
            brand_id=brand_id,
            daily_budget_usd=daily_budget_usd,
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
                "message": (
                    "Execution stopped by budget "
                    "guard before provider call."
                ),
            },
            model_used="budget_guard",
            execution_time=execution_time,
            security_flag="budget_exceeded",
        )

        raise

    provider_response = execute_provider(runtime_prompt)

    raw_output = provider_response["output"]
    usage = provider_response["usage"]
    model_used = provider_response["model_used"]

    try:
        validated_output = validate_provider_output(raw_output)

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
                "validation_error": str(error),
            },
            model_used=model_used,
            execution_time=execution_time,
            security_flag="invalid_output",
        )

        raise

    execution_time = round(time.time() - start_time, 2)

    cost_usd = calculate_cost(
        model_name=model_used,
        input_tokens=usage["input_tokens"],
        output_tokens=usage["output_tokens"],
    )

    persist_successful_execution(
        brand_id=brand_id,
        prompt_id=prompt_id,
        product_data=product_data,
        runtime_prompt=runtime_prompt,
        validated_output=validated_output,
        model_used=model_used,
        execution_time=execution_time,
        usage=usage,
        cost_usd=cost_usd,
    )

    return validated_output.model_dump()


def run_dynamic_runtime(brand_id: int) -> None:
    raw_product_data = get_sample_product_data()

    try:
        output = run_generation_pipeline(
            brand_id=brand_id,
            raw_product_data=raw_product_data,
        )

    except ValueError as error:
        print("\n🛑 Input Sanitizer detenido")
        print(str(error))
        return

    except RuntimeError as error:
        print("\n🛑 Budget Guard detenido")
        print(str(error))
        return

    except ValidationError as error:
        print("\n🛑 Invalid Output detenido")
        print("El output no cumple el schema Pydantic.")
        print(error)
        return

    print("\n✅ Runtime + Sanitizer + Security Flag Layer OK")
    print("\n--- OUTPUT VALIDADO ---")
    print(
        json.dumps(
            output,
            indent=2,
            ensure_ascii=False,
        )
    )