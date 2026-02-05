import re
from bs4 import BeautifulSoup


def clean_html(html: str) -> str:
    if not html:
        return ""

    soup = BeautifulSoup(html, "lxml")

    # Remove scripts, styles, and hidden junk
    for tag in soup(["script", "style", "noscript", "svg", "img", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    # Normalize whitespace
    text = re.sub(r"\n{2,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def aggressive_cleanup(text: str) -> str:
    """
    Remove obvious LinkedIn / web UI noise.
    """
    if not text:
        return ""

    noise_patterns = [
        r"Sign in.*",
        r"Join LinkedIn.*",
        r"LinkedIn Member",
        r"See more",
        r"Show less",
        r"Followers?\s*\d+",
        r"Connections?\s*\d+",
        r"Message",
        r"Connect",
    ]

    for pattern in noise_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    # Final whitespace cleanup
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()

