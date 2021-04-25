from http import HTTPStatus

from flask_restful import abort

from backend.flaskr.model import Category

from backend.flaskr.util import (get_request_page, get_request_per_page, get_request_pagination, get_request_type,
                                 pagination, success_result, key_or_alias,
                                 paginated_success_result, categories_per_page, CATEGORY_RESPONSE_ALIASES, MAP_TYPE
                                 )
from backend.flaskr.service import get_category_by_id, get_categories, QueryParam
from .question_controller import qc_questions_by_category_id


def all_categories():
    """
    Get all categories.
    :return:

    Request arguments:
    page:           requested page number
    per_page:       number of entries per page
    pagination:     pagination flag; y/n
    type:           entity response type; entity or map
    """
    page = get_request_page()
    per_page = get_request_per_page(categories_per_page())
    paginate = get_request_pagination()
    rsp_type = get_request_type()

    total = get_categories(param=QueryParam.COUNT)

    if total > 0:
        if paginate:
            offset, limit, code, msg = pagination(page, per_page, total)

            if code != HTTPStatus.OK.value:
                # pagination error
                abort(code)

        else:
            offset = 0
            per_page = None
            limit = total

        categories = get_categories(order_by=Category.id, param=QueryParam.GET_ALL, offset=offset, limit=per_page)

    else:
        categories = []
        offset = limit = 0

    if rsp_type == MAP_TYPE:
        # generate a dict with id as key and the type as value
        data = {str(k): v for k, v in map(lambda x: x.map_kv(), categories)}
    else:
        # generate a list of entities
        data = [category.format() for category in categories]

    if paginate:
        result = paginated_success_result(
            data=data,
            page=page,
            per_page=per_page,
            total=total,
            offset=offset,
            limit=limit,
            aliases=CATEGORY_RESPONSE_ALIASES
        )
    else:
        result_args = {
            key_or_alias("data", CATEGORY_RESPONSE_ALIASES): data
        }
        result = success_result(**result_args)

    return result


def _get_category_by_id(category_id: int):
    """
    Get a category.
    :param category_id: id of category
    :return: category or abort if category does not exist
    """
    category = get_category_by_id(category_id)
    if category is None:
        abort(HTTPStatus.NOT_FOUND.value)
    return category


def category_by_id(category_id: int):
    """
    Get a category.
    :param category_id: id of category
    :return:
    """
    category = _get_category_by_id(category_id)
    return success_result(category=category.format())


def questions_by_category_id(category_id: int):
    """
    Get questions for a category.
    :param category_id: id of category
    :return:
    """
    category = _get_category_by_id(category_id)     # to verify valid category

    return qc_questions_by_category_id(category)


