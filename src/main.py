import json
import time

from validators import InstagramCaptionSchema


def run_pure_runtime_loop():
    print("AI Operational Middleware — Sprint 0A")
    print("Iniciando runtime local...")

    start_time = time.time()

    product_data = {
        "name": "Ficus Lyrata",
        "details": "Hojas grandes premium."
    }

    mock_output = {
        "caption": f"La magia botánica del {product_data['name']} ya está aquí. Ideal para tu rincón favorito.",
        "hashtags": ["plantparents", "urbanjungle", "plantasmagicas"],
        "cta": "Visita el link en nuestra bio."
    }

    validated_output = InstagramCaptionSchema(**mock_output)

    execution_time = round(time.time() - start_time, 2)

    print("\nOUTPUT VALIDADO:")
    print(json.dumps(validated_output.model_dump(), indent=2, ensure_ascii=False))
    print(f"\nTiempo de ejecución: {execution_time}s")


if __name__ == "__main__":
    run_pure_runtime_loop()