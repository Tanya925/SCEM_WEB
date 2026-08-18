# Main purpose: centralize research_projects queries, updates, and public-list formatting.

from .common import (  # Shared database helpers and column constants.
    PROJECT_COLUMNS,
    PROJECT_ORDER_SQL,
    build_insert_sql,
    build_update_sql,
    execute_write,
    fetch_all,
    fetch_one,
    values_for_columns,
)

# Fetch the full project list used by the admin page.
def get_all_projects():
    """Fetch the full project list for the admin page."""
    return fetch_all(
        f"""
        SELECT *
        FROM research_projects
        {PROJECT_ORDER_SQL}
        """
    )

# Fetch one project by ID.
def get_project_by_id(project_id):
    """Fetch a single project by its ID."""
    return fetch_one(
        """
        SELECT *
        FROM research_projects
        WHERE id = ?
        """,
        (project_id,),
    )

# Insert a new project record.
def create_project(form_data):
    """Insert a new research_projects record."""
    query = build_insert_sql("research_projects", PROJECT_COLUMNS)
    execute_write(query, values_for_columns(form_data, PROJECT_COLUMNS))

# Update an existing project record.
def update_project(project_id, form_data):
    """Update the specified research_projects record."""
    query = build_update_sql("research_projects", PROJECT_COLUMNS, "id = ?")
    execute_write(query, values_for_columns(form_data, PROJECT_COLUMNS) + (project_id,))

# Delete a specific project record.
def delete_project(project_id):
    """Delete the specified research_projects record."""
    execute_write("DELETE FROM research_projects WHERE id = ?", (project_id,))

# Build the grouped data structure used by the public /research page.
def get_research_projects():
    """Group projects into ongoing and finished collections for the public site."""
    grouped_research = {
        "ongoing": [],
        "finished": [],
    }

    for row in get_all_projects():
        grouped_research[row["project_type"]].append(row)

    return grouped_research
