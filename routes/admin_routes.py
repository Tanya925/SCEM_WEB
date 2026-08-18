# Main purpose: handle admin routes for the dashboard, content management, staff management, and project management.

from functools import wraps
from flask import Blueprint, redirect, render_template, request, session, url_for
from database.auth_db import get_user_by_id
from services.auth_service import (
    PasswordChangeError,
    reset_administrator_credentials,
)

from services.admin_service import (  
    get_general_info_page_context,
    get_projects_page_context,
    get_staff_page_context,
    handle_general_info_submission,
    handle_projects_submission,
    handle_staff_submission,
)

admin_bp = Blueprint("admin", __name__, url_prefix="/0630_SCEMadmin")

def login_required(view_function):
    """Require login and redirect to the credential-change page when necessary."""
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        if session.get("must_change_credentials"):
            return redirect(url_for("auth.change_credentials"))

        return view_function(*args, **kwargs)

    return wrapped_view

@admin_bp.route("/dashboard")
@login_required
def dashboard():
    """Render the admin dashboard together with the current user information."""
    current_user = get_user_by_id(session["user_id"])
    current_username = current_user["username"] if current_user else session.get("username", "User")
    session["username"] = current_username
    return render_template(
        "admin/dashboard.html",
        current_user_name=current_username,
    )

@admin_bp.route("/general-info", methods=["GET", "POST"])
@login_required
def general_info():
    """Render and process the homepage General Info admin page."""
    if request.method == "POST":
        success_message = handle_general_info_submission()
        return render_template("admin/general_info.html", **get_general_info_page_context(success_message))

    return render_template("admin/general_info.html", **get_general_info_page_context())

@admin_bp.route("/staff", methods=["GET", "POST"])
@login_required
def staff():
    """Render and process the staff management page."""
    edit_id = request.args.get("edit_id", type=int)

    if request.method == "POST":
        submission_result = handle_staff_submission()
        return render_template(
            "admin/staff.html",
            **get_staff_page_context(
                success_message=submission_result["success_message"],
                edit_id=None,
            ),
        )

    return render_template("admin/staff.html", **get_staff_page_context(edit_id=edit_id))

@admin_bp.route("/passwords", methods=["GET", "POST"])
@login_required
def passwords():
    """Handle administrator credential resets."""
    if request.method == "POST":
        user_id = request.form.get("user_id", type=int)
        try:
            restored_username = reset_administrator_credentials(user_id)
            target_user = get_user_by_id(user_id)
            target_name = target_user["display_name"] or target_user["username"]

            if user_id == session.get("user_id"):
                session.clear()
                return redirect(url_for("auth.login"))

            session["password_management_feedback"] = {
                "success_message": (
                    f"{target_name}'s account was reset. The initial username is "
                    f"{restored_username}. They must choose a new username and password after signing in."
                ),
                "error_message": None,
            }
        except PasswordChangeError as error:
            session["password_management_feedback"] = {
                "success_message": None,
                "error_message": str(error),
            }
        return redirect(url_for("admin.passwords"))

    feedback = session.pop("password_management_feedback", {})
    return render_template(
        "admin/passwords.html",
        admin_accounts=[get_user_by_id(session["user_id"])],
        success_message=feedback.get("success_message"),
        error_message=feedback.get("error_message"),
    )

@admin_bp.route("/projects", methods=["GET", "POST"])
@login_required
def projects():
    """Render and process the research-project management page."""
    edit_id = request.args.get("edit_id", type=int)

    if request.method == "POST":
        submission_result = handle_projects_submission()
        return render_template(
            "admin/projects.html",
            **get_projects_page_context(
                success_message=submission_result["success_message"],
                editing_project_override=submission_result["editing_project"],
            ),
        )

    return render_template("admin/projects.html", **get_projects_page_context(edit_id=edit_id))
