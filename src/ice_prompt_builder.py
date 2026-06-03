OBJECTIVE_PROMPTS = {
    "MAS_VENTAS": (
        "Enfócate en la conversión directa, escasez y los beneficios inmediatos del producto. "
        "El CTA debe invitar a comprar o cotizar ya."
    ),
    "MAS_INTERACCION": (
        "Genera conversación. Termina el caption con una pregunta abierta y orgánica "
        "sobre el producto para que los usuarios comenten."
    ),
    "LANZAR_PRODUCTO": (
        "Genera expectativa y novedad. Resalta que es un nuevo lanzamiento "
        "y explica qué problema viene a resolver."
    ),
    "VISIBILIDAD": (
        "Enfócate en compartir valor, educación o el contexto local de la ciudad. "
        "Haz que el contenido sea altamente compartible."
    ),
}


def build_prompt(
    profile: dict,
    producto: str,
    oferta: str,
    objective: str,
) -> str:
    if objective not in OBJECTIVE_PROMPTS:
        raise ValueError(f"Objective inválido: {objective}")

    objective_instruction = OBJECTIVE_PROMPTS[objective]

    oferta_line = f"Oferta: {oferta}" if oferta else ""

    return f"""
Eres un experto en marketing para pequeños negocios locales hispanohablantes.

Negocio: {profile['nombre_negocio']}
Rubro: {profile['rubro']}
Ciudad: {profile['ciudad']}
Producto: {producto}
{oferta_line}

{objective_instruction}

Responde ÚNICAMENTE con JSON:
{{
  "caption": "texto 80-250 palabras mencionando explícitamente el producto",
  "hashtags": ["hashtag1", "..."],
  "cta": "un llamado a la acción"
}}
""".strip()