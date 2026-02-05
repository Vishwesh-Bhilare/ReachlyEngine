import sys
from pathlib import Path
import sqlite3

# --- ensure project root is on PYTHONPATH ---
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
# -------------------------------------------

from reachly_engine.config import DB_PATH
from reachly_engine.logger import get_logger

logger = get_logger("init_db")


def main():
    schema_path = (
        ROOT_DIR
        / "reachly_engine"
        / "memory"
        / "schema.sql"
    )

    if not schema_path.exists():
        raise RuntimeError("schema.sql not found")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(schema_path.read_text())

    logger.info(f"Memory DB initialized at: {DB_PATH}")


if __name__ == "__main__":
    main()

