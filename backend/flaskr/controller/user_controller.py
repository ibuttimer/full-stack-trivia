from flask import request

from ..service import login_or_register_user
from ..util import success_result, USERNAME, PASSWORD


def login():
    """
    Login or register a user
    :return:

    Request body:
    username: username
    password: password
    """
    data = request.get_json()
    username = data[USERNAME] if USERNAME in data else None
    password = data[PASSWORD] if PASSWORD in data else None

    result = {
        'user': login_or_register_user(username, password)
    }
    return success_result(**result)
