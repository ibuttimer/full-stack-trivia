from http import HTTPStatus
from typing import Optional

from flask_restful import abort

from backend.flaskr.model import User, M_USERNAME, M_PASSWORD, M_NUM_QUESTIONS, M_NUM_CORRECT, M_ID, USER_FIELDS
from .base_service import get_by_id, get_entity, get_entities, create_entity, update_entity
from .misc import QueryParam
from .session_scope import SessionScope, SessionScopeArgs


def get_user_by_id(user_id: int, session_scope: SessionScope = None) -> Optional[User]:
    """
    Get a user.
    :param user_id:         id of category
    :param session_scope:   scoped session
    :return: user or None if user does not exist
    """
    if session_scope is None:
        result = get_by_id(User, user_id)
    else:
        result = get_entity(User, criteria=User.id == user_id, param=QueryParam.GET_FIRST, session_scope=session_scope)
    return result


def get_user_by_username(username: str):
    """
    Get a user.
    :param username: username of user
    :return: user or None if user does not exist
    """
    return get_entities(User, criteria=User.username == username, param=QueryParam.GET_FIRST)


def get_users(criteria=None, order_by=None, offset: int = 0, limit: int = None,
              param: QueryParam = QueryParam.GET_ALL):
    """
    Search for a user(s).
    :param criteria:    orm criteria
    :param order_by:
    :param offset:      num records to skip
    :param limit:       max num records to return
    :param param:       query result to return
    :return: list of users, or count
    """
    return get_entities(User, criteria=criteria, order_by=order_by, offset=offset, limit=limit, param=param)


def create_user(user: dict) -> int:
    """
    Create a user.
    :param user:    user to create
    :return: number of affected entities
    """
    # validate input
    error = None
    if isinstance(user, dict):

        for key in [M_USERNAME, M_PASSWORD]:
            if key not in user.keys():
                error = f'Missing {key} data'
            else:
                value = user[key]

                if key in [M_USERNAME, M_PASSWORD]:
                    if len(value.strip()) == 0:
                        error = f'Empty {key} data'

            if error is not None:
                break

    else:
        error = f'Invalid data'

    if error is not None:
        abort(HTTPStatus.BAD_REQUEST.value, detailed_message=error)

    return create_entity(
        User(username=user[M_USERNAME].strip(), password=user[M_PASSWORD].strip())
    )


def update_user_by_id(user_id: int, updates: dict, op: QueryParam = QueryParam.UPDATE_ADD) -> dict:
    """
    Update a user.
    :param user_id: id of category
    :param updates: updates to apply
    :param op:      operation to perform on numeric data field in user model
    :return: number of affected entities
    """
    # validate input
    error = None
    if isinstance(updates, dict):
        for key in updates.keys():
            if key not in USER_FIELDS:
                error = f'Unexpected data {key}'
                break
        else:
            if M_ID in updates.keys():
                if updates[M_ID] != user_id:
                    error = f'Illegal operation, unable to update {M_ID}'
                else:
                    updates.pop(M_ID)
    else:
        error = f'Invalid data'

    if error is not None:
        abort(HTTPStatus.BAD_REQUEST.value, detailed_message=error)

    # Use same session for all sub operations.
    session_scope = SessionScope(use=SessionScopeArgs.MULTI_USE)
    with session_scope.scope() as session:
        user = get_user_by_id(user_id, session_scope=session_scope)
        if user is None:
            abort(HTTPStatus.NOT_FOUND.value)

        if op == QueryParam.UPDATE_ADD:
            update_values = {**updates}
            user_dict = user.format()
            for key in [M_NUM_CORRECT, M_NUM_QUESTIONS]:
                if key in update_values.keys():
                    update_values[key] = user_dict[key] + update_values[key]
        else:
            update_values = updates

        result = update_entity(
                    User, update_values, criteria=User.id == user_id, session_scope=session_scope
                )
        formatted_user = get_user_by_id(user_id, session_scope=session_scope).format()

    return {k: v for k, v in formatted_user.items() if k != M_PASSWORD}


def login_or_register_user(username: str, password: str) -> dict:
    """
    Login or register a user.
    :param username:    username
    :param password:    password
    :return: number of affected entities
    """
    # validate input
    if username is None or len(username.strip()) == 0:
        abort(HTTPStatus.BAD_REQUEST.value, detailed_message="Username required")
    if password is None or len(password.strip()) == 0:
        abort(HTTPStatus.BAD_REQUEST.value, detailed_message="Password required")

    user = get_user_by_username(username)

    if user is None:
        create_user({
            M_USERNAME: username, M_PASSWORD: password
        })
        user = get_user_by_username(username)

    if user.password != password:
        abort(HTTPStatus.UNAUTHORIZED.value, detailed_message="Invalid username or password")

    return {k: v for k, v in user.format().items() if k != M_PASSWORD}
