import os
import time

from psycopg import OperationalError, connect


DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "app_db"),
    "user": os.getenv("POSTGRES_USER", "app_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "app_password"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}


def wait_for_database(retries: int = 15, delay_seconds: int = 2):
    for attempt in range(1, retries + 1):
        try:
            return connect(**DB_CONFIG)
        except OperationalError as exc:
            if attempt == retries:
                raise RuntimeError("Database did not become ready in time") from exc
            print(f"Database not ready yet (attempt {attempt}/{retries}). Retrying...")
            time.sleep(delay_seconds)


def main():
    with wait_for_database() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    message TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
            cur.execute(
                "INSERT INTO notes (message) VALUES (%s) RETURNING id, message, created_at",
                ("Hello from local Postgres in Docker",),
            )
            inserted_row = cur.fetchone()

            cur.execute(
                "SELECT id, message, created_at FROM notes ORDER BY id DESC LIMIT 5"
            )
            rows = cur.fetchall()

        conn.commit()

    print("Inserted row:")
    print(inserted_row)
    print("\nLatest rows:")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()