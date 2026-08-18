# Main purpose: manage public publication records and Scopus synchronization writes.

from .common import fetch_all, get_db_connection  # Shared database helpers.

PUBLICATION_FORM_COLUMNS = (
    "title",
    "authors",
    "journal",
    "publication_year",
    "volume",
    "issue",
    "article_number",
    "page",
    "pdf_url",
)

# ===== Table Initialization =====
# These helpers are called before table operations so missing tables do not break the app.
def ensure_publications_table() -> None:
    """Create the publications table if it does not exist."""
    connection = get_db_connection()
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS publications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_order INTEGER NOT NULL DEFAULT 0,
                title TEXT NOT NULL,
                authors TEXT NOT NULL DEFAULT '',
                journal TEXT NOT NULL DEFAULT '',
                publication_year INTEGER,
                volume TEXT NOT NULL DEFAULT '',
                issue TEXT NOT NULL DEFAULT '',
                article_number TEXT NOT NULL DEFAULT '',
                page TEXT NOT NULL DEFAULT '',
                pdf_url TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        ensure_publications_table_columns(connection)
        connection.commit()
    finally:
        connection.close()

def ensure_publications_table_columns(connection) -> None:
    """Add any newer publication columns required by Scopus synchronization."""
    existing_columns = {
        row["name"]
        for row in connection.execute("PRAGMA table_info(publications)").fetchall()
    }

    if "source_type" in existing_columns:
        rebuild_publications_table_without_source_type(connection)
        existing_columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(publications)").fetchall()
        }

    if "scopus_eid" not in existing_columns:
        connection.execute(
            "ALTER TABLE publications ADD COLUMN scopus_eid TEXT NOT NULL DEFAULT ''"
        )
    if "scopus_last_updated_at" not in existing_columns:
        connection.execute(
            "ALTER TABLE publications ADD COLUMN scopus_last_updated_at TEXT"
        )

    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_publications_scopus_eid
        ON publications(scopus_eid)
        """
    )

def rebuild_publications_table_without_source_type(connection) -> None:
    """
    Rebuild the publications table without the deprecated `source_type` column.

    Even though newer SQLite versions support limited column removal, the most
    reliable project-safe path here is to recreate the table and copy the data.
    This keeps existing rows intact while fully removing the old column.
    """
    connection.execute(
        """
        CREATE TABLE publications__new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_order INTEGER NOT NULL DEFAULT 0,
            title TEXT NOT NULL,
            authors TEXT NOT NULL DEFAULT '',
            journal TEXT NOT NULL DEFAULT '',
            publication_year INTEGER,
            volume TEXT NOT NULL DEFAULT '',
            issue TEXT NOT NULL DEFAULT '',
            article_number TEXT NOT NULL DEFAULT '',
            page TEXT NOT NULL DEFAULT '',
            pdf_url TEXT NOT NULL DEFAULT '',
            scopus_eid TEXT NOT NULL DEFAULT '',
            scopus_last_updated_at TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    connection.execute(
        """
        INSERT INTO publications__new (
            id,
            source_order,
            title,
            authors,
            journal,
            publication_year,
            volume,
            issue,
            article_number,
            page,
            pdf_url,
            scopus_eid,
            scopus_last_updated_at,
            created_at,
            updated_at
        )
        SELECT
            id,
            source_order,
            title,
            authors,
            journal,
            publication_year,
            volume,
            issue,
            article_number,
            page,
            pdf_url,
            COALESCE(scopus_eid, ''),
            scopus_last_updated_at,
            created_at,
            updated_at
        FROM publications
        """
    )
    connection.execute("DROP TABLE publications")
    connection.execute("ALTER TABLE publications__new RENAME TO publications")

# ===== Shared Queries for Public Display =====
# Fetch the complete public publication list used across the site.
def get_all_publications():
    ensure_publications_table()
    rows = fetch_all(
        """
        SELECT
            id,
            source_order,
            title,
            authors,
            journal,
            publication_year,
            volume,
            issue,
            article_number,
            page,
            pdf_url
        FROM publications
        ORDER BY source_order ASC, id ASC
        """
    )
    return [dict(row) for row in rows]
