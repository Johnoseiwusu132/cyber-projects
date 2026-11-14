"""Load transformed records into PostgreSQL."""

import logging

import psycopg2
from psycopg2.extras import execute_batch

logger = logging.getLogger(__name__)

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id);
"""

UPSERT_SQL = """
INSERT INTO posts (id, user_id, title, body)
VALUES (%(id)s, %(user_id)s, %(title)s, %(body)s)
ON CONFLICT (id) DO UPDATE SET
    user_id = EXCLUDED.user_id,
    title = EXCLUDED.title,
    body = EXCLUDED.body,
    loaded_at = CURRENT_TIMESTAMP;
"""


def load_posts(records: list[dict], db_config: dict) -> int:
    """Create the destination table and upsert records in one transaction."""
    if not records:
        logger.warning("No valid records to load.")
        return 0

    connection = psycopg2.connect(**db_config)
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_TABLE_SQL)
                execute_batch(cursor, UPSERT_SQL, records, page_size=100)
        logger.info("Loaded or updated %d records", len(records))
        return len(records)
    finally:
        connection.close()
