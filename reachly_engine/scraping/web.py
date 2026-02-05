import requests

from reachly_engine.config import USER_AGENT
from reachly_engine.logger import get_logger
from reachly_engine.scraping.cleaner import clean_html, aggressive_cleanup

logger = get_logger("web_scraper")


def fetch_web_text(url: str, timeout: int = 20) -> str:
    headers = {
        "User-Agent": USER_AGENT,
    }

    logger.info(f"Fetching web page: {url}")

    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        raise RuntimeError(f"Failed to fetch URL: {url}") from e

    cleaned = clean_html(resp.text)
    return aggressive_cleanup(cleaned)

