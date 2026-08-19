# Main purpose: validate administrator credentials and update administrator account details.

from werkzeug.security import check_password_hash, generate_password_hash
from database.auth_db import (
    get_user_by_id,
    get_user_by_username,
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

# Update the administrator username, password, or both from the Set Up page.
def change_user_credentials(user_id, current_password, new_username, new_password, confirm_password):
    user = get_user_by_id(user_id)
    if user is None or not check_password_hash(user["password_hash"], current_password or ""):
        raise PasswordChangeError("Current password is incorrect.")
    cleaned_username = (new_username or "").strip() or user["username"]
    username_owner = get_user_by_username(cleaned_username)
    if username_owner is not None and username_owner["id"] != user_id:
        raise PasswordChangeError("This username is already in use.")

    password_hash_to_store = user["password_hash"]
    submitted_password = new_password or ""
    if submitted_password or (confirm_password or ""):
        if len(submitted_password) < 8:
            raise PasswordChangeError("New password must contain at least 8 characters.")
        if submitted_password != confirm_password:
            raise PasswordChangeError("New password and confirmation do not match.")
        if check_password_hash(user["password_hash"], submitted_password):
            raise PasswordChangeError("New password must be different from the current password.")
        password_hash_to_store = generate_password_hash(submitted_password)

    if cleaned_username == user["username"] and password_hash_to_store == user["password_hash"]:
        raise PasswordChangeError("Please change the username, password, or both before saving.")

    update_user_credentials(user_id, cleaned_username, password_hash_to_store)


