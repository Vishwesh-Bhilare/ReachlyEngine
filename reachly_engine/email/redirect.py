import webbrowser
import urllib.parse
from reachly_engine.logger import get_logger

logger = get_logger("email_redirect")


def open_gmail_compose(
    *,
    to: str = "",
    subject: str,
    body: str,
):
    """
    Opens Gmail compose window in browser with pre-filled content.
    """

    base_url = "https://mail.google.com/mail/?view=cm&fs=1"

    params = {
        "to": to,
        "su": subject,
        "body": body,
    }

    encoded = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

    url = f"{base_url}&{encoded}"

    logger.info("Opening Gmail compose window")
    webbrowser.open(url)

