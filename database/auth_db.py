# Main purpose: manage the single administrator account and the must-change-password state.

import os
import sqlite3
from werkzeug.security import generate_password_hash
from .common import fetch_one, get_db_connection

def get_default_admin_username() -> str:
    """Read the default administrator username from the environment or use the built-in fallback."""
    return os.environ.get("DEFAULT_ADMIN_USERNAME", "SCEM_admin").strip() or "SCEM_admin"

def get_default_admin_password() -> str:
    """Read the default administrator password from the environment or use the built-in fallback."""
    return os.environ.get("DEFAULT_ADMIN_PASSWORD", "realjanjjI_0807").strip() or "realjanjjI_0807"

def ensure_auth_tables():
    """Create the administrator login table and seed the default admin account when necessary."""
    connection = get_db_connection()
    try:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_id INTEGER UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                must_change_credentials INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (staff_id) REFERENCES staff(id) ON DELETE SET NULL
            );
            """
        )

        ensure_users_table_columns(connection)

        admin_exists = connection.execute(
            "SELECT id FROM users LIMIT 1"
        ).fetchone()
        if admin_exists is None:
            connection.execute(
                """
                INSERT INTO users
                    (username, password_hash, must_change_credentials)
                VALUES (?, ?, 1)
                """,
                (get_default_admin_username(), generate_password_hash(get_default_admin_password())),
            )

        connection.commit()
    finally:
        connection.close()

def ensure_users_table_columns(connection) -> None:
    """Upgrade the legacy users table to the current single-administrator schema when needed."""
    existing_columns = {
        row["name"]
        for row in connection.execute("PRAGMA table_info(users)").fetchall()
    }

    if "role" in existing_columns:
        rebuild_users_table_without_role(connection)

def rebuild_users_table_without_role(connection) -> None:
    """Rebuild the legacy role-based users table into the single-admin version."""
    admin_row = connection.execute(
        """
        SELECT id, staff_id, username, password_hash,
               must_change_credentials, created_at, updated_at
        FROM users
        WHERE role = 'admin'
        ORDER BY id ASC
        LIMIT 1
        """
    ).fetchone()

    connection.execute(
        """
        CREATE TABLE users__new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id INTEGER UNIQUE,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            must_change_credentials INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (staff_id) REFERENCES staff(id) ON DELETE SET NULL
        )
        """
    )

    if admin_row is not None:
        connection.execute(
            """
            INSERT INTO users__new (
                id, staff_id, username, password_hash,
                must_change_credentials, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                admin_row["id"],
                admin_row["staff_id"],
                admin_row["username"],
                admin_row["password_hash"],
                admin_row["must_change_credentials"],
                admin_row["created_at"],
                admin_row["updated_at"],
            ),
        )

    connection.execute("DROP TABLE users")
    connection.execute("ALTER TABLE users__new RENAME TO users")

def get_user_by_username(username):
    """Fetch one administrator record by username."""
    return fetch_one(
        "SELECT * FROM users WHERE username = ?",
        (username,),
    )

def get_user_by_id(user_id):
    """Fetch one administrator record by primary-key id."""
    return fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))

def update_user_credentials(user_id, username, password_hash):
    """Update the target user's username, password hash, and first-login status."""
    connection = get_db_connection()
    try:
        connection.execute(
            """
            UPDATE users
            SET username = ?, password_hash = ?, must_change_credentials = 0,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (username, password_hash, user_id),
        )
        connection.commit()
    finally:
        connection.close()

def reset_admin_credentials(user_id):
    """Reset the administrator to the default credentials and require reconfiguration on the next login."""
    connection = get_db_connection()
    try:
        try:
            cursor = connection.execute(
                """
                UPDATE users
                SET username = ?, password_hash = ?, must_change_credentials = 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    get_default_admin_username(),
                    generate_password_hash(get_default_admin_password()),
                    user_id,
                ),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            connection.rollback()
            return None

        return get_default_admin_username() if cursor.rowcount == 1 else None
    finally:
        connection.close()
