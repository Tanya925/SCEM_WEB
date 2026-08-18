# Main purpose: handle General Info, Staff, and Projects admin forms, file uploads, and related database writes.

import json
from pathlib import Path
from flask import request  # Access submitted form data and uploaded files.
from werkzeug.utils import secure_filename  # Sanitize uploaded filenames.

# Import database helpers so the service layer can call them directly.
from database.general_info_db import (
    add_home_activity_image,
    delete_home_activity_image,
    get_general_info,
    get_home_activity_images,
    update_general_info,
)
from database.project_db import (
    create_project,
    delete_project,
    get_all_projects,
    get_project_by_id,
    update_project,
)
from database.staff_db import (
    create_staff,
    delete_staff,
    get_all_staff,
    get_staff_by_id,
    update_staff,
)
from database.common import (
    parse_project_custom_fields,
    parse_project_member_photo_list,
)

# File-upload settings used by the admin area.
STATIC_FOLDER = Path(__file__).resolve().parent.parent / "static"  # Root folder for static assets.
IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}  # Allowed image extensions.
PDF_EXTENSIONS = {"pdf"}  # Allowed PDF extensions.
AUDIO_EXTENSIONS = {"mp3", "m4a", "wav", "ogg", "aac"}   # Allowed audio extensions.

# Read a text form field and trim surrounding whitespace.
def text_form_value(field_name, default=""):
    """Read a text form field and strip surrounding whitespace."""
    return request.form.get(field_name, default).strip()

# Shared helper for saving uploaded files.
# It validates the extension, normalizes the filename, and overwrites an existing file with the same name.
def save_uploaded_file(uploaded_file, folder_name, allowed_extensions):
    """Validate the extension and save an uploaded file, returning the saved filename."""
    if not uploaded_file or not uploaded_file.filename:
        return ""

    raw_filename = uploaded_file.filename
    cleaned_filename = secure_filename(raw_filename)
    extension = raw_filename.rsplit(".", 1)[-1].lower() if "." in raw_filename else ""

    if extension not in allowed_extensions:
        return ""

    saved_filename = cleaned_filename or f"uploaded-file.{extension}"
    target_folder = STATIC_FOLDER / folder_name
    target_folder.mkdir(parents=True, exist_ok=True)
    uploaded_file.save(target_folder / saved_filename)

    return saved_filename

# Reuse the existing staff photo filename when no new file is uploaded.
def resolve_uploaded_filename(file_field_name, existing_filename=""):
    """Keep the existing filename when no replacement file is uploaded."""
    uploaded_filename = save_uploaded_file(
        request.files.get(file_field_name),
        "uploads",
        IMAGE_EXTENSIONS,
    )
    return uploaded_filename or existing_filename

# Build the admin editing structure for bilingual project-member names and photo lists.
def build_project_member_entries(project, field_name):
    """Convert stored project member names and photos into form-ready entry data."""
    if not project:
        return []

    member_names_en = [
        line.strip()
        for line in str(project[f"{field_name}_en"] or "").splitlines()
        if line.strip()
    ]
    member_names_th = [
        line.strip()
        for line in str(project[f"{field_name}_th"] or "").splitlines()
        if line.strip()
    ]
    member_photos = parse_project_member_photo_list(project[f"{field_name}_photos_json"])

    member_count = max(len(member_names_en), len(member_names_th), len(member_photos))
    member_entries = []

    for index in range(member_count):
        member_entries.append({
            "name_en": member_names_en[index] if index < len(member_names_en) else "",
            "name_th": member_names_th[index] if index < len(member_names_th) else "",
            "photo_filename": member_photos[index] if index < len(member_photos) else "",
        })

    return member_entries

