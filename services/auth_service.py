# Main purpose: validate administrator credentials and handle the forced credential-change flow.

from werkzeug.security import check_password_hash, generate_password_hash
from database.auth_db import (
    get_user_by_id,
    get_user_by_username,
    reset_admin_credentials,
    update_user_credentials,
)

class PasswordChangeError(ValueError):
    pass

def authenticate_user(username, password):
    cleaned_username = (username or "").strip()
    if not cleaned_username or not password:
        return None

    user = get_user_by_username(cleaned_username)
    if user is None or not check_password_hash(user["password_hash"], password):
        return None

    return user

def change_user_credentials(user_id, current_password, new_username, new_password, confirm_password):
    """Replace temporary credentials with permanent ones and clear the forced-change state."""
    user = get_user_by_id(user_id)
    if user is None or not check_password_hash(user["password_hash"], current_password or ""):
        raise PasswordChangeError("Current password is incorrect.")
    cleaned_username = (new_username or "").strip()
    if not cleaned_username:
        raise PasswordChangeError("New username is required.")
    username_owner = get_user_by_username(cleaned_username)
    if username_owner is not None and username_owner["id"] != user_id:
        raise PasswordChangeError("This username is already in use.")
    if cleaned_username == user["username"]:
        raise PasswordChangeError("New username must be different from the temporary username.")
    if len(new_password or "") < 8:
        raise PasswordChangeError("New password must contain at least 8 characters.")
    if new_password != confirm_password:
        raise PasswordChangeError("New password and confirmation do not match.")
    if check_password_hash(user["password_hash"], new_password):
        raise PasswordChangeError("New password must be different from the current password.")

    update_user_credentials(user_id, cleaned_username, generate_password_hash(new_password))

def reset_administrator_credentials(user_id):
    """Reset administrator credentials to their defaults and require setup on the next login."""
    restored_username = reset_admin_credentials(user_id) if user_id else None
    if restored_username is None:
        raise PasswordChangeError(
            "Administrator account not found, or the initial username is already in use."
        )
    return restored_username
