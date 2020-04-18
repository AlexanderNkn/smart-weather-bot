import logging


def _get_user_fullname(user):
    """Return username, first name and last name"""
    result = user.first_name
    if user.last_name:
        result += f" {user.last_name}"
    if user.username:
        result += f" (@{user.username})"
    return result


def log_update(update):
    request = update.message
    user = request.from_user

    log_msg = f"Request from {_get_user_fullname(user)}: {request.text}"
    logging.info(log_msg)
