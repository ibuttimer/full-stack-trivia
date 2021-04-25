from backend.flaskr.model import Category
from .base_service import get_by_id, get_entities
from .misc import QueryParam


def get_category_by_id(category_id: int):
    """
    Get a category.
    :param category_id: id of category
    :return: category or None if category does not exist
    """
    return get_by_id(Category, category_id)


def get_categories(criteria=None, order_by=None, offset: int = 0, limit: int = None,
                   param: QueryParam = QueryParam.GET_ALL):
    """
    Search for a category.
    :param criteria:    orm criteria
    :param order_by:
    :param offset:      num records to skip
    :param limit:       max num records to return
    :param param:       query result to return
    :return: list of categories, or count
    """
    return get_entities(Category, criteria=criteria, order_by=order_by, offset=offset, limit=limit, param=param)


def get_categories_as_map():
    """
    Get all categories as a map with id as the key.
    :return: map of categories
    """
    categories = get_entities(Category)
    return {k: v for k, v in [category.map_kv() for category in categories]}


def search_category_by_name(category_name: str):
    """
    Search for a category.
    :param category_name: name/partial name of category
    :return: list of categories
    """
    return get_categories(
        criteria=Category.name.ilike("%" + category_name + "%"), order_by=Category.name)
