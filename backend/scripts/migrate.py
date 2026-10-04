"""Apply app/schema.sql to the database in DATABASE_URL.  Run: python -m scripts.migrate"""
from pathlib import Path

import psycopg

from app.config import settings

SCHEMA = Path(__file__).resolve().parent.parent / "app" / "schema.sql"


def main() -> None:
    sql = SCHEMA.read_text()
    with psycopg.connect(settings.database_url) as conn:
        conn.execute(sql)
    print("Schema applied.")


if __name__ == "__main__":
    main()
