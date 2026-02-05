import math

# Rough but safe heuristic for Mistral-family models
# ~4 characters per token is conservative
CHARS_PER_TOKEN = 4


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return math.ceil(len(text) / CHARS_PER_TOKEN)


def truncate_to_tokens(text: str, max_tokens: int) -> str:
    if not text:
        return ""

    max_chars = max_tokens * CHARS_PER_TOKEN
    if len(text) <= max_chars:
        return text

    return text[:max_chars].rsplit(" ", 1)[0] + "\n\n[TRUNCATED]"

