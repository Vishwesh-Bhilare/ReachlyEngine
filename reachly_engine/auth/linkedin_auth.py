import webbrowser
import requests
from rich.console import Console

from reachly_engine.auth.store import save_linkedin_cookie
from reachly_engine.config import USER_AGENT

console = Console()


def authenticate_linkedin():
    console.print(
        "\n[bold]LinkedIn authentication required (one-time).[/bold]\n"
        "A browser window will open.\n\n"
        "Steps:\n"
        "1. Log in to LinkedIn normally\n"
        "2. Open DevTools → Application → Cookies\n"
        "3. Select https://www.linkedin.com\n"
        "4. Copy the value of the cookie named [bold]li_at[/bold]\n"
    )

    webbrowser.open("https://www.linkedin.com/login")

    li_at = console.input("\nPaste li_at cookie here: ").strip()
    if not li_at:
        raise RuntimeError("No cookie provided.")

    # Validate cookie
    headers = {
        "User-Agent": USER_AGENT,
        "Cookie": f"li_at={li_at}",
    }

    resp = requests.get(
        "https://www.linkedin.com/feed/",
        headers=headers,
        timeout=15,
    )

    if resp.status_code != 200 or "feed" not in resp.text.lower():
        raise RuntimeError("Invalid or expired LinkedIn cookie.")

    save_linkedin_cookie(li_at)
    console.print("[green]LinkedIn authentication successful.[/green]")

