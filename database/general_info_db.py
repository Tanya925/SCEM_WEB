# Main purpose: centralize queries and updates for homepage general info and activity images.

from .common import (  # Shared database helpers and column constants.
    GENERAL_INFO_COLUMNS,
    build_update_sql,
    execute_write,
    fetch_all,
    fetch_one,
    values_for_columns,
)

# Fetch the single homepage general_info row.
def get_general_info():
    """Fetch the single homepage general_info record."""
    return fetch_one("SELECT * FROM general_info ORDER BY id ASC LIMIT 1")

# Update the single homepage general_info row.
def update_general_info(form_data):
    """Update the single homepage general_info record."""
    general_info = fetch_one("SELECT id FROM general_info ORDER BY id ASC LIMIT 1")
    if general_info is None:
        return

    query = build_update_sql("general_info", GENERAL_INFO_COLUMNS, "id = ?")
    execute_write(query, values_for_columns(form_data, GENERAL_INFO_COLUMNS) + (general_info["id"],))

# Fetch all homepage activity-slider images.
def get_home_activity_images():
    """Fetch all homepage activity image records."""
    return fetch_all("SELECT * FROM home_activity_images ORDER BY id ASC")

# Add one homepage activity image record.
def add_home_activity_image(filename):
    """Insert a homepage activity image record."""
    cleaned_filename = (filename or "").strip()
    if not cleaned_filename:
        return

    execute_write(
        "INSERT OR IGNORE INTO home_activity_images (filename) VALUES (?)",
        (cleaned_filename,),
    )

# Delete a specific homepage activity image record.
def delete_home_activity_image(image_id):
    """Delete the specified homepage activity image record."""
    execute_write("DELETE FROM home_activity_images WHERE id = ?", (image_id,))
