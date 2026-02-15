import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

# --------------------
# Base Paths
# --------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.getenv("REACHLY_DATA_DIR", BASE_DIR / "data"))

PROFILES_DIR = DATA_DIR / "profiles"
SUMMARIES_DIR = DATA_DIR / "summaries"
MESSAGES_DIR = DATA_DIR / "messages"
DB_PATH = DATA_DIR / "memory.db"

# Ensure directories exist
for p in [DATA_DIR, PROFILES_DIR, SUMMARIES_DIR, MESSAGES_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# --------------------
# Ollama Configuration
# --------------------
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = "llama3:latest"
#os.getenv("OLLAMA_MODEL", "mistral:7b-instruct-q4_K_M")

OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

# --------------------
# Scraping
# --------------------
USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0"
)

LINKEDIN_COOKIE = os.getenv("LINKEDIN_COOKIE")  # optional

# --------------------
# LLM Limits
# --------------------
MAX_PROFILE_CHARS = 12000
MAX_CONTEXT_CHARS = 8000

# --------------------
# Logging
# --------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# --------------------
# Auth
# --------------------
AUTH_DIR = Path.home() / ".reachly"

