import json
import random
import unittest
from http import HTTPStatus

from backend.flaskr import (CATEGORIES_URL, CATEGORY_BY_ID_URL, QUESTIONS_BY_CATEGORY_ID_URL, CATEGORY_RESPONSE_ALIASES,
                            QUESTION_RESPONSE_ALIASES, key_or_alias, Category
                            )
from backend.test.base_test import TriviaTestCase
from backend.test.misc import make_url, MatchParam
from test_data import *


class CategoriesTestCase(TriviaTestCase):
    """This class represents the test case for trivia categories"""

    def assert_categories_page(self, page: int, per_page: int, accum_total: int):
        """
        Request and verify a page of categories
        :param page:        page to request
        :param per_page:    per page to request
        :param accum_total: accumulated total
        @:return tuple of next page and new accumulated total
        """
        with self.client as client:
            resp = client.get(
                make_url(CATEGORIES_URL, page=page, per_page=per_page))

            page, accum_total = self.assert_data_page(resp, page, per_page, accum_total, ALL_CATEGORY_DATA,
                                                      aliases=CATEGORY_RESPONSE_ALIASES)

        return page, accum_total

    def test_all_categories(self):
        """
        Test all categories
        Note: In the event the total num exceed the max items per page, this will just check the 1st page
        """
        self.assert_categories_page(1, len(ALL_CATEGORY_DATA) + 1, 0)

    def test_all_categories_map(self):
        """
        Test all categories non paginated map
        """
        with self.client as client:
            resp = client.get(
                make_url(CATEGORIES_URL, pagination='n', type='map'))

            self.assert_ok(resp.status_code)

            resp_body = json.loads(resp.data)

            data_key = key_or_alias("data", CATEGORY_RESPONSE_ALIASES)

            resp_body = resp_body[data_key]
            self.assertTrue(isinstance(resp_body, dict))

            for key in ALL_CATEGORY_MAP.keys():
                self.assertTrue(key in resp_body.keys(), f'key {key} not in response')
                self.assertEqual(ALL_CATEGORY_MAP[key], resp_body[key], f'value for {key} not correct')

    def test_all_categories_pagination(self):
        """ Test all categories pagination """
        page = 1
        per_page = int(len(ALL_CATEGORY_DATA) / 2) + 1
        if per_page > self.max_items_per_page:
            per_page = self.max_items_per_page
        total = 0

        while total < len(ALL_CATEGORY_DATA):
            page, total = self.assert_categories_page(page, per_page, total)

        self.assertEqual(len(ALL_CATEGORY_DATA), total, f'actual total != expected total')

    def test_invalid_category_page(self):
        """ Test an invalid categories page """
        with self.client as client:
            resp = client.get(
                make_url(CATEGORIES_URL, page=1000))
            self.assert_bad_request(resp.status_code)

            data = json.loads(resp.data)
            self.assert_error_response(data, HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.phrase,
                                       MatchParam.CASE_INSENSITIVE, MatchParam.IN)

    def test_category_by_id(self):
        """ Test getting category by id """
        expected = ALL_CATEGORY_DATA[random.randrange(0, len(ALL_CATEGORY_DATA))]
        with self.client as client:
            resp = client.get(
                make_url(CATEGORY_BY_ID_URL, category_id=expected.id))
            self.assert_ok(resp.status_code)

            resp_body = json.loads(resp.data)
            self.assert_success_response(resp_body)

            self.assert_equal_data(expected, resp_body["category"])

    def test_category_by_id_not_found(self):
        """ Test an invalid category by id """
        with self.client as client:
            resp = client.get(
                make_url(CATEGORY_BY_ID_URL, category_id=1000))
            self.assert_not_found(resp.status_code)

            resp = json.loads(resp.data)
            self.assert_error_response(resp, HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase,
                                       MatchParam.CASE_INSENSITIVE, MatchParam.IN)

    def test_questions_by_category_id(self):
        """ Test getting questions by category id """
        category = ALL_CATEGORY_DATA[random.randrange(0, len(ALL_CATEGORY_DATA))]
        # get questions from db as not guaranteed to have pristine test data with just ALL_QUESTION_DATA
        questions = [QuestionData.from_model(question)
                     for question in Question.query.filter(Question.category == category.id).order_by(Question.id).all()
                     ]
        if len(questions) == 0:
            self.fail(f'No questions found for category {category.id}')

        page = 1
        per_page = int(len(questions) / 2)
        if per_page > self.max_items_per_page:
            per_page = self.max_items_per_page
        total = 0

        while total < len(questions):
            with self.client as client:
                resp = client.get(
                    make_url(QUESTIONS_BY_CATEGORY_ID_URL, category_id=category.id, page=page, per_page=per_page))

                page, total = self.assert_data_page(resp, page, per_page, total, questions,
                                                    aliases=QUESTION_RESPONSE_ALIASES)

        self.assertEqual(len(questions), total, f'actual total != expected total')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
