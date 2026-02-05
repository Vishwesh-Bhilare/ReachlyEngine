import sqlite3
from pathlib import Path
from typing import Optional, Dict

from reachly_engine.config import DB_PATH
from reachly_engine.logger import get_logger

logger = get_logger("memory_store")


class MemoryStore:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._ensure_db()

    def _ensure_db(self):
        if not self.db_path.exists():
            self._init_schema()

    def _init_schema(self):
        schema_path = Path(__file__).parent / "schema.sql"
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(schema_path.read_text())

    # ---------- Prospects ----------

    def save_prospect(
        self,
        *,
        name,
        role,
        company,
        industry,
        seniority,
        summary,
        style,
        raw_profile,
        source,
    ) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO prospects
                (name, role, company, industry, seniority, summary, style, raw_profile, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    role,
                    company,
                    industry,
                    seniority,
                    summary,
                    style,
                    raw_profile,
                    source,
                ),
            )
            conn.commit()
            return cur.lastrowid

    def list_prospects(self) -> list[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT id, name, role, company, industry, created_at
                FROM prospects
                ORDER BY created_at DESC
                """
            ).fetchall()

        return [dict(row) for row in rows]

    def get_prospect(self, prospect_id: int) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM prospects WHERE id = ?",
                (prospect_id,),
            ).fetchone()

        return dict(row) if row else None

    # ---------- Messages ----------

    def save_message(self, prospect_id: int, channel: str, content: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO messages (prospect_id, channel, content)
                VALUES (?, ?, ?)
                """,
                (prospect_id, channel, content),
            )
            conn.commit()

