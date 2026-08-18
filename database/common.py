# Main purpose: provide shared SQLite connections, column constants, SQL builders, and normalization helpers for all database modules.

import json
import re  # Regular expressions for text cleanup and matching.
import sqlite3
from pathlib import Path  # Filesystem path handling.

# Project-level constants shared by public pages, admin logic, and the crawler.
BASE_DIR = Path(__file__).resolve().parent.parent  # Absolute path to the project root.
DATABASE_PATH = BASE_DIR / "scem.db"  # Full path to the SQLite database file.
SCOPUS_AUTHOR_URL_TEMPLATE = "https://www.scopus.com/authid/detail.uri?authorId={author_id}"  # URL template for Scopus author pages.

# Staff ordering rules: group first, then admin sort order, then row ID for stability.
STAFF_ORDER_SQL = """
ORDER BY
    CASE
        WHEN LOWER(COALESCE(staff_group, '')) = 'advisor' THEN 0
        WHEN LOWER(COALESCE(staff_group, '')) = 'member' THEN 1
        WHEN LOWER(COALESCE(staff_group, '')) = 'researcher' THEN 2
        ELSE 3
    END,
    sort_order ASC,
    id ASC
"""

# Shared ordering clause for project queries.
PROJECT_ORDER_SQL = """
ORDER BY
    CASE project_type WHEN 'ongoing' THEN 0 ELSE 1 END,
    id ASC
"""

# staff table columns, kept in a stable order for create/update SQL generation.
STAFF_COLUMNS = (
    "name_en",
    "name_th",
    "position_en",
    "position_th",
    "department_en",
    "department_th",
    "staff_group",
    "sort_order",
    "photo_filename",
    "profile_url",
    "scopus_author_id",
    "scopus_hindex",
    "audio_en_url",
    "audio_th_url",
)

# general_info table columns, kept in a stable order for create/update SQL generation.
GENERAL_INFO_COLUMNS = (
    "page_title_en",
    "page_title_th",
    "about_content_en",
    "about_content_th",
    "content_en",
    "content_th",
)

# research_projects table columns, kept in a stable order for create/update SQL generation.
PROJECT_COLUMNS = (
    "project_type",
    "year_en",
    "year_th",
    "title_en",
    "title_th",
    "leader_en",
    "leader_th",
    "leader_photo_filename",
    "deputy_en",
    "deputy_th",
    "deputy_photo_filename",
    "coordinator_en",
    "coordinator_th",
    "coordinator_photo_filename",
    "advisor_en",
    "advisor_th",
    "advisor_photo_filename",
    "researcher_en",
    "researcher_th",
    "researcher_photos_json",
    "engineer_en",
    "engineer_th",
    "engineer_photos_json",
    "assistant_en",
    "assistant_th",
    "assistant_photos_json",
    "duration_en",
    "duration_th",
    "lead_unit_en",
    "lead_unit_th",
    "partner_en",
    "partner_th",
    "funding_en",
    "funding_th",
    "budget_en",
    "budget_th",
    "collaboration_details_en",
    "collaboration_details_th",
    "custom_team_fields_json",
    "custom_detail_fields_json",
    "notes",
    "description_en",
    "description_th",
)

# The public Staff page is always split into three fixed sections.
# These definitions provide the shared section order and labels.
STAFF_DIRECTORY_SECTIONS = [
    {"key": "advisor", "title_en": "ADVISOR", "title_th": "ที่ปรึกษา"},
    {"key": "member", "title_en": "MEMBER", "title_th": "สมาชิก"},
    {"key": "researcher", "title_en": "RESEARCHER", "title_th": "นักวิจัย"},
]

# Normalize staff filter text to avoid mismatches caused by case or extra whitespace.
def normalize_staff_filter_value(value):
    """Normalize filter values so case and whitespace do not break matching."""
    cleaned_value = re.sub(r"\s+", " ", str(value or "").strip().lower())
    return cleaned_value

