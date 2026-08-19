# Main purpose: manage the single administrator account and its login credentials.

from .common import fetch_one, get_db_connection  # Shared database helper functions.


# Create the administrator login table.
def ensure_auth_tables():
    connection = get_db_connection()
    try:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_id INTEGER UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (staff_id) REFERENCES staff(id) ON DELETE SET NULL
            );
            """
        )

        connection.commit()
    finally:
        connection.close()


# Fetch one administrator record by username.
def get_user_by_username(username):
    return fetch_one(
        "SELECT * FROM users WHERE username = ?",
        (username,),
    )


# Fetch one administrator record by primary-key id.
def get_user_by_id(user_id):
    return fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))


# Update the target administrator username and password hash.
def update_user_credentials(user_id, username, password_hash):
    connection = get_db_connection()
    try:
        connection.execute(
            """
            UPDATE users
            SET username = ?, password_hash = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (username, password_hash, user_id),
        )
        connection.commit()
    finally:
        connection.close()
