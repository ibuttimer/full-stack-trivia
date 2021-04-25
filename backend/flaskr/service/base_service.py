from typing import Union, List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from werkzeug.exceptions import ServiceUnavailable

from .misc import QueryParam
from .session_scope import SessionScope
from ..model import AnyModel
from ..util import print_exc_info


def get_by_id(model: AnyModel, entity_id: int) -> Optional[AnyModel]:
    """
    Get an entity from the database
    :param model:       SQLAlchemy model
    :param entity_id:   id of entity
    :return: entity or None if entity does not exist
    """
    try:
        entity = model.query \
            .filter(model.id == entity_id) \
            .first()
    except SQLAlchemyError:
        print_exc_info()
        raise ServiceUnavailable()

    return entity


def get_entities(model: AnyModel, criteria=None, order_by=None, offset: int = 0, limit: int = None,
                 with_entities=None,
                 param: QueryParam = QueryParam.GET_ALL) -> Union[AnyModel, List[AnyModel], int]:
    """
    Search for entities.
    :param model:       SQLAlchemy model
    :param criteria:    orm criteria
    :param order_by:
    :param offset:      num records to skip
    :param limit:       max num records to return
    :param with_entities:   entities to return
    :param param:       query result to return
    :return: list of entities, entity, or count
    """
    # Do some sanity checks.
    if limit is not None and limit <= 0:
        raise ValueError(f'Invalid query limit: {limit}')
    if offset is None:
        offset = 0
    if offset < 0:
        raise ValueError(f'Invalid query offset: {offset}')

    if param == QueryParam.GET_FIRST:
        result = None
    elif param == QueryParam.GET_ALL:
        result = []
    elif param == QueryParam.COUNT:
        result = 0
    else:
        raise ValueError(f'QueryParam not supported: {param}')

    try:
        query = model.query

        if with_entities is not None:
            query = query.with_entities(with_entities)
        if criteria is not None:
            query = query.filter(criteria)
        if order_by is not None:
            query = query.order_by(order_by)
        if offset > 0:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        if param == QueryParam.GET_FIRST:
            result = query.first()
        elif param == QueryParam.GET_ALL:
            result = query.all()
        elif param == QueryParam.COUNT:
            result = query.count()

    except SQLAlchemyError:
        print_exc_info()
        raise ServiceUnavailable()

    return result


def create_entity(model: AnyModel, session_scope: SessionScope = None) -> int:
    """
    Create an entity
    :param model:       SQLAlchemy model
    :param session_scope:   scoped session
    :return: number of affected entities
    """
    session_scope = SessionScope.select_scope(session_scope)
    with session_scope.scope() as session:
        session.add(model)

        session_scope.add_result(1)

    return session_scope.op_result()


def _get_entity(model: AnyModel, session: Session, criteria=None,
                param: QueryParam = QueryParam.GET_ALL) -> Union[AnyModel, List, int]:
    """
    Update an entity.
    :param model:       SQLAlchemy model
    :param criteria:    entity filter criteria
    :return: number of affected entities
    """
    select_query = session.query(model)
    if criteria is not None:
        select_query = select_query.filter(criteria)

    if param == QueryParam.GET_FIRST:
        result = select_query.first()
    elif param == QueryParam.GET_ALL:
        result = select_query.all()
    elif param == QueryParam.COUNT:
        result = select_query.count()
    else:
        raise ValueError(f'QueryParam not supported: {param}')

    return result


def get_entity(model: AnyModel, criteria=None, param: QueryParam = QueryParam.GET_ALL,
               session_scope: SessionScope = None) -> int:
    """
    Update an entity.
    :param model:       SQLAlchemy model
    :param criteria:    entity filter criteria
    :param param:       query result to return
    :param session_scope:   scoped session
    :return: number of affected entities
    """
    session_scope = SessionScope.select_scope(session_scope)
    if session_scope.is_single_use():
        # Just for this operation, so create a scope.
        with session_scope.scope() as session:
            session_scope.add_result(
                _get_entity(model, session, criteria=criteria, param=param)
            )
    else:
        # Already scoped, use existing.
        session_scope.add_result(
            _get_entity(model, session_scope.session(), criteria=criteria, param=param)
        )

    return session_scope.op_result()


def _update_entity(model: AnyModel, session: Session, updates: dict, criteria=None) -> int:
    """
    Update an entity
    :param model:       SQLAlchemy model
    :param updates:     updates to apply
    :param criteria:    entity filter criteria
    :return: number of affected entities
    """
    update_query = session.query(model)
    if criteria is not None:
        update_query = update_query.filter(criteria)

    count = update_query.count()    # Number of rows that will be affected.
    update_query.update(updates, synchronize_session="fetch")

    return count


def update_entity(model: AnyModel, updates: dict, criteria=None, session_scope: SessionScope = None) -> int:
    """
    Update an entity
    :param model:       SQLAlchemy model
    :param updates:     updates to apply
    :param criteria:    entity filter criteria
    :param session_scope:   scoped session
    :param session_scope:   scoped session
    :return: number of affected entities
    """
    session_scope = SessionScope.select_scope(session_scope)
    if session_scope.is_single_use():
        # Just for this operation, so create a scope.
        with session_scope.scope() as session:
            session_scope.add_result(
                _update_entity(model, session, updates, criteria=criteria)
            )
    else:
        # Already scoped, use existing.
        session_scope.add_result(
            _update_entity(model, session_scope.session(), updates, criteria=criteria)
        )

    return session_scope.op_result()


def _delete_entity(model: AnyModel, session: Session) -> int:
    """
    Delete an entity.
    :param model:       SQLAlchemy model
    :return: number of affected entities
    """
    session.delete(model)
    return 1


def delete_entity(model: AnyModel, session_scope: SessionScope = None) -> int:
    """
    Delete an entity.
    :param model:       SQLAlchemy model
    :param session_scope:   scoped session
    :return: number of affected entities
    """
    session_scope = SessionScope.select_scope(session_scope)
    if session_scope.is_single_use():
        # Just for this operation, so create a scope.
        with session_scope.scope() as session:
            session_scope.add_result(
                _delete_entity(model, session)
            )
    else:
        # Already scoped, use existing.
        session_scope.add_result(
            _delete_entity(model, session_scope.session())
        )

    return session_scope.op_result()