def sync_scopus_publications(publications):
    """
    Write the synchronized Scopus publications into the publications table.

    This flow handles more than plain inserts: it refreshes existing Scopus
    records, adopts matching manual records when possible, and keeps the public
    Publications page aligned with the latest synchronized dataset.
    """
    ensure_publications_table()
    connection = get_db_connection()
    inserted_count = 0
    updated_count = 0
    adopted_existing_count = 0

    try:
        connection.execute("BEGIN IMMEDIATE")
        max_source_order_row = connection.execute(
            "SELECT COALESCE(MAX(source_order), 0) AS max_source_order FROM publications"
        ).fetchone()
        next_source_order = int(max_source_order_row["max_source_order"] if max_source_order_row else 0) + 1

        active_eids = []
        seen_eids = set()

        for publication in publications:
            scopus_eid = str(publication.get("scopus_eid", "") or "").strip()
            if not scopus_eid or scopus_eid in seen_eids:
                continue

            seen_eids.add(scopus_eid)
            active_eids.append(scopus_eid)

            payload = {
                column: publication.get(column, "")
                for column in PUBLICATION_FORM_COLUMNS
            }

            existing_row = connection.execute(
                "SELECT id FROM publications WHERE scopus_eid = ? LIMIT 1",
                (scopus_eid,),
            ).fetchone()

            if existing_row:
                assignments = ", ".join(f"{column} = ?" for column in PUBLICATION_FORM_COLUMNS)
                connection.execute(
                    f"""
                    UPDATE publications
                    SET {assignments},
                        scopus_eid = ?,
                        scopus_last_updated_at = DATETIME('now', '+7 hours'),
                        updated_at = DATETIME('now', '+7 hours')
                    WHERE id = ?
                    """,
                    (
                        *(payload[column] for column in PUBLICATION_FORM_COLUMNS),
                        scopus_eid,
                        existing_row["id"],
                    ),
                )
                updated_count += 1
                continue

            duplicate_row = connection.execute(
                """
                SELECT id, pdf_url
                FROM publications
                WHERE LOWER(title) = LOWER(?) OR LOWER(pdf_url) = LOWER(?)
                LIMIT 1
                """,
                (payload["title"], payload["pdf_url"]),
            ).fetchone()
            if duplicate_row:
                existing_url = str(duplicate_row["pdf_url"] or "").strip()
                incoming_url = str(payload["pdf_url"] or "").strip()
                use_existing_url = bool(existing_url) and (
                    not incoming_url
                    or "scopus.com" in incoming_url.lower()
                    or "api.elsevier.com" in incoming_url.lower()
                )
                merged_payload = dict(payload)
                if use_existing_url:
                    merged_payload["pdf_url"] = existing_url

                assignments = ", ".join(f"{column} = ?" for column in PUBLICATION_FORM_COLUMNS)
                connection.execute(
                    f"""
                    UPDATE publications
                    SET {assignments},
                        scopus_eid = ?,
                        scopus_last_updated_at = DATETIME('now', '+7 hours'),
                        updated_at = DATETIME('now', '+7 hours')
                    WHERE id = ?
                    """,
                    (
                        *(merged_payload[column] for column in PUBLICATION_FORM_COLUMNS),
                        scopus_eid,
                        duplicate_row["id"],
                    ),
                )
                adopted_existing_count += 1
                continue

            placeholders = ", ".join("?" for _ in PUBLICATION_FORM_COLUMNS)
            column_sql = ", ".join(PUBLICATION_FORM_COLUMNS)
            connection.execute(
                f"""
                INSERT INTO publications (
                    source_order,
                    {column_sql},
                    scopus_eid,
                    scopus_last_updated_at
                )
                VALUES (?, {placeholders}, ?, DATETIME('now', '+7 hours'))
                """,
                (
                    next_source_order,
                    *(payload[column] for column in PUBLICATION_FORM_COLUMNS),
                    scopus_eid,
                ),
            )
            next_source_order += 1
            inserted_count += 1

        if active_eids:
            placeholders = ", ".join("?" for _ in active_eids)
            connection.execute(
                f"""
                DELETE FROM publications
                WHERE COALESCE(scopus_eid, '') != ''
                  AND scopus_eid NOT IN ({placeholders})
                """,
                tuple(active_eids),
            )

        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return {
        "inserted_count": inserted_count,
        "updated_count": updated_count,
        "adopted_existing_count": adopted_existing_count,
        "active_count": len(active_eids),
    }
