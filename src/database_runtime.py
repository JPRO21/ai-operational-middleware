import json

from config.database import get_db_connection
from config.settings import (
    DAILY_BUDGET_USD,
    OPENAI_PRICING,
)


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
        SELECT input_price_per_1k, output_price_per_1k
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

    input_price_per_1k, output_price_per_1k = pricing

    cost = (input_tokens / 1000) * float(input_price_per_1k) + (output_tokens / 1000) * float(output_price_per_1k)

    return round(cost, 6)
