import json
import unittest
from http import HTTPStatus
from typing import Union, Any

from flask import Response
from flask_sqlalchemy import SQLAlchemy

from backend import test_config
from backend.flaskr import create_app, key_or_alias
from backend.flaskr.model import setup_db
from backend.test.test_data import EqualDataMixin

from .misc import MatchParam


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(test_config=test_config)
        self.app.testing = True
        self.client = self.app.test_client()
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.max_items_per_page = test_config.MAX_ITEMS_PER_PAGE

    def tearDown(self):
        """Executed after reach test"""
        pass

    def assert_ok(self, status_code: int, msg=None):
        self.assertEqual(HTTPStatus.OK.value, status_code, msg=msg)

    def assert_created(self, status_code: int, msg=None):
        self.assertEqual(HTTPStatus.CREATED.value, status_code, msg=msg)

    def assert_bad_request(self, status_code: int, msg=None):
        self.assertEqual(HTTPStatus.BAD_REQUEST.value, status_code, msg=msg)

    def assert_unauthorized_request(self, status_code: int, msg=None):
        self.assertEqual(HTTPStatus.UNAUTHORIZED.value, status_code, msg=msg)

    def assert_not_found(self, status_code: int, msg=None):
        self.assertEqual(HTTPStatus.NOT_FOUND.value, status_code, msg=msg)

    def assert_equal_data(self, expected: EqualDataMixin, actual: dict, ignore: list = None):
        """
        Test item quality
        :param expected:    expected value
        :param actual:      actual value
        :param ignore:      list of attributes to ignore
        """
        self.assertTrue(expected.equals(actual, ignore=ignore), msg=f'{expected} != {actual}')

    def assert_data_array(self, expected: list[EqualDataMixin], actual: list[dict],
                          offset: int = 0, limit: int = None, ignore: list = None):
        """
        Test an item array
        :param expected:    expected value
        :param actual:      actual value
        :param offset:      offset of start of data
        :param limit:       limit of end of data
        :param ignore:      list of attributes to ignore
        """
        if limit is None:
            limit = len(expected) - offset
        expected_slice = expected[offset:limit]

        self.assertEqual(len(expected_slice), len(actual), f'actual length != expected length')

        for index in range(limit - offset):
            self.assert_equal_data(expected_slice[index], actual[index], ignore=ignore)

    def assert_body_entry(self, resp_body: dict, key: str, *args, value: Any = None, msg=None):
        """
        Check a success response
        :param resp_body:   response body
        :param key:         key for entry
        :param value:       expected value
        :param match:       match type to check
        :param msg:         assert error message
        """
        self.assertTrue(key in resp_body.keys(), msg=msg)

        resp_value = resp_body[key]
        expected_value = value
        if MatchParam.CASE_INSENSITIVE in args:
            resp_value = resp_body[key].lower()
            expected_value = value.lower()
        elif MatchParam.TO_INT in args:
            resp_value = int(resp_value)

        if MatchParam.EQUAL in args:
            self.assertEqual(expected_value, resp_value, msg=msg)
        elif MatchParam.NOT_EQUAL in args:
            self.assertNotEqual(expected_value, resp_value, msg=msg)
        elif MatchParam.TRUE in args:
            self.assertTrue(resp_value, msg=msg)
        elif MatchParam.FALSE in args:
            self.assertFalse(resp_value, msg=msg)
        elif MatchParam.IN in args:
            self.assertIn(resp_value, expected_value, msg=f'{value} not found in {resp_value}'
                                                          f'{f" for {msg}" if msg is not None else ""}')
        elif len(args) > 0 and MatchParam.IGNORE not in args:
            raise ValueError(f'MatchParam {args} not supported')

    def assert_success_response(self, resp_body: dict, msg=None):
        """
        Check a success response
        :param resp_body:   response body
        :param msg:         assert error message
        """
        self.assert_body_entry(resp_body, "success", MatchParam.TRUE, msg=msg)

    def assert_error_response(self, resp_body: dict, status_code: Union[int, range], message: str, *args, msg=None):
        """
        Check an error response
        :param resp_body:   response body
        :param status_code: expected status code or range within it should be
        :param message:     expected message
        :param msg:         assert error message
        :param args:        list of MatchParam
        """
        self.assert_body_entry(resp_body, "success", MatchParam.FALSE, msg=msg)

        param = (MatchParam.TO_INT, MatchParam.IN) if isinstance(status_code, range) else (MatchParam.EQUAL, )
        self.assert_body_entry(resp_body, "error", *param, value=status_code, msg=msg)

        self.assert_body_entry(resp_body, "message", *args, value=message, msg=msg)

    def assert_success_paginated_response(self, resp_body: dict, page: int, per_page: int, total: int,
                                          aliases: dict = None):
        """
        Check a paginated success response
        :param resp_body:    actual response
        :param page:        page requested
        :param per_page:    items per page requested
        :param total:       total num of items
        :param aliases:     dict of aliases for standard body fields
        """
        self.assert_success_response(resp_body)

        data_key = key_or_alias("data", aliases)
        total_key = key_or_alias("total", aliases)

        for key in [data_key, "page", "per_page", "num_pages", total_key, "offset", "limit"]:
            self.assertTrue(key in resp_body.keys(), f'"{key}" not in response')

        self.assertEqual(page, resp_body["page"], f'Incorrect page, expected {page}')

        expected_per_page = per_page if per_page <= self.max_items_per_page else self.max_items_per_page
        self.assertEqual(expected_per_page, resp_body["per_page"], f'Incorrect per page, expected {expected_per_page}')

        expected_num_pages = int(total / expected_per_page)
        if expected_num_pages * expected_per_page < total:
            expected_num_pages = expected_num_pages + 1
        self.assertEqual(expected_num_pages, resp_body["num_pages"], f'Incorrect num of pages, expected '
                                                                     f'{expected_num_pages}')

        self.assertEqual(total, resp_body[total_key], f'Incorrect total, expected {total}')

        expected_offset = expected_per_page * (page - 1)
        self.assertEqual(expected_offset, resp_body["offset"], f'Incorrect offset, expected {expected_offset}')

        expected_limit = expected_per_page * page
        if expected_limit > total:
            expected_limit = total
        self.assertEqual(expected_limit, resp_body["limit"], f'Incorrect limit, expected {expected_limit}')

    def assert_data_page(self, resp: Response, page: int, per_page: int, accum_total: int,
                         all_expected: list[EqualDataMixin], aliases: dict = None, **kwargs):
        """
        Verify a page of data
        :param resp:        response
        :param page:        page to request
        :param per_page:    per page to request
        :param accum_total: accumulated total
        :param all_expected: all expected results
        :param aliases:     dict of aliases for standard body fields
        :param kwargs:      additional fields to verify
        @:return tuple of next page and new accumulated total
        """
        self.assert_ok(resp.status_code)

        resp_body = json.loads(resp.data)
        # verify pagination info
        self.assert_success_paginated_response(resp_body, page, per_page, len(all_expected), aliases=aliases)

        # verify data
        data_key = key_or_alias("data", aliases)
        self.assertTrue(data_key in resp_body.keys(), f'key {data_key} not in response')

        self.assert_data_array(all_expected, resp_body[data_key], offset=resp_body["offset"], limit=resp_body["limit"])

        # verify any additional
        for key, val in kwargs.items():
            key = key_or_alias(key, aliases)
            self.assertTrue(key in resp_body.keys(), f'key {key} not in response')
            self.assertEqual(val, resp_body[key], f'value for {key} not correct')

        return page + 1, accum_total + len(resp_body[data_key])
