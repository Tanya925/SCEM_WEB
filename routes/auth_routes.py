# Main purpose: handle administrator login and logout.

from flask import Blueprint, redirect, render_template, request, session, url_for
from services.auth_service import authenticate_user

auth_bp = Blueprint("auth", __name__, url_prefix="/0630_SCEMadmin")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if "user_id" in session:
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
                return redirect(url_for("admin.dashboard"))

    return render_template("auth/admin_login.html", error_message=error_message)

@auth_bp.route("/logout")
def logout():
    """Clear the current session and log the user out of the admin interface."""
    session.clear()
    return redirect(url_for("auth.login"))
