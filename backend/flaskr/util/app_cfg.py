from typing import Any

from flask import Config


__APP_CONFIG__: Config = None


def set_config(config: Config):
    """
    Set the configuration for the application.
    :param config:
    :return:
    """
    global __APP_CONFIG__
    __APP_CONFIG__ = config


def get_config(option: str):
    """
    Get a configuration option.
    :param option: name of option
    :return:
    """
    if __APP_CONFIG__ is None:
        raise ValueError("Application configuration not set")
    return __APP_CONFIG__.get(option)


def is_configured():
    """
    Check if application is configured.
    :return:
    """
    return __APP_CONFIG__ is not None


__CATEGORIES_PER_PAGE__ = None
__QUESTIONS_PER_PAGE__ = None
__MAX_ITEMS_PER_PAGE__ = None


def _get_setting(current: Any, name: str):
    """ Get a setting. """
    set_it = False
    if current is None and is_configured():
        current = get_config(name)
        set_it = True
    return current, set_it


def categories_per_page():
    """ Get the categories per page setting. """
    global __CATEGORIES_PER_PAGE__
    current, set_it = _get_setting(__CATEGORIES_PER_PAGE__, "CATEGORIES_PER_PAGE")
    if set_it:
        __CATEGORIES_PER_PAGE__ = current
    return current


def questions_per_page():
    """ Get the questions per page setting. """
    global __QUESTIONS_PER_PAGE__
    current, set_it = _get_setting(__QUESTIONS_PER_PAGE__, "QUESTIONS_PER_PAGE")
    if set_it:
        __QUESTIONS_PER_PAGE__ = current
    return current


def max_items_per_page():
    """ Get the max items per page setting. """
    global __MAX_ITEMS_PER_PAGE__
    current, set_it = _get_setting(__MAX_ITEMS_PER_PAGE__, "MAX_ITEMS_PER_PAGE")
    if set_it:
        __MAX_ITEMS_PER_PAGE__ = current
    return current

