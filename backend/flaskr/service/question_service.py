import random
from http import HTTPStatus
from typing import Union, List

from flask_restful import abort
from sqlalchemy import and_

from backend.flaskr.model import Question, M_ID, M_QUESTION, M_ANSWER, M_CATEGORY, M_DIFFICULTY, M_TYPE

from backend.flaskr.util import MIN_DIFFICULTY, MAX_DIFFICULTY

from .base_service import get_by_id, get_entities, create_entity, delete_entity
from .category_service import get_category_by_id
from .misc import QueryParam


def get_question_by_id(question_id: int) -> Question:
    """
    Get a question.
    :param question_id: id of question
    :return: question or None if question does not exist
    """
    return get_by_id(Question, question_id)


def get_questions(criteria=None, order_by=None, offset: int = 0, limit: int = None,
                  with_entities=None,
                  param: QueryParam = QueryParam.GET_ALL) -> Union[Question, List[Question], int]:
    """
    Search for questions.
    :param criteria:    orm criteria
    :param order_by:    order by criteria
    :param offset:      num records to skip
    :param limit:       max num records to return
    :param with_entities:   entities to return
    :param param:       query result to return
    :return: list of questions, or count
    """
    return get_entities(Question, criteria=criteria, order_by=order_by, offset=offset, limit=limit,
                        with_entities=with_entities, param=param)


def search_question_by_category_id(category_id: int, order_by=None, offset: int = 0, limit: int = None,
                                   param: QueryParam = QueryParam.GET_ALL) -> Union[Question, List[Question], int]:
    """
    Get questions for a category.
    Note: No category validity check is performed
    :param category_id: id of category
    :param order_by:    order by criteria
    :param offset:      num records to skip
    :param limit:       max num records to return
    :param param:       query result to return
    :return: list of questions, or count
    """
    return get_questions(criteria=Question.category == category_id,
                         order_by=order_by, offset=offset, limit=limit, param=param)


def search_question_by_question_text(question_text: str, order_by=None, offset: int = 0, limit: int = None,
                                     param: QueryParam = QueryParam.GET_ALL) -> Union[Question, List[Question], int]:
    """
    Search for questions.
    :param question_text: text to be included in question text
    :param order_by:    order by criteria
    :param offset:      num records to skip
    :param limit:       max num records to return
    :param param:       query result to return
    :return: list of questions, or count
    """
    return get_questions(criteria=Question.question.ilike("%" + question_text + "%"),
                         order_by=order_by, offset=offset, limit=limit, param=param)


def get_random_questions(criteria=None, offset: int = 0, limit: int = None, pick: int = 0,
                         param: QueryParam = QueryParam.GET_ALL) -> Union[Question, List[Question], int]:
    """
    Search for questions.
    :param criteria:    orm criteria
    :param offset:      num records to skip
    :param limit:       max num records to return
    :param pick:        number of random picks to make from records
    :param param:       query result to return
    :return: list of questions
    """
    # get all the ids, pick randomly from those and get the corresponding questions
    query_result = get_questions(criteria=criteria, offset=offset, limit=limit, with_entities=Question.id,
                                 param=QueryParam.GET_ALL)

    if len(query_result) > 0:
        if param == QueryParam.GET_FIRST:   # same as pick=1
            indices = [
                # element 0 (i.e. id) of tuple at random index
                query_result[random.randrange(0, len(query_result))][0]
            ]
        elif param == QueryParam.GET_ALL:
            indices = []
            if pick < len(query_result):
                # pick random
                picked = 0
                while picked < pick:
                    index = random.randrange(0, len(query_result))
                    if index not in indices:
                        indices.append(index)
                        picked = picked + 1
            else:
                # return all
                indices = list(range(len(query_result)))

            indices = [
                # element 0 (i.e. id) of tuple at random index
                query_result[index][0] for index in indices
            ]
        else:
            raise ValueError(f'QueryParam not supported: {param}')

        pick_criteria = and_(
            Question.id.in_(indices),
            criteria
        ) if criteria is not None else Question.id.in_(indices)

        result = get_questions(criteria=pick_criteria, offset=offset, limit=limit, param=QueryParam.GET_ALL)

    else:
        result = []

    return result


def create_question(question: dict) -> int:
    """
    Create a question.
    :param question:    question to create
    :return: number of affected entities
    """
    # validate input
    error = None
    if isinstance(question, dict):
        for key in [M_QUESTION, M_ANSWER, M_DIFFICULTY, M_CATEGORY]:
            if key not in question.keys():
                error = f'Missing {key} data'
            else:
                value = question[key]

                if key in [M_QUESTION, M_ANSWER]:
                    if len(value.strip()) == 0:
                        error = f'Empty {key} data'
                elif key in [M_DIFFICULTY, M_CATEGORY]:
                    if isinstance(value, str):
                        if not value.isnumeric():
                            error = f'Expected {key} data as int'
                    elif not isinstance(value, int):
                        error = f'Expected {key} data as int'
                    elif key == M_DIFFICULTY:
                        if not MIN_DIFFICULTY <= question[M_DIFFICULTY] <= MAX_DIFFICULTY:
                            error = f'Out of range value for difficulty'

            if error is not None:
                break

    else:
        error = f'Invalid data'

    if error is not None:
        abort(HTTPStatus.BAD_REQUEST.value, detailed_message=error)

    category = get_category_by_id(int(question[M_CATEGORY]))
    if category is None:
        abort(HTTPStatus.BAD_REQUEST.value, detailed_message="Unknown category")

    return create_entity(
        Question(question=question[M_QUESTION].strip(), answer=question[M_ANSWER].strip(),
                 difficulty=question[M_DIFFICULTY], category=int(question[M_CATEGORY]))
    )


def delete_question(question_id: int = None, question: Question = None):
    """
    Delete a question.
    :param question_id: id of question
    :param question:    question model
    :return: number of affected entities
    """
    if question_id is not None:
        question = get_by_id(Question, question_id)
    elif question is None:
        raise ValueError()
    return delete_entity(question)
