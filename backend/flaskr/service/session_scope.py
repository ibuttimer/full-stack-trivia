from contextlib import contextmanager
from enum import Enum
from http import HTTPStatus
from typing import Any

from flask_restful import abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from werkzeug.exceptions import ServiceUnavailable

from backend.flaskr.model.models import db
from backend.flaskr.util import print_exc_info


class SessionScopeArgs(Enum):
    SINGLE_USE = 1
    MULTI_USE = 2


class SessionScope(object):
    """
    Class providing a context managed SQLAlchemy session.
    :param use: single or multi-use session flag
    """

    def __init__(self, use: SessionScopeArgs = SessionScopeArgs.SINGLE_USE):
        self.use = use
        self.result_stack = []
        self.is_success = False
        self.active_session = None

    @contextmanager
    def scope(self):
        """Provide a transactional scope around a series of operations."""
        self.active_session = db.session
        try:
            yield self.active_session
            self.active_session.commit()
            self.is_success = True

        except SQLAlchemyError as e:
            self.active_session.rollback()
            print_exc_info()
            if isinstance(e, IntegrityError):
                abort(HTTPStatus.UNPROCESSABLE_ENTITY, detailed_message="Conflicts with existing entry")
            else:
                raise ServiceUnavailable()

        finally:
            self.active_session.close()

    def session(self) -> Session:
        return self.active_session()

    def was_success(self) -> bool:
        return self.is_success

    def add_result(self, result: Any):
        """
        Add result to the result stack.
        :param result:  result
        :return:
        """
        return self.result_stack.append(result)

    def pop_result(self) -> Any:
        """
        Pop result from the result stack.
        :return:
        """
        if len(self.result_stack) > 0:
            result = self.result_stack.pop()
        else:
            result = None
        return result

    def peek_result(self) -> Any:
        """
        Peek at the last result on the result stack.
        :return:
        """
        if len(self.result_stack) > 0:
            result = self.result_stack[-1]
        else:
            result = None
        return result

    def op_result(self) -> Any:
        """
        Result of last operation.
        :return:
        """
        if self.use == SessionScopeArgs.SINGLE_USE:
            result = self.pop_result()
        else:
            result = self.peek_result()
        return result

    def is_single_use(self):
        return self.use == SessionScopeArgs.SINGLE_USE

    @staticmethod
    def select_scope(scope):
        if scope is None:
            scope = SessionScope()
        elif not isinstance(scope, SessionScope):
            raise ValueError("Expected SessionScope object")

        return scope

