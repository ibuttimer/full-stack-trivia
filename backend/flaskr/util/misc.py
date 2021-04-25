import traceback
from http import HTTPStatus

from flask import request, abort, jsonify

from .constants import REQ_ARG_PAGE, REQ_ARG_PER_PAGE, REQ_ARG_PAGINATION, REQ_ARG_TYPE, ENTITY_TYPE
from .app_cfg import max_items_per_page


def get_request_arg(arg: str, default: int) -> int:
    """
    Get a positive integer argument from the request arguments.
    :param arg:     argument name
    :param default: default value
    :return:
    """
    req_arg = request.args.get(arg, default, type=int)
    if req_arg < 1:
        abort(HTTPStatus.BAD_REQUEST.value)
    return req_arg


def get_request_page() -> int:
    """
    Get the page number from the request arguments.
    :return:
    """
    return get_request_arg(REQ_ARG_PAGE, 1)


def get_request_per_page(default: int) -> int:
    """
    Get the items per page from the request arguments.
    :param default:     default value if not specified in request
    :return:
    """
    per_page = request.args.get(REQ_ARG_PER_PAGE, default, type=int)
    if per_page < 1:
        abort(HTTPStatus.BAD_REQUEST.value)
    max_items = max_items_per_page()
    return per_page if per_page <= max_items else max_items


def get_request_pagination() -> bool:
    """
    Get the pagination flag from the request arguments; 'y' or 'n'.
    :return:
    """
    req_pagination = request.args.get(REQ_ARG_PAGINATION, 'y', type=str)
    return True if req_pagination.lower() == 'y' else False


def get_request_type() -> str:
    """
    Get the entity response type from the request arguments; 'entity' or 'map'.
    :return:
    """
    req_type = request.args.get(REQ_ARG_TYPE, ENTITY_TYPE, type=str)
    return req_type.lower()


def pagination(page: int, num_per_page: int, total: int) -> (int, int, int, str):
    """
    Get pagination data.
    :param page:            requested page
    :param num_per_page:    items per page
    :param total:           total number of items
    :return: tuple of offset for start, limit for end, result code, error message
    """
    code = HTTPStatus.OK.value
    msg = None
    offset = num_per_page * (page - 1)
    limit = num_per_page * page

    if offset > total:
        code = HTTPStatus.BAD_REQUEST.value
        msg = 'Not a valid page number'
    elif limit > total:
        limit = total

    return offset, limit, code, msg


def _make_result(success: bool, error: int = None, message: str = None, **kwargs):
    """
    Make a json result.
    :param success: True or False
    :param error:   if success == False, HTTP error code
    :param message: if success == False, HTTP error message
    :param kwargs:  result data as key/value pairs
    :return:
    """
    result = {
        'success': success
    }
    if error is not None:
        result["error"] = error
        result["message"] = message if message is not None else ''

    result = {**result, **kwargs}

    return jsonify(result)


def success_result(**kwargs):
    """
    Make a success json result.
    :param kwargs:  result data as key/value pairs
    :return:
    """
    return _make_result(True, **kwargs)


def key_or_alias(key: str, aliases: dict) -> str:
    alias = key
    if aliases is not None and key in aliases.keys():
        alias = aliases[key]
    return alias


def paginated_success_result(data: list, page: int, per_page: int, total: int, offset: int, limit: int,
                             aliases: dict = None, **kwargs):
    """
    Make a paginated json result
    :param data:        result data
    :param page:        requested page
    :param per_page:    items per page
    :param total:       total number of items
    :param offset:      offset of start of data
    :param limit:       limit of end of data
    :param aliases:     dict of aliases for standard body fields
    :param kwargs:      optional additional entries to include
    :return:
    """
    num_pages = int(total / per_page)
    if num_pages * per_page < total:
        num_pages = num_pages + 1

    result = {
        key_or_alias("data", aliases): data,
        key_or_alias("page", aliases): page,
        key_or_alias("per_page", aliases): per_page,
        key_or_alias("num_pages", aliases): num_pages,
        key_or_alias("total", aliases): total,
        key_or_alias("offset", aliases): offset,
        key_or_alias("limit", aliases): limit
    }
    return success_result(**{
        **result, **kwargs
    })


def error_result(error: int, message: str, **kwargs):
    """
    Make a fail json result.
    :param error:   if success == False, HTTP error code
    :param message: if success == False, HTTP error message
    :param kwargs:  result data as key/value pairs
    :return:
    """
    return _make_result(False, error=error, message=message, **kwargs)


def http_error_result(http_code: HTTPStatus, error):
    """
    Make a fail json result.
    :param http_code:  HTTP status code
    :param error:      error exception
    :return:
    """
    if "data" in vars(error):
        extra = error.data
    else:
        extra = {}
    return error_result(http_code.value, http_code.phrase, **extra), http_code.value


def print_exc_info():
    """ Print exception information. """
    for line in traceback.format_exc().splitlines():
        print(line)