# Normalize Researchers / Engineers / Assistants style form fields into one shared structure.
# This keeps route handlers from repeating nearly identical logic for each group.
def collect_project_member_entries(field_prefix):
    """Collect multi-person field data into a normalized name-and-photo list."""
    names_en = request.form.getlist(f"{field_prefix}_name_en[]")
    names_th = request.form.getlist(f"{field_prefix}_name_th[]")
    existing_photos = request.form.getlist(f"{field_prefix}_existing_photo[]")
    uploaded_photos = request.files.getlist(f"{field_prefix}_photo_file[]")

    member_entries = []
    member_count = max(len(names_en), len(names_th), len(existing_photos), len(uploaded_photos))

    for index in range(member_count):
        name_en = names_en[index].strip() if index < len(names_en) else ""
        name_th = names_th[index].strip() if index < len(names_th) else ""
        existing_photo = existing_photos[index].strip() if index < len(existing_photos) else ""
        uploaded_file = uploaded_photos[index] if index < len(uploaded_photos) else None
        uploaded_photo = save_uploaded_file(uploaded_file, "uploads", IMAGE_EXTENSIONS)

        if name_en or name_th or existing_photo or uploaded_photo:
            member_entries.append({
                "name_en": name_en,
                "name_th": name_th,
                "photo_filename": uploaded_photo or existing_photo,
            })

    return member_entries

# Convert multi-person field data back into the newline-delimited text format stored in the database.
def build_member_names_text(entries, language):
    """Convert member entries back into the multiline text format used in storage."""
    lines = []

    for entry in entries:
        primary_name = entry[f"name_{language}"]
        fallback_name = entry["name_th"] if language == "en" else entry["name_en"]
        display_name = (primary_name or fallback_name).strip()

        if display_name:
            lines.append(display_name)

    return "\n".join(lines)

# Collect the form data for custom single-person team fields.
def collect_custom_team_fields():
    """Collect bilingual text and photo data for custom team fields."""
    labels_en = request.form.getlist("custom_team_label_en[]")
    labels_th = request.form.getlist("custom_team_label_th[]")
    values_en = request.form.getlist("custom_team_value_en[]")
    values_th = request.form.getlist("custom_team_value_th[]")
    existing_photos = request.form.getlist("custom_team_existing_photo[]")
    uploaded_photos = request.files.getlist("custom_team_photo_file[]")

    custom_team_fields = []
    field_count = max(
        len(labels_en),
        len(labels_th),
        len(values_en),
        len(values_th),
        len(existing_photos),
        len(uploaded_photos),
    )

    for index in range(field_count):
        label_en = labels_en[index].strip() if index < len(labels_en) else ""
        label_th = labels_th[index].strip() if index < len(labels_th) else ""
        value_en = values_en[index].strip() if index < len(values_en) else ""
        value_th = values_th[index].strip() if index < len(values_th) else ""
        existing_photo = existing_photos[index].strip() if index < len(existing_photos) else ""
        uploaded_file = uploaded_photos[index] if index < len(uploaded_photos) else None
        uploaded_photo = save_uploaded_file(uploaded_file, "uploads", IMAGE_EXTENSIONS)

        if label_en or label_th or value_en or value_th or existing_photo or uploaded_photo:
            custom_team_fields.append({
                "label_en": label_en,
                "label_th": label_th,
                "value_en": value_en,
                "value_th": value_th,
                "photo_filename": uploaded_photo or existing_photo,
            })

    return custom_team_fields

# Collect the form data for custom general-detail fields.
def collect_custom_detail_fields():
    """Collect bilingual text data for custom detail fields."""
    labels_en = request.form.getlist("custom_detail_label_en[]")
    labels_th = request.form.getlist("custom_detail_label_th[]")
    values_en = request.form.getlist("custom_detail_value_en[]")
    values_th = request.form.getlist("custom_detail_value_th[]")

    custom_detail_fields = []
    field_count = max(len(labels_en), len(labels_th), len(values_en), len(values_th))

    for index in range(field_count):
        label_en = labels_en[index].strip() if index < len(labels_en) else ""
        label_th = labels_th[index].strip() if index < len(labels_th) else ""
        value_en = values_en[index].strip() if index < len(values_en) else ""
        value_th = values_th[index].strip() if index < len(values_th) else ""

        if label_en or label_th or value_en or value_th:
            custom_detail_fields.append({
                "label_en": label_en,
                "label_th": label_th,
                "value_en": value_en,
                "value_th": value_th,
            })

    return custom_detail_fields

