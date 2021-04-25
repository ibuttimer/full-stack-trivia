from http import HTTPStatus

from flask import request, make_response
from flask_restful import abort

from ..model import Question, Category
from ..service import (get_question_by_id, QueryParam, search_question_by_category_id, get_questions,
                       get_categories_as_map, search_question_by_question_text, create_question as create_question_srvc,
                       delete_question
                       )
from ..util import (get_request_page, get_request_per_page, pagination, success_result,
                    paginated_success_result, questions_per_page, QUESTION_RESPONSE_ALIASES,
                    QUESTION_SEARCH_TERM
                    )


def all_questions():
    """
    Get all questions.
    :return: paginated list of questions,
             number of total questions,
             categories

    Request arguments:
    page:       requested page number
    per_page:   number of entries per page
    """
    page = get_request_page()
    per_page = get_request_per_page(questions_per_page())

    total = get_questions(order_by=Question.id, param=QueryParam.COUNT)

    if total > 0:
        offset, limit, code, msg = pagination(page, per_page, total)

        if code != HTTPStatus.OK.value:
            # pagination error
            abort(code)

        questions = get_questions(order_by=Question.id, param=QueryParam.GET_ALL, offset=offset, limit=per_page)

    else:
        questions = []
        offset = limit = 0

    return paginated_success_result(
        data=[question.format() for question in questions],
        page=page,
        per_page=per_page,
        total=total,
        offset=offset,
        limit=limit,
        aliases=QUESTION_RESPONSE_ALIASES,
        # additional elements
        categories=get_categories_as_map()
    )


def _get_question_by_id(question_id: int):
    """
    Get a question.
    :param question_id: id of question
    :return: question or abort if question does not exist
    """
    question = get_question_by_id(question_id)
    if question is None:
        abort(HTTPStatus.NOT_FOUND.value)

    return question


def question_by_id(question_id: int):
    """
    Get a question.
    :param question_id: id of question
    :return:
    """
    is_delete = (request.method == 'DELETE')
    is_get = (request.method == 'GET')

    question = _get_question_by_id(question_id)

    if is_get:
        response = success_result(question=question.format())
    elif is_delete:
        response = success_result(
            deleted=delete_question(question=question)
        )
    else:
        raise NotImplemented

    return response


def qc_questions_by_category_id(category: Category):
    """
    Get questions for a category.
    Note: No category validity check is performed
    :param category:    category
    :return:
    """
    page = get_request_page()
    per_page = get_request_per_page(questions_per_page())

    total = search_question_by_category_id(category.id, param=QueryParam.COUNT)

    if total > 0:
        offset, limit, code, msg = pagination(page, per_page, total)

        if code != HTTPStatus.OK.value:
            # pagination error
            abort(code)

        questions = search_question_by_category_id(category.id, order_by=Question.id, offset=offset, limit=per_page,
                                                   param=QueryParam.GET_ALL)

    else:
        questions = []
        offset = limit = 0

    return paginated_success_result(
        data=[question.format() for question in questions],
        page=page,
        per_page=per_page,
        total=total,
        offset=offset,
        limit=limit,
        aliases=QUESTION_RESPONSE_ALIASES,
        # additional elements
        categories=get_categories_as_map(),
        current_category=category.id
    )


def create_question():
    """
    Create a question.
    :return:
    """
    num_affected = create_question_srvc(
        request.get_json())

    return make_response(
        success_result(created=num_affected), HTTPStatus.CREATED)


def search_questions():
    """
    Search for questions.
    :return: paginated list of questions,
             number of total questions,
             current category, # TODO not used?
             categories

    Request arguments:
    page:       requested page number
    per_page:   number of entries per page

    Request form:
    searchTerm: question search term
    """
    page = get_request_page()
    per_page = get_request_per_page(questions_per_page())

    data = request.get_json()
    search_term = data[QUESTION_SEARCH_TERM] if QUESTION_SEARCH_TERM in data else ''

    total = search_question_by_question_text(search_term, param=QueryParam.COUNT)

    if total > 0:
        offset, limit, code, msg = pagination(page, per_page, total)

        if code != HTTPStatus.OK.value:
            # pagination error
            abort(code)

        questions = search_question_by_question_text(search_term, order_by=Question.id, offset=offset, limit=per_page,
                                                     param=QueryParam.GET_ALL)

    else:
        questions = []
        offset = limit = 0

    return paginated_success_result(
        data=[question.format() for question in questions],
        page=page,
        per_page=per_page,
        total=total,
        offset=offset,
        limit=limit,
        aliases=QUESTION_RESPONSE_ALIASES,
        # additional elements
        categories=get_categories_as_map()
    )


