# Main purpose: build the SCEM Flask application, initialize the database and shared helpers, and register the public and admin routes.

# ===== Imports =====
import os  # Read operating-system information and environment variables.
import re  # Handle regular expressions.
from datetime import timedelta  # Configure the session lifetime.
from pathlib import Path  # Work with filesystem paths.
from flask import Flask, request, session
from dotenv import load_dotenv

from database.common import (
    DATABASE_PATH,
    build_staff_scopus_url,
    get_db_connection,
    get_staff_photo_lookup,
    normalize_project_person_name,
    parse_project_custom_fields,
    parse_project_member_photo_list,
)
from database.auth_db import ensure_auth_tables
from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp
from routes.public_routes import public_bp
from services.scopus_scheduler import init_scopus_scheduler

# ===== Constants =====
# Project-level constants shared by startup logic and template helpers.
BASE_DIR = Path(__file__).resolve().parent  # Absolute path to the project root.
LANGUAGE_FALLBACK = {"en": "th", "th": "en"}  # Fallback language when the preferred field is empty.
OVERVIEW_IMAGE_MAP = {  # Mapping between overview titles and the fixed homepage images.
    "logistics/ supply chain strategy development": {
        "en": "EN_Logistics_ Supply Chain Strategy Development.png",
        "th": "TH_Logistics_ Supply Chain Strategy Development.png",
    },
    "การพัฒนากลยุทธ์ด้านโลจิสติกส์และโซ่อุปทาน": {
        "en": "EN_Logistics_ Supply Chain Strategy Development.png",
        "th": "TH_Logistics_ Supply Chain Strategy Development.png",
    },
    "industrial logistics": {
        "en": "EN_Industrial Logistics.png",
        "th": "TH_Industrial Logistics.png",
    },
    "โลจิสติกส์อุตสาหกรรม": {
        "en": "EN_Industrial Logistics.png",
        "th": "TH_Industrial Logistics.png",
    },
}

# Load the local .env file early so required settings are available during startup.
load_dotenv(BASE_DIR / ".env")

# ===== App Setup =====
# Explicitly set the template and static directories to keep path resolution stable.
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
)

# ===== Configuration Helper =====
# Apply the secret key, cookie settings, and database configuration required at startup.
def configure_app(flask_app):
    secret_key = os.environ.get("SECRET_KEY", "").strip()
    if not secret_key:
        raise RuntimeError("SECRET_KEY environment variable is required before starting the app.")

    flask_app.config["SECRET_KEY"] = secret_key
    flask_app.config["SESSION_COOKIE_HTTPONLY"] = True
    flask_app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    flask_app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
    flask_app.config["DATABASE"] = str(DATABASE_PATH)