# Build all initial dynamic-field data for the project editing page in one place.
def get_project_editing_context(project):
    """Prepare all dynamic-field seed data required by the project editing page."""
    if not project:
        return {
            "editing_researchers": [],
            "editing_engineers": [],
            "editing_assistants": [],
            "editing_custom_team_fields": [],
            "editing_custom_detail_fields": [],
        }

    return {
        "editing_researchers": build_project_member_entries(project, "researcher"),
        "editing_engineers": build_project_member_entries(project, "engineer"),
        "editing_assistants": build_project_member_entries(project, "assistant"),
        "editing_custom_team_fields": parse_project_custom_fields(project["custom_team_fields_json"]),
        "editing_custom_detail_fields": parse_project_custom_fields(project["custom_detail_fields_json"]),
    }

# Base context for the General Info admin page.
def get_general_info_page_context(success_message=None):
    """Provide the data required by the General Info admin template."""
    return {
        "general_info": get_general_info(),
        "activity_images": get_home_activity_images(),
        "success_message": success_message,
    }

# Handle the General Info form, including text updates and activity image management.
def handle_general_info_submission():
    """Handle homepage text updates and activity image create/delete actions."""
    action = request.form.get("form_action", "save_text").strip()

    if action == "add_activity_image":
        uploaded_filename = save_uploaded_file(
            request.files.get("activity_image_file"),
            "uploads",
            IMAGE_EXTENSIONS,
        )

        if uploaded_filename:
            add_home_activity_image(uploaded_filename)
            return "Activity image added successfully."

        return "Please upload a JPG, PNG, GIF, or WEBP image."

    if action == "delete_activity_image":
        image_id = request.form.get("image_id", type=int)
        if image_id:
            delete_home_activity_image(image_id)
            return "Activity image deleted successfully."

        return None

    form_data = {
        "page_title_en": text_form_value("page_title_en"),
        "page_title_th": text_form_value("page_title_th"),
        "about_content_en": text_form_value("about_content_en"),
        "about_content_th": text_form_value("about_content_th"),
        "content_en": text_form_value("content_en"),
        "content_th": text_form_value("content_th"),
    }
    update_general_info(form_data)
    return "General Info saved successfully."

# Base context for the Staff admin page.
def get_staff_page_context(edit_id=None, success_message=None):
    """Provide the data required by the Staff admin template."""
    editing_staff = get_staff_by_id(edit_id) if edit_id else None
    return {
        "staff_list": get_all_staff(),
        "success_message": success_message,
        "editing_staff": editing_staff,
    }

