# Initialize the SCEM SQLite database, admin account, and initial Scopus data.

from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.auth_db import upsert_admin_user
from database.common import DATABASE_PATH, get_db_connection
from services.scopus_sync_service import ScopusSyncError, sync_scopus_dataset

SCHEMA_PATH = PROJECT_ROOT / "schema.sql"
ENV_PATH = PROJECT_ROOT / ".env"
REQUIRED_CORE_TABLES = {
    "general_info",
    "home_activity_images",
    "research_projects",
    "staff",
}


def load_environment() -> tuple[str, str]:
    load_dotenv(ENV_PATH)

    from os import environ

    admin_user = environ.get("ADMIN_USER", "").strip()
    admin_password = environ.get("ADMIN_PASSWORD", "").strip()

    if not admin_user:
        raise RuntimeError("ADMIN_USER is required in .env before running init_db/seed.py.")

    if not admin_password:
        raise RuntimeError("ADMIN_PASSWORD is required in .env before running init_db/seed.py.")

    return admin_user, admin_password


def existing_tables() -> set[str]:
    if not DATABASE_PATH.exists():
        return set()

    connection = get_db_connection()
    try:
        return {
            row["name"]
            for row in connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
                """
            ).fetchall()
        }
    finally:
        connection.close()


def initialize_database_if_needed() -> bool:
    tables = existing_tables()
    if not tables:
        schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
        connection = get_db_connection()
        try:
            connection.executescript(schema_sql)
            connection.commit()
        finally:
            connection.close()
        return True

    if REQUIRED_CORE_TABLES.issubset(tables):
        return False

    missing_tables = ", ".join(sorted(REQUIRED_CORE_TABLES - tables))
    raise RuntimeError(
        "The database file already exists but is missing required core tables: "
        f"{missing_tables}. Remove the file or repair it before rerunning the seed script."
    )

def sync_admin_credentials(admin_user: str, admin_password: str) -> int:
    password_hash = generate_password_hash(admin_password)
    return upsert_admin_user(admin_user, password_hash)


def run_scopus_sync() -> dict:
    return sync_scopus_dataset()


def print_scopus_summary(sync_result: dict) -> None:
    publication_summary = sync_result["publication_summary"]
    print("Scopus sync finished.")
    print(f"- Staff processed: {sync_result['staff_count']}")
    print(f"- H-index updated: {sync_result['hindex_updated_count']}")
    print(f"- Publications active: {publication_summary['active_count']}")
    print(f"- Publications inserted: {publication_summary['inserted_count']}")
    print(f"- Publications refreshed: {publication_summary['updated_count']}")
    print(f"- Existing publications adopted: {publication_summary['adopted_existing_count']}")

    if sync_result["errors"]:
        print("- Staff-level errors:")
        for error in sync_result["errors"]:
            print(f"  * {error}")


def main() -> int:
    try:
        admin_user, admin_password = load_environment()
        database_created = initialize_database_if_needed()
        admin_user_id = sync_admin_credentials(admin_user, admin_password)

        print(
            "Database initialized from schema.sql."
            if database_created
            else "Database already exists. Core data was left in place."
        )
        print(f"Admin account is ready for username: {admin_user} (user id: {admin_user_id})")

        sync_result = run_scopus_sync()
        print_scopus_summary(sync_result)
        return 0
    except ScopusSyncError as error:
        print(f"Scopus sync failed: {error}")
        return 1
    except Exception as error:
        print(f"Seed failed: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
