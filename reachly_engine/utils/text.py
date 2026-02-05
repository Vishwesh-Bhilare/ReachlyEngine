import re


def normalize_text(text: str) -> str:
    """
    Normalize whitespace and line breaks.
    """
    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def safe_snippet(text: str, max_chars: int = 500) -> str:
    """
    Extract a clean snippet for previews or logs.
    """
    if not text:
        return ""

    if len(text) <= max_chars:
        return text

    return text[:max_chars].rsplit(" ", 1)[0] + "..."

