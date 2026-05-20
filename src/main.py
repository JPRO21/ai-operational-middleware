import os
import time
import json
from dotenv import load_dotenv
from validators import InstagramCaptionSchema

load_dotenv()

def run_pure_runtime_loop(brand_name: str, product_data: dict):
    print(f"🚀 [Sprint 0A] Iniciando bucle local para: {brand_name}")
    start_time = time.time()
    
    # 1. MOCK DE CONTEXTO (Simulando lo que vendrá de la DB en el Sprint 0B)
    brand_config_mock = {
        "tone": "místico y cercano",
        "forbidden_words": ["barato", "oferta"],
        "cta_default": "Visita el link en nuestra bio."
    }
    system_instruction_mock = "Eres un experto en contenido. Genera un JSON que cumpla el esquema requerido."
    
    # 2. PROMPT ASSEMBLY
    print("🧠 [Prompt Assembly] Juntando piezas de texto...")
    runtime_prompt = f"""
    System: {system_instruction_mock}
    Config: {json.dumps(brand_config_mock)}
    Input: {json.dumps(product_data)}
    """
    
    # 3. MOCK OUTPUT (Simulando la respuesta del LLM sin gastar API)
    print("🤖 [LLM Runtime] Generando respuesta simulada (Mock)...")
    time.sleep(0.5) # Simula latencia
    
    mock_llm_string = json.dumps({
        "caption": f"La magia botánica del {product_data['name']} ya está aquí. Ideal para tu rincón favorito.",
        "hashtags": ["plantparents", "urbanjungle"],
        "cta": brand_config_mock["cta_default"]
    })
    
    # 4. VALIDACIÓN CON PYDANTIC
    print("🛡️ [Validation Layer] Validando contra el esquema estricto...")
    try:
        parsed_data = json.loads(mock_llm_string)
        validated_output = InstagramCaptionSchema(**parsed_data)
        print("✅ [Validation Layer] Estructura perfecta.")
    except Exception as e:
        print(f"❌ [Validation Layer] Falló la estructura: {e}")
        return

    # 5. SALIDA POR CONSOLA
    execution_time = round(time.time() - start_time, 2)
    print("\n✨ --- OUTPUT EN CONSOLA (PROYECTO VIVO) --- ✨")
    print(f"Tiempo de cómputo: {execution_time}s")
    print(json.dumps(validated_output.model_dump(), indent=2, ensure_ascii=False))
    print("---------------------------------------------\n")

if __name__ == "__main__":
    input_test = {"name": "Ficus Lyrata", "details": "Hojas grandes premium."}
    run_pure_runtime_loop("Plantas Mágicas", input_test)