from typing import Any


def normalize_input(raw_product_data: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(raw_product_data)

    if "name" in normalized and isinstance(normalized["name"], str):
        normalized["name"] = " ".join(
            normalized["name"].strip().split()
        ).title()

    if "details" in normalized and isinstance(
        normalized["details"],
        str,
    ):
        details = " ".join(
            normalized["details"].strip().split()
        )

        normalized["details"] = (
            details[:1].upper() + details[1:]
            if details
            else details
        )

    return normalized


def semantic_sanity_check(
    product_data: dict[str, Any],
) -> dict[str, Any]:

    issues: list[str] = []

    name = str(
        product_data.get("name", "")
    ).strip().lower()

    details = str(
        product_data.get("details", "")
    ).strip().lower()

    suspicious_terms = [
        "caca",
        "asdf",
        "xxx",
        "test",
    ]

    vowels = "aeiouáéíóú"

    if not name:
        issues.append("Missing product name")

    elif len(name) < 4:
        issues.append("Product name too short")

    for term in suspicious_terms:
        if term in name or term in details:
            issues.append(
                f"Suspicious term detected: {term}"
            )

    vowel_count = sum(
        1 for char in name if char in vowels
    )

    if len(name) > 5 and vowel_count <= 1:
        issues.append(
            "Low semantic confidence in product name"
        )

    if len(details) < 10:
        issues.append("Product details too short")

    score = max(
        0.0,
        1.0 - (0.25 * len(issues))
    )

    return {
        "passed": len(issues) == 0,
        "score": round(score, 2),
        "issues": issues,
    }


def brand_protection_check(
    output_data: dict[str, Any],
    brand_config: dict[str, Any],
) -> dict[str, Any]:

    issues: list[str] = []

    caption = str(
        output_data.get("caption", "")
    )

    cta = str(
        output_data.get("cta", "")
    )

    full_text = f"{caption} {cta}".lower()

    forbidden_words = brand_config.get(
        "forbidden_words",
        [],
    )

    for word in forbidden_words:
        if str(word).lower() in full_text:
            issues.append(
                f"Forbidden word detected: {word}"
            )

    expected_cta = brand_config.get(
        "cta_default"
    )

    if not cta:
        issues.append("Missing CTA")

    elif (
        expected_cta
        and cta.strip() != str(expected_cta).strip()
    ):
        issues.append(
            "CTA does not match brand default"
        )

    score = max(
        0.0,
        1.0 - (0.25 * len(issues))
    )

    return {
        "passed": len(issues) == 0,
        "score": round(score, 2),
        "issues": issues,
    }


def output_qa_check(
    output_data: dict[str, Any],
) -> dict[str, Any]:

    issues: list[str] = []

    caption = str(
        output_data.get("caption", "")
    )

    hashtags = output_data.get(
        "hashtags",
        [],
    )

    cta = str(
        output_data.get("cta", "")
    )

    tone_check = str(
        output_data.get("tone_check", "")
    )

    if len(caption.strip()) < 80:
        issues.append("Caption too short")

    if (
        not isinstance(hashtags, list)
        or len(hashtags) < 3
    ):
        issues.append("Not enough hashtags")

    if not cta.strip():
        issues.append("Missing CTA")

    if not tone_check.strip():
        issues.append("Missing tone_check")

    confidence_score = max(
        0.0,
        1.0 - (0.20 * len(issues))
    )

    return {
        "passed": len(issues) == 0,
        "confidence_score": round(
            confidence_score,
            2,
        ),
        "issues": issues,
    }