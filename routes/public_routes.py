# Main purpose: handle SCEM public pages, language switching, project detail pages, and the publications JSON API.

# ===== Imports =====
from flask import Blueprint, abort, jsonify, redirect, render_template, request, session, url_for  # Common Flask helpers.
from database.publication_db import get_all_publications

# Import public-service helpers so routes mainly coordinate requests and responses.
from services.public_service import (
    get_homepage_context,
    get_public_project_detail,
    get_research_page_context,
    get_staff_page_context,
)

# ===== Blueprint =====
# public_bp holds every visitor-facing route so public pages stay separate from admin pages.
public_bp = Blueprint("public", __name__)

# ===== Routes =====
# Switch the public-site language.
# Only en and th are supported, and the selection is stored in session across pages.
@public_bp.route("/language/<lang_code>")
def change_language(lang_code):
    """Switch the public-site language and return to the source page or homepage."""
    if lang_code not in {"en", "th"}:
        lang_code = "en"

    session["language"] = lang_code

    next_url = request.args.get("next", "").strip()
    if next_url.startswith("/"):
        return redirect(next_url)

    return redirect(url_for("public.index"))

# Homepage: show the unit introduction, activity images, and research highlights.
@public_bp.route("/")
def index():
    """Render the website homepage."""
    return render_template(
        "public/index.html",
        **get_homepage_context(),
    )

# Staff page: show grouped people data and filter options.
@public_bp.route("/staff")
def staff():
    """Render the public staff page."""
    return render_template(
        "public/staff.html",
        **get_staff_page_context(),
    )

# Research page: show ongoing and finished project lists.
@public_bp.route("/research")
def research():
    """Render the public research listing page."""
    return render_template("public/research.html", **get_research_page_context())

# Publications page: the page shell loads data from the public API on the client side.
@public_bp.route("/publications")
def publications():
    """Render the public publications shell; the client loads the data from the API."""
    return render_template("public/publications.html")

# Public publications endpoint: return all publication records in database order.
@public_bp.route("/api/publications")
def publication_data():
    """Return the JSON data used by the public publications page."""
    return jsonify(get_all_publications())

# Single research project detail page.
# Only ongoing projects have a public detail page.
@public_bp.route("/project/<int:project_id>")
def project_detail(project_id):
    """Render the detail page for one public ongoing project."""
    project = get_public_project_detail(project_id)

    if project is None:
        abort(404)

    return render_template("public/project_detail.html", project=project)
