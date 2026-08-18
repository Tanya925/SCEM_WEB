# Main purpose: centralize public-page data assembly and display logic for the SCEM site.

# Database query helpers used to fetch the data needed by public pages.
from database.general_info_db import get_general_info, get_home_activity_images
from database.project_db import get_project_by_id, get_research_projects
from database.staff_db import get_staff_directory_sections, get_staff_filter_options

# Homepage data assembly, including the introduction, activity images, and research highlights.
def get_homepage_context():
    """Prepare the data required by the homepage template."""
    return {
        "general_info": get_general_info(),
        "home_activity_images": get_home_activity_images(),
    }

# Staff page data assembly, including grouped staff records and filter options.
def get_staff_page_context():
    """Prepare grouped staff data and filter options for the Staff page template."""
    return {
        "staff_sections": get_staff_directory_sections(),
        "filter_options": get_staff_filter_options(),
    }

# Research page data assembly, including both ongoing and finished projects.
def get_research_page_context():
    """Prepare the project data required by the Research page template."""
    return {
        "research_projects": get_research_projects(),
    }

# Fetch a single research project that is allowed to be shown publicly.
def get_public_project_detail(project_id):
    """Return only an ongoing project that is allowed on the public site."""
    project = get_project_by_id(project_id)

    if project is None or project["project_type"] != "ongoing":
        return None

    return project
