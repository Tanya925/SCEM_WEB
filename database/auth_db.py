# 主要用途：管理單一管理員帳號及其登入憑證。

from .common import fetch_one, get_db_connection

INITIAL_ADMIN_USERNAME_PARTS = ("SCEM", "_", "admin")
INITIAL_ADMIN_PASSWORD_HASH = (
    "scrypt:32768:8:1$SMIUhVLv9uwUwv94$"
    "b1778aff41f12e8cae8429a01e800e3bcd638fbd708a44fdd5c74ce074e1e075"
    "c592891f86abce74af155edbe96fd4a8a4261c7d20f3d9d4e90f05b23c475266"
)

def get_initial_admin_username() -> str:
    """建立首次初始化帳號時使用的管理員預設帳號名稱。"""
    return "".join(INITIAL_ADMIN_USERNAME_PARTS)

def ensure_auth_tables():
    """建立管理員登入資料表，並在需要時建立預設管理員帳號。"""
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

        admin_exists = connection.execute(
            "SELECT id FROM users LIMIT 1"
        ).fetchone()
        if admin_exists is None:
            connection.execute(
                """
                INSERT INTO users (username, password_hash)
                VALUES (?, ?)
                """,
                (get_initial_admin_username(), INITIAL_ADMIN_PASSWORD_HASH),
            )

        connection.commit()
    finally:
        connection.close()

def get_user_by_username(username):
    """依帳號名稱取得單一管理員資料。"""
    return fetch_one(
        "SELECT * FROM users WHERE username = ?",
        (username,),
    )

def get_user_by_id(user_id):
    """依主鍵 id 取得單一管理員資料。"""
    return fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))

def update_user_credentials(user_id, username, password_hash):
    """更新指定管理員的帳號名稱與密碼雜湊值。"""
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

