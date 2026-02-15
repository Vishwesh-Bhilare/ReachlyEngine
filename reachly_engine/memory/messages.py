import sqlite3
from reachly_engine.config import DB_PATH


def get_messages_for_prospect(prospect_id: int) -> dict:
    """
    Returns latest message per channel.
    """
    query = """
        SELECT channel, content
        FROM messages
        WHERE prospect_id = ?
        ORDER BY created_at DESC
    """

    messages = {}

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(query, (prospect_id,)).fetchall()

    for channel, content in rows:
        if channel not in messages:
            messages[channel] = content

    return messages