# Handle the Staff form, including create/update/delete actions and related file uploads.
def handle_staff_submission():
    """Handle Staff create/update/delete actions and related file uploads."""
    form_action = request.form.get("form_action", "save_staff").strip()

    if form_action == "delete_staff":
        delete_staff_id = request.form.get("delete_staff_id", type=int)
        if delete_staff_id:
            delete_staff(delete_staff_id)
            return {
                "success_message": "Staff deleted successfully.",
                "editing_staff": None,
            }

        return {
            "success_message": None,
            "editing_staff": None,
        }

    staff_id = request.form.get("staff_id", type=int)
    existing_staff = get_staff_by_id(staff_id) if staff_id else None

    uploaded_photo_filename = save_uploaded_file(
        request.files.get("photo_file"),
        "uploads",
        IMAGE_EXTENSIONS,
    )
    uploaded_profile_pdf = save_uploaded_file(
        request.files.get("profile_pdf_file"),
        "cv",
        PDF_EXTENSIONS,
    )
    uploaded_audio_en = save_uploaded_file(
        request.files.get("audio_en_file"),
        "audio/EN",
        AUDIO_EXTENSIONS,
    )
    uploaded_audio_th = save_uploaded_file(
        request.files.get("audio_th_file"),
        "audio/TH",
        AUDIO_EXTENSIONS,
    )

    profile_url = text_form_value("profile_url")
    if uploaded_profile_pdf:
        profile_url = f"/static/cv/{uploaded_profile_pdf}"

    audio_en_url = existing_staff["audio_en_url"] if existing_staff else ""
    audio_th_url = existing_staff["audio_th_url"] if existing_staff else ""

    if uploaded_audio_en:
        audio_en_url = f"/static/audio/EN/{uploaded_audio_en}"
    if uploaded_audio_th:
        audio_th_url = f"/static/audio/TH/{uploaded_audio_th}"

    staff_group = text_form_value("staff_group", "member").lower() or "member"
    if staff_group not in {"advisor", "member", "researcher"}:
        staff_group = "member"

    scopus_hindex_raw = request.form.get("scopus_hindex", "").strip()
    try:
        scopus_hindex = int(scopus_hindex_raw) if scopus_hindex_raw else None
    except ValueError:
        scopus_hindex = existing_staff["scopus_hindex"] if existing_staff else None

    form_data = {
        "name_en": text_form_value("name_en"),
        "name_th": text_form_value("name_th"),
        "position_en": text_form_value("position_en"),
        "position_th": text_form_value("position_th"),
        "department_en": text_form_value("department_en"),
        "department_th": text_form_value("department_th"),
        "staff_group": staff_group,
        "sort_order": request.form.get("sort_order", type=int) or 0,
        "photo_filename": uploaded_photo_filename or (existing_staff["photo_filename"] if existing_staff else ""),
        "profile_url": profile_url,
        "scopus_author_id": text_form_value("scopus_author_id"),
        "scopus_hindex": scopus_hindex,
        "audio_en_url": audio_en_url,
        "audio_th_url": audio_th_url,
    }

    if staff_id:
        update_staff(staff_id, form_data)
        success_message = "Staff updated successfully."
    else:
        create_staff(form_data)
        success_message = "Staff created successfully."

    return {
        "success_message": success_message,
        "editing_staff": None,
    }

# Base context for the Projects admin page, including the list and any project being edited.
def get_projects_page_context(edit_id=None, success_message=None, editing_project_override=None):
    """Provide the data required by the Projects admin template."""
    editing_project = editing_project_override if editing_project_override is not None else (
        get_project_by_id(edit_id) if edit_id else None
    )
    page_context = get_project_editing_context(editing_project)
    page_context.update({
        "project_list": get_all_projects(),
        "editing_project": editing_project,
        "success_message": success_message,
    })
    return page_context

