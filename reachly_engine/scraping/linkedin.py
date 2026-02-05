import re
import requests
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from reachly_engine.auth.store import load_linkedin_cookie

from reachly_engine.config import (
    USER_AGENT,
    LINKEDIN_COOKIE,
    PROFILES_DIR,
    MAX_PROFILE_CHARS,
)
from reachly_engine.logger import get_logger
from reachly_engine.scraping.cleaner import clean_html, aggressive_cleanup

logger = get_logger("linkedin_scraper")


from reachly_engine.auth.store import load_linkedin_cookie

def _build_headers() -> dict:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept-Language": "en-US,en;q=0.9",
    }

    li_at = load_linkedin_cookie()
    if li_at:
        headers["Cookie"] = f"li_at={li_at}"

    return headers



def fetch_linkedin_profile_text(url: str) -> str:
    headers = _build_headers()
    logger.info(f"Fetching LinkedIn profile: {url}")

    try:
        resp = requests.get(url, headers=headers, timeout=25)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"LinkedIn fetch failed: {e}")
        raise RuntimeError("Failed to fetch LinkedIn profile") from e

    html = resp.text

    # --- IMPORTANT ---
    # LinkedIn stores profile data inside JSON in <script> tags.
    # We must NOT remove scripts here.
    soup = BeautifulSoup(html, "lxml")

    texts = []

    # 1. Visible text
    texts.append(soup.get_text(separator="\n"))

    # 2. Script JSON payloads (critical)
    for script in soup.find_all("script"):
        content = script.string or ""

        if (
            "profile" in content.lower()
            or "experience" in content.lower()
            or "education" in content.lower()
            or "firstname" in content.lower()
            or "lastname" in content.lower()
        ):
            texts.append(content)


    combined_text = "\n\n".join(texts)

    # Light cleanup only
    combined_text = re.sub(r"\n{3,}", "\n\n", combined_text)
    combined_text = combined_text.strip()

    if len(combined_text) > MAX_PROFILE_CHARS:
        combined_text = combined_text[:MAX_PROFILE_CHARS] + "\n\n[TRUNCATED]"

    return combined_text



def save_profile_text(text: str, source: str = "linkedin") -> Path:
    """
    Persist raw profile text for traceability.
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{source}_{timestamp}.txt"
    path = PROFILES_DIR / filename

    path.write_text(text, encoding="utf-8")

    logger.info(f"Profile text saved: {path}")
    return path

