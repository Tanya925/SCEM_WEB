# Main purpose: handle administrator login, logout, and forced credential changes after reset or first login.

from flask import Blueprint, redirect, render_template, request, session, url_for
from services.auth_service import PasswordChangeError, authenticate_user, change_user_credentials

auth_bp = Blueprint("auth", __name__, url_prefix="/0630_SCEMadmin")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if "user_id" in session:
        if session.get("must_change_credentials"):
            return redirect(url_for("auth.change_credentials"))
        return redirect(url_for("admin.dashboard"))

    error_message = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            error_message = "Please enter your username and password."
        else:
            user = authenticate_user(username, password)
            if user is None:
                error_message = "Incorrect username or password."
            else:
                session.clear()
                session.permanent = True
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["display_name"] = user["display_name"] or user["username"]
                session["must_change_credentials"] = bool(user["must_change_credentials"])

                if session["must_change_credentials"]:
                    return redirect(url_for("auth.change_credentials"))
                return redirect(url_for("admin.dashboard"))

    return render_template("auth/admin_login.html", error_message=error_message)

@auth_bp.route("/change-credentials", methods=["GET", "POST"])
def change_credentials():
    
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    if not session.get("must_change_credentials"):
        return redirect(url_for("admin.dashboard"))

    error_message = None
    if request.method == "POST":
        try:
            new_username = request.form.get("new_username", "").strip()
            change_user_credentials(
                session["user_id"],
                request.form.get("current_password", ""),
                new_username,
                request.form.get("new_password", ""),
                request.form.get("confirm_password", ""),
            )
            session["username"] = new_username
            session["must_change_credentials"] = False
            return redirect(url_for("admin.dashboard"))
        except PasswordChangeError as error:
            error_message = str(error)

    return render_template(
        "auth/change_credentials.html",
        current_username=session.get("username", ""),
        error_message=error_message,
    )

@auth_bp.route("/logout")
def logout():
    """Clear the current session and log the user out of the admin interface."""
    session.clear()
    return redirect(url_for("auth.login"))
