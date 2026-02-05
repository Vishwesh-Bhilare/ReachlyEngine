import json
from pathlib import Path
from datetime import datetime, timezone


AUTH_DIR = Path.home() / ".reachly"
CRED_FILE = AUTH_DIR / "credentials.json"


def _ensure_dir():
    AUTH_DIR.mkdir(parents=True, exist_ok=True)


def save_linkedin_cookie(li_at: str):
    _ensure_dir()
    data = {
        "linkedin": {
            "li_at": li_at.strip(),
            "added_at": datetime.now(timezone.utc).isoformat(),
        }
    }
    CRED_FILE.write_text(json.dumps(data, indent=2))


def load_linkedin_cookie() -> str | None:
    if not CRED_FILE.exists():
        return None

    try:
        data = json.loads(CRED_FILE.read_text())
        return data.get("linkedin", {}).get("li_at")
    except Exception:
        return None


def clear_credentials():
    if CRED_FILE.exists():
        CRED_FILE.unlink()