# ===== Template Helpers =====
# The Flask context processor injects shared data and helper functions into all templates so route handlers stay focused on requests and responses.
@app.context_processor
# Register shared helpers that every Jinja template can use directly.
def inject_template_helpers():
    current_language = session.get("language", "en")
    staff_photo_lookup_cache = None

    # Build the primary field name for the requested language.
    def primary_key(prefix, language):
        return f"{prefix}_{language}"

    # Build the fallback field name for the requested language.
    def fallback_key(prefix, language):
        return f"{prefix}_{LANGUAGE_FALLBACK.get(language, 'en')}"

    # Normalize null-like display values into a safe empty string.
    def normalize_display_text(value):
        if value is None:
            return ""

        cleaned_value = str(value).strip()
        if cleaned_value.lower() in {"none", "null", "nil", "n/a"}:
            return ""

        return cleaned_value

    # Safely read a field value and return an empty string when it is missing.
    def row_value(data, key):
        try:
            return normalize_display_text(data[key])
        except (KeyError, TypeError, IndexError):
            return ""

    # Read a multilingual field and fall back to the alternate language when needed.
    def field_text(data, field_name):
        if data is None:
            return ""

        preferred_value = row_value(data, primary_key(field_name, current_language))
        fallback_value = row_value(data, fallback_key(field_name, current_language))
        return preferred_value or fallback_value

    # Convert long homepage text into titled sections for rendering.
    def format_general_content(raw_text):
        if not raw_text:
            return []

        sections = []
        current_section = None

        for line in [line.strip() for line in str(raw_text).splitlines()]:
            if not line or line in {"Details and Works", "รายละเอียดและผลงาน"}:
                continue

            if line.startswith("-"):
                if current_section is None:
                    current_section = {"title": "", "items": []}
                    sections.append(current_section)
                current_section["items"].append(line.lstrip("-").strip())
                continue

            current_section = {"title": line, "items": []}
            sections.append(current_section)

        return sections

    # Return the fixed homepage image that matches the given section title.
    def overview_image_for_title(title):
        normalized_title = " ".join(normalize_display_text(title).lower().split())
        if not normalized_title:
            return None

        image_options = OVERVIEW_IMAGE_MAP.get(normalized_title)
        if not image_options:
            return None

        return image_options.get(current_language) or image_options.get("en")

    # Split multiline text into a list that excludes blank rows.
    def text_lines(raw_text):
        return [
            cleaned_line
            for cleaned_line in (
                normalize_display_text(line)
                for line in str(raw_text or "").splitlines()
            )
            if cleaned_line
        ]

    # Parse freeform people text into structured heading and person entries.
    def parse_people_entries(raw_text):
        entries = []

        for raw_line in str(raw_text or "").splitlines():
            line = normalize_display_text(raw_line)
            if not line:
                continue

            if line.startswith("("):
                closing_index = line.find(")")
                if closing_index != -1:
                    heading = line[:closing_index + 1].strip().rstrip(";")
                    remainder = line[closing_index + 1:].strip(" ;,")

                    if heading:
                        entries.append({"type": "heading", "text": heading})

                    if remainder:
                        entries.extend(
                            {"type": "person", "name": part.strip()}
                            for part in re.split(r"[;,]", remainder)
                            if part.strip()
                        )
                    continue

            entries.extend(
                {"type": "person", "name": part.strip()}
                for part in re.split(r"[;,]", line)
                if part.strip()
            )

        return entries

    # Use the explicit photo filename first, otherwise fall back to the staff record photo.
    def photo_for_person(name, override_filename=""):
        nonlocal staff_photo_lookup_cache

        if override_filename:
            return override_filename

        if not name:
            return ""

        if staff_photo_lookup_cache is None:
            staff_photo_lookup_cache = get_staff_photo_lookup()

        normalized_name = normalize_project_person_name(name)
        matched_staff = staff_photo_lookup_cache.get(normalized_name)
        if matched_staff:
            return matched_staff["photo_filename"] or ""

        return ""

    # Build the full Scopus profile URL for a staff record.
    def staff_scopus_url(staff):
        return build_staff_scopus_url(staff)

    # Prepare multi-person project fields and photos for direct template rendering.
    def project_people_entries(project, field_name):
        raw_text = field_text(project, field_name)
        photo_filenames = row_value(project, f"{field_name}_photos_json")
        parsed_filenames = parse_project_member_photo_list(photo_filenames)

        entries = []
        person_index = 0

        for entry in parse_people_entries(raw_text):
            if entry["type"] == "heading":
                entries.append(entry)
                continue

            override_filename = parsed_filenames[person_index] if person_index < len(parsed_filenames) else ""
            entries.append({
                "type": "person",
                "name": entry["name"],
                "photo_filename": photo_for_person(entry["name"], override_filename),
            })
            person_index += 1

        return entries

    # Parse custom project team fields and attach photo information when possible.
    def project_custom_team_fields(project):
        entries = []

        for field in parse_project_custom_fields(row_value(project, "custom_team_fields_json")):
            label = field.get(primary_key("label", current_language)) or field.get(fallback_key("label", current_language)) or ""
            value = field.get(primary_key("value", current_language)) or field.get(fallback_key("value", current_language)) or ""

            if not label and not value:
                continue

            entries.append({
                "label": label,
                "value": value,
                "photo_filename": photo_for_person(value, field.get("photo_filename", "")),
            })

        return entries

    # Parse custom project detail fields for direct template rendering.
    def project_custom_detail_fields(project):
        entries = []

        for field in parse_project_custom_fields(row_value(project, "custom_detail_fields_json")):
            label = field.get(primary_key("label", current_language)) or field.get(fallback_key("label", current_language)) or ""
            value = field.get(primary_key("value", current_language)) or field.get(fallback_key("value", current_language)) or ""

            if not label and not value:
                continue

            entries.append({
                "label": label,
                "value": value,
            })

        return entries

    # Inject the shared helpers into the Jinja environment for both public and admin templates.
    return {
        "current_language": current_language,  # Template variable name on the left, function/local value on the right.
        "current_path": request.path,
        "field_text": field_text,
        "format_general_content": format_general_content,
        "overview_image_for_title": overview_image_for_title,
        "text_lines": text_lines,
        "photo_for_person": photo_for_person,
        "staff_scopus_url": staff_scopus_url,
        "project_people_entries": project_people_entries,
        "project_custom_team_fields": project_custom_team_fields,
        "project_custom_detail_fields": project_custom_detail_fields,
    }

# ===== Database Startup Checks =====
# Test whether the seeded SQLite database can be opened before the app starts.
def test_db_connection():
    if not DATABASE_PATH.exists():
        print(
            "Database file is missing. Run init_db/seed.py before starting the app."
        )
        return False

    try:
        connection = get_db_connection()
        connection.close()
        return True
    except Exception as error:
        print(f"Database connection failed: {error}")
        return False

# Return whether the seeded database still contains the required application tables.
def has_required_database_tables():
    connection = get_db_connection()
    try:
        existing_tables = {
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

    required_tables = {
        "general_info",
        "home_activity_images",
        "publications",
        "research_projects",
        "staff",
        "users",
    }

    return required_tables.issubset(existing_tables)

# Verify that required tables exist before startup.
def ensure_database_ready():
    if not test_db_connection():
        return False

    if not has_required_database_tables():
        print(
            "Database is missing required tables. Run init_db/seed.py before starting the app."
        )
        return False

    ensure_auth_tables()

    return True

configure_app(app)
database_ready = ensure_database_ready()
scopus_scheduler_started = init_scopus_scheduler(app) if database_ready else False

# ===== Blueprint Registration =====
# Register the public, auth, and admin blueprints.
app.register_blueprint(public_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# ===== Application Entry Point =====
# When app.py is executed directly, verify the database first and then start the server.
if __name__ == "__main__":
    if database_ready:
        print("SQLite database connection succeeded.")
        if scopus_scheduler_started:
            print("In-process Scopus scheduler is running.")
        else:
            print("Scopus scheduler is not running in this process.")
        app.run(port=3000, debug=False)
    else:
        print(
            "SQLite database is not ready. Please run init_db/seed.py and then start the app again."
        )
        raise SystemExit(1)