# Create the shared SQLite connection used throughout the project.
def get_db_connection():
    """Create a shared SQLite connection with dict-like row access enabled."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

# Run a query and return the first row.
def fetch_one(query, params=()):
    """Execute a query and return the first result row."""
    connection = get_db_connection()
    try:
        return connection.execute(query, params).fetchone()
    finally:
        connection.close()

# Run a query and return all rows.
def fetch_all(query, params=()):
    """Execute a query and return all result rows."""
    connection = get_db_connection()
    try:
        return connection.execute(query, params).fetchall()
    finally:
        connection.close()

# Execute a write query such as insert, update, or delete.
def execute_write(query, params=()):
    """Execute insert, update, or delete SQL."""
    connection = get_db_connection()
    try:
        connection.execute(query, params)
        connection.commit()
    finally:
        connection.close()

# Read SQL parameter values from form_data in the order required by a column list.
def values_for_columns(form_data, columns):
    """Extract values in column order for SQL parameter binding."""
    return tuple(form_data.get(column) for column in columns)

# Build an INSERT SQL statement.
def build_insert_sql(table_name, columns):
    """Build the INSERT SQL for the specified table and columns."""
    placeholders = ", ".join("?" for _ in columns)
    column_sql = ", ".join(columns)
    return f"INSERT INTO {table_name} ({column_sql}) VALUES ({placeholders})"

# Build an UPDATE SQL statement.
def build_update_sql(table_name, columns, where_clause):
    """Build the UPDATE SQL for the specified table, columns, and where clause."""
    assignments = ", ".join(f"{column} = ?" for column in columns)
    return f"UPDATE {table_name} SET {assignments} WHERE {where_clause}"

# Build the full Scopus author URL from a staff record.
def build_staff_scopus_url(staff):
    """Build the Scopus author page URL from a staff row."""
    try:
        author_id = (staff["scopus_author_id"] or "").strip()
    except (KeyError, TypeError, IndexError):
        author_id = ""

    if not author_id:
        return ""

    return SCOPUS_AUTHOR_URL_TEMPLATE.format(author_id=author_id)

# Enrich staff rows with Scopus and filter metadata used by the frontend.
def attach_staff_scopus_metadata(staff_rows):
    """Attach Scopus URLs and filter keys to staff rows."""
    if not staff_rows:
        return []

    enriched_staff_rows = []

    for staff in staff_rows:
        staff_data = dict(staff)
        staff_data["scopus_url"] = build_staff_scopus_url(staff_data)
        staff_data["position_filter_key"] = normalize_staff_filter_value(
            staff_data.get("position_en") or staff_data.get("position_th")
        )
        staff_data["department_filter_key"] = normalize_staff_filter_value(
            staff_data.get("department_en") or staff_data.get("department_th")
        )
        enriched_staff_rows.append(staff_data)

    return enriched_staff_rows

# Normalize freeform names from project pages so they can be matched against staff records.
def normalize_project_person_name(name):
    """Normalize a project-person name into a matching-friendly format."""
    cleaned_name = (name or "").strip().lower()
    cleaned_name = cleaned_name.replace("\n", " ").replace("\t", " ")
    cleaned_name = re.sub(r"[.,;:()\\-_/]", " ", cleaned_name)

    removable_tokens = {
        "assoc", "associate", "asst", "assistant", "prof", "professor", "distinguished",
        "of", "practice", "dr", "ph", "d", "phd", "eng", "deng", "miss", "mr", "mrs", "ms",
        "รองศาสตราจารย์", "ผู้ช่วยศาสตราจารย์", "ศาสตราจารย์", "ศาสตราจารย์เชี่ยวชาญพิเศษ",
        "อาจารย์", "ดร", "ผศ", "รศ", "ศ", "นางสาว", "นาย", "นาง",
    }

    normalized_tokens = []
    for token in cleaned_name.split():
        compact_token = token.strip()
        if compact_token and compact_token not in removable_tokens:
            normalized_tokens.append(compact_token)

    return "".join(normalized_tokens)

# Build a normalized-name to staff lookup used for automatic photo matching.
def get_staff_photo_lookup():
    """Build a lookup from normalized names to staff photo records."""
    staff_rows = fetch_all(
        """
        SELECT name_en, name_th, photo_filename
        FROM staff
        """
    )
    staff_lookup = {}

    for staff in staff_rows:
        for name_key in ("name_en", "name_th"):
            normalized_name = normalize_project_person_name(staff[name_key])
            if normalized_name:
                staff_lookup[normalized_name] = staff

    return staff_lookup

# Parse stored JSON for custom project fields into a safe list of dictionaries.
def parse_project_custom_fields(raw_text):
    """Parse custom-field JSON into a safe list of dictionaries."""
    if not raw_text:
        return []

    try:
        parsed_fields = json.loads(raw_text)
    except json.JSONDecodeError:
        return []

    if not isinstance(parsed_fields, list):
        return []

    return [field for field in parsed_fields if isinstance(field, dict)]

# Parse the JSON for multi-person photo fields into an ordered filename list.
def parse_project_member_photo_list(raw_text):
    """Parse member-photo JSON into a clean list of filenames."""
    if not raw_text:
        return []

    try:
        parsed_filenames = json.loads(raw_text)
    except json.JSONDecodeError:
        return []

    if not isinstance(parsed_filenames, list):
        return []

    return [str(filename or "").strip() for filename in parsed_filenames]
