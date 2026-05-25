def sanitize_input(raw_input: str, max_length: int = 500) -> str:
    text = raw_input[:max_length]

    injection_patterns = [
        "ignore",
        "ignora",
        "forget",
        "olvida",
        "system prompt",
        "instrucciones anteriores",
        "previous instructions",
        "disregard",
        "override",
    ]

    text_lower = text.lower()

    for pattern in injection_patterns:
        if pattern in text_lower:
            raise ValueError(f"Input rechazado: patrón sospechoso '{pattern}'")

    return text