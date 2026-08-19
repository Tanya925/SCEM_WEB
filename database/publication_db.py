# 主要用途：管理前台公開論文資料，以及 Scopus 同步寫入流程。


from .common import fetch_all, get_db_connection  # 共用資料庫輔助函式。


# 論文資料表中，前台論文頁實際使用的欄位。
# Scopus 同步流程會把抓回來的論文資料整理成這組固定欄位後再寫入 SQLite。
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

# ===== 資料表初始化 =====
# 這些函式會在操作資料表前先執行，避免資料表不存在時讓網站出錯。
def ensure_publications_table() -> None:
    """如果 publications 資料表不存在，就先建立它。"""
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
    """補上 Scopus 同步流程需要的較新論文欄位。"""
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


# ===== 前台共用查詢 =====
# 取得整個網站前台共用的完整論文列表。
def get_all_publications():
    """取得前台使用的完整公開論文列表。"""
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
    將 Scopus 同步回來的論文清單寫回 publications 表。

    這個函式的重點不只是「新增」資料，還包含三種情況：
    1. 同 scopus_eid 的既有論文：直接更新
    2. 舊手動資料但其實是同一篇論文：接管那一筆舊資料並補上 scopus_eid
    3. 這次同步清單裡已不存在的舊 Scopus 記錄：移除

    這樣前台 Publications 頁面才能維持：
    - 同一篇論文只出現一次
    - 舊資料逐步被正式的 Scopus 識別碼接手
    - 資料庫不會殘留不再屬於同步結果的舊論文
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
            # 每篇論文一定要有 scopus_eid，這是整個同步去重與更新的核心鍵值。
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
                # 若資料庫中已經有相同 scopus_eid，代表就是同一篇論文，直接刷新內容即可。
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
                # 若沒有相同 scopus_eid，但標題或 URL 對得上，
                # 通常代表這篇論文早年曾經手動匯入，現在改由 Scopus 正式接管。
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
            # 本次同步後，凡是不在 active_eids 中、卻仍有 scopus_eid 的資料，
            # 代表它已經不屬於目前同步結果，應該移除以保持資料一致。
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
