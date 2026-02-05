import sqlite3
from typing import List, Dict

from reachly_engine.config import DB_PATH
from reachly_engine.logger import get_logger

logger = get_logger("memory_retrieval")


def find_similar_prospects(
    *,
    industry: str | None = None,
    role: str | None = None,
    limit: int = 3,
) -> List[Dict]:
    """
    Lightweight similarity based on industry + role overlap.
    Deterministic, fast, offline.
    """

    conditions = []
    params = []

    if industry:
        conditions.append("industry = ?")
        params.append(industry)

    if role:
        conditions.append("role = ?")
        params.append(role)

    if not conditions:
        return []

    where_clause = " OR ".join(conditions)

    query = f"""
        SELECT id, name, role, company, industry, summary
        FROM prospects
        WHERE {where_clause}
        ORDER BY created_at DESC
        LIMIT ?
    """

    params.append(limit)

    logger.info("Retrieving similar prospects")

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(query, params).fetchall()

    return [dict(row) for row in rows]