# Handle the Projects form, including full CRUD and dynamic person-field processing.
def handle_projects_submission():
    """Handle Project create/update/delete actions and dynamic field normalization."""
    form_action = request.form.get("form_action", "save_project").strip()

    if form_action == "delete_project":
        delete_project_id = request.form.get("delete_project_id", type=int)
        if delete_project_id:
            delete_project(delete_project_id)
            return {
                "success_message": "Project deleted successfully.",
                "editing_project": None,
            }

        return {
            "success_message": None,
            "editing_project": None,
        }

    project_id = request.form.get("project_id", type=int)
    existing_project = get_project_by_id(project_id) if project_id else None

    researcher_entries = collect_project_member_entries("researcher")
    engineer_entries = collect_project_member_entries("engineer")
    assistant_entries = collect_project_member_entries("assistant")
    custom_team_fields = collect_custom_team_fields()
    custom_detail_fields = collect_custom_detail_fields()

    project_type = text_form_value("project_type", "ongoing")

    form_data = {
        "project_type": project_type,
        "year_en": text_form_value("year_en"),
        "year_th": text_form_value("year_th"),
        "title_en": text_form_value("title_en"),
        "title_th": text_form_value("title_th"),
        "leader_en": text_form_value("leader_en"),
        "leader_th": text_form_value("leader_th"),
        "leader_photo_filename": resolve_uploaded_filename(
            "leader_photo_file",
            existing_project["leader_photo_filename"] if existing_project else "",
        ),
        "deputy_en": text_form_value("deputy_en"),
        "deputy_th": text_form_value("deputy_th"),
        "deputy_photo_filename": resolve_uploaded_filename(
            "deputy_photo_file",
            existing_project["deputy_photo_filename"] if existing_project else "",
        ),
        "coordinator_en": text_form_value("coordinator_en"),
        "coordinator_th": text_form_value("coordinator_th"),
        "coordinator_photo_filename": resolve_uploaded_filename(
            "coordinator_photo_file",
            existing_project["coordinator_photo_filename"] if existing_project else "",
        ),
        "advisor_en": text_form_value("advisor_en"),
        "advisor_th": text_form_value("advisor_th"),
        "advisor_photo_filename": resolve_uploaded_filename(
            "advisor_photo_file",
            existing_project["advisor_photo_filename"] if existing_project else "",
        ),
        "researcher_en": build_member_names_text(researcher_entries, "en"),
        "researcher_th": build_member_names_text(researcher_entries, "th"),
        "researcher_photos_json": json.dumps([entry["photo_filename"] for entry in researcher_entries], ensure_ascii=False),
        "engineer_en": build_member_names_text(engineer_entries, "en"),
        "engineer_th": build_member_names_text(engineer_entries, "th"),
        "engineer_photos_json": json.dumps([entry["photo_filename"] for entry in engineer_entries], ensure_ascii=False),
        "assistant_en": build_member_names_text(assistant_entries, "en"),
        "assistant_th": build_member_names_text(assistant_entries, "th"),
        "assistant_photos_json": json.dumps([entry["photo_filename"] for entry in assistant_entries], ensure_ascii=False),
        "duration_en": text_form_value("duration_en"),
        "duration_th": text_form_value("duration_th"),
        "lead_unit_en": text_form_value("lead_unit_en"),
        "lead_unit_th": text_form_value("lead_unit_th"),
        "partner_en": text_form_value("partner_en"),
        "partner_th": text_form_value("partner_th"),
        "funding_en": text_form_value("funding_en"),
        "funding_th": text_form_value("funding_th"),
        "budget_en": text_form_value("budget_en"),
        "budget_th": text_form_value("budget_th"),
        "collaboration_details_en": text_form_value("collaboration_details_en"),
        "collaboration_details_th": text_form_value("collaboration_details_th"),
        "custom_team_fields_json": json.dumps(custom_team_fields, ensure_ascii=False),
        "custom_detail_fields_json": json.dumps(custom_detail_fields, ensure_ascii=False),
        "notes": text_form_value("notes"),
        "description_en": text_form_value("description_en"),
        "description_th": text_form_value("description_th"),
    }

    if project_type == "finished":
        form_data.update({
            "leader_en": "",
            "leader_th": "",
            "leader_photo_filename": "",
            "deputy_en": "",
            "deputy_th": "",
            "deputy_photo_filename": "",
            "coordinator_en": "",
            "coordinator_th": "",
            "coordinator_photo_filename": "",
            "advisor_en": "",
            "advisor_th": "",
            "advisor_photo_filename": "",
            "researcher_en": "",
            "researcher_th": "",
            "researcher_photos_json": "[]",
            "engineer_en": "",
            "engineer_th": "",
            "engineer_photos_json": "[]",
            "assistant_en": "",
            "assistant_th": "",
            "assistant_photos_json": "[]",
            "duration_en": "",
            "duration_th": "",
            "lead_unit_en": "",
            "lead_unit_th": "",
            "partner_en": "",
            "partner_th": "",
            "funding_en": "",
            "funding_th": "",
            "budget_en": "",
            "budget_th": "",
            "collaboration_details_en": "",
            "collaboration_details_th": "",
            "custom_team_fields_json": "[]",
            "custom_detail_fields_json": "[]",
            "notes": "",
            "description_en": "",
            "description_th": "",
        })
    else:
        form_data["year_en"] = ""
        form_data["year_th"] = ""

    if project_id:
        update_project(project_id, form_data)
        success_message = "Project updated successfully."
    else:
        create_project(form_data)
        success_message = "Project created successfully."

    return {
        "success_message": success_message,
        "editing_project": None,
    }
