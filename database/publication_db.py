# Main purpose: manage public publication records and the Scopus synchronization write flow.

from .common import fetch_all, get_db_connection  # Shared database helper functions.


# Frontend publication fields actually used by the public Publications page.
# The Scopus sync flow reshapes incoming publication data into this stable column set before writing to SQLite.
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
# Run these helpers before table operations so the app does not break when the table is missing.
# Create the publications table if it does not exist.
def ensure_publications_table() -> None:
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


# Add newer publication columns required by the Scopus sync flow.
def ensure_publications_table_columns(connection) -> None:
    existing_columns = {
        row["name"]
        for row in connection.execute("PRAGMA table_info(publications)").fetchall()
    }

    if "scopus_eid" not in existing_columns:
        connection.execute(
            "ALTER TABLE publications ADD COLUMN scopus_eid TEXT NOT NULL DEFAULT ''"
        )

    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_publications_scopus_eid
        ON publications(scopus_eid)
        """
    )

    if "scopus_last_updated_at" in existing_columns:
        rebuild_publications_table_without_scopus_timestamp(connection)


# Rebuild the publications table to remove the old scopus_last_updated_at column.
def rebuild_publications_table_without_scopus_timestamp(connection) -> None:
    connection.execute("DROP TABLE IF EXISTS publications__new")
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
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            scopus_eid TEXT NOT NULL DEFAULT ''
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
            created_at,
            updated_at,
            scopus_eid
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
            created_at,
            updated_at,
            COALESCE(scopus_eid, '')
        FROM publications
        """
    )
    connection.execute("DROP TABLE publications")
    connection.execute("ALTER TABLE publications__new RENAME TO publications")
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_publications_scopus_eid
        ON publications(scopus_eid)
        """
    )


# ===== Shared Queries for the Public Site =====
# Fetch the complete public publication list.
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


#
#     Write the synchronized Scopus publication list back into the publications table.
#
#     This function handles more than just inserts:
#     1. Refresh existing rows with the same scopus_eid
#     2. Adopt older manually imported rows when they are actually the same paper
#     3. Remove outdated Scopus-managed rows that no longer appear in the latest sync result
#
#     This keeps the public Publications page consistent:
#     - each paper appears only once
#     - older rows can be taken over by official Scopus identifiers
#     - the database does not retain stale synchronized publications
#     
def sync_scopus_publications(publications):
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
            # Every publication must have scopus_eid because it is the core key for sync deduping and refreshes.
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
                # If the same scopus_eid already exists, it is the same paper, so refresh the record in place.
                assignments = ", ".join(f"{column} = ?" for column in PUBLICATION_FORM_COLUMNS)
                connection.execute(
                    f"""
                    UPDATE publications
                    SET {assignments},
                        scopus_eid = ?,
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
                # If the EID is new but the title or URL already matches,
                # this is usually an older manually imported row now being adopted by Scopus.
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
                    updated_at
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
            # After this sync, any row that still has scopus_eid but is missing from active_eids
            # no longer belongs to the current sync result and should be removed for consistency.
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
