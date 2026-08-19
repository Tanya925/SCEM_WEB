# Main purpose: centralize SCEM staff queries, updates, and frontend display formatting.

from .common import (  # Shared database helpers and column constants.
    STAFF_COLUMNS,
    STAFF_DIRECTORY_SECTIONS,
    STAFF_ORDER_SQL,
    attach_staff_scopus_metadata,
    build_insert_sql,
    build_update_sql,
    execute_write,
    fetch_all,
    fetch_one,
    get_db_connection,
    normalize_staff_filter_value,
    values_for_columns,
)

#
#     Add any staff-table columns required by Scopus synchronization.
#
#     At the moment this only ensures the h-index timestamp column exists.
#     
def ensure_staff_table_columns() -> None:
    connection = get_db_connection()
    try:
        existing_columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(staff)").fetchall()
        }

        if "scopus_hindex_updated_at" not in existing_columns:
            connection.execute(
                "ALTER TABLE staff ADD COLUMN scopus_hindex_updated_at TEXT"
            )

        connection.commit()
    finally:
        connection.close()

# Fetch the full staff list for admin pages using the shared staff ordering rules.
# Fetch the full staff list for admin pages.
def get_all_staff():
    staff_list = fetch_all(
        f"""
        SELECT *
        FROM staff
        {STAFF_ORDER_SQL}
        """
    )
    return attach_staff_scopus_metadata(staff_list)

# Fetch one staff record by ID.
# Fetch a single staff record by ID.
def get_staff_by_id(staff_id):
    staff = fetch_one("SELECT * FROM staff WHERE id = ?", (staff_id,))
    if staff is None:
        return None

    return attach_staff_scopus_metadata([staff])[0]

# Insert a new staff record.
# Insert a new staff record.
def create_staff(form_data):
    query = build_insert_sql("staff", STAFF_COLUMNS)
    execute_write(query, values_for_columns(form_data, STAFF_COLUMNS))

# Update an existing staff record.
# Update the specified staff record.
def update_staff(staff_id, form_data):
    query = build_update_sql("staff", STAFF_COLUMNS, "id = ?")
    execute_write(query, values_for_columns(form_data, STAFF_COLUMNS) + (staff_id,))

# Delete a specific staff record.
# Delete the specified staff record.
def delete_staff(staff_id):
    execute_write("DELETE FROM staff WHERE id = ?", (staff_id,))

# Fetch the staff data actually displayed on the public Staff page.
# Fetch the staff list shown on the public Staff page.
def get_staff_directory():
    staff_rows = fetch_all(
        """
        SELECT *
        FROM staff
        ORDER BY sort_order ASC, id ASC
        """
    )
    return attach_staff_scopus_metadata(staff_rows)

# Group public staff data into the three fixed Staff-page sections.
# Group public staff into the predefined directory sections.
def get_staff_directory_sections():
    staff_rows = get_staff_directory()
    grouped_staff = {section["key"]: [] for section in STAFF_DIRECTORY_SECTIONS}

    for staff in staff_rows:
        section_key = (staff["staff_group"] or "member").strip().lower()
        if section_key not in grouped_staff:
            section_key = "member"
        grouped_staff[section_key].append(staff)

    return [
        {
            "key": section["key"],
            "title_en": section["title_en"],
            "title_th": section["title_th"],
            "staff": grouped_staff[section["key"]],
        }
        for section in STAFF_DIRECTORY_SECTIONS
    ]

# Build the filter options used by the Staff page search UI.
# Prepare search and filter options for the public Staff page.
def get_staff_filter_options():
    staff_rows = get_staff_directory()
    positions = []
    departments = []
    seen_positions = set()
    seen_departments = set()

    for staff in staff_rows:
        position_key = staff.get("position_filter_key", "")
        department_key = staff.get("department_filter_key", "")

        if position_key and position_key not in seen_positions:
            positions.append({
                "value": position_key,
                "label_en": staff["position_en"] or staff["position_th"],
                "label_th": staff["position_th"] or staff["position_en"],
            })
            seen_positions.add(position_key)

        if department_key and department_key not in seen_departments:
            departments.append({
                "value": department_key,
                "label_en": staff["department_en"] or staff["department_th"],
                "label_th": staff["department_th"] or staff["department_en"],
            })
            seen_departments.add(department_key)

    return {
        "positions": positions,
        "departments": departments,
    }

# Fetch all staff records with a configured Scopus Author ID for crawler updates.
# Fetch all staff members that have a Scopus Author ID configured.
def get_staff_scopus_targets():
    staff_rows = fetch_all(
        """
        SELECT id, name_en, name_th, scopus_author_id
        FROM staff
        WHERE COALESCE(NULLIF(scopus_author_id, ''), '') != ''
        ORDER BY sort_order ASC, id ASC
        """
    )
    return [dict(staff) for staff in staff_rows]

# Batch-write the crawler's h-index results back to the staff table.
#
#     Batch-write the synchronized h-index values back to the staff table.
#
#     Updating in one database session keeps the synchronization logic simpler
#     and avoids repeatedly opening and closing the SQLite connection.
#     
def update_staff_scopus_metrics(rows):
    if not rows:
        return

    ensure_staff_table_columns()
    connection = get_db_connection()
    try:
        for row in rows:
            author_id = (row.get("author_id") or "").strip()
            if not author_id:
                continue

            hindex_value = row.get("hindex")
            try:
                parsed_hindex = int(hindex_value) if hindex_value not in ("", None) else None
            except (TypeError, ValueError):
                parsed_hindex = None

            connection.execute(
                """
                UPDATE staff
                SET scopus_hindex = ?,
                    scopus_hindex_updated_at = DATETIME('now', '+7 hours')
                WHERE scopus_author_id = ?
                """,
                (parsed_hindex, author_id),
            )

        connection.commit()
    finally:
        connection.close()


