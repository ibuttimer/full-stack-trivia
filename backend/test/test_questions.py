import json
import random
import unittest
from http import HTTPStatus

from sqlalchemy import and_

from backend.flaskr import (QUESTIONS_URL, QUESTION_BY_ID_URL, QUESTION_RESPONSE_ALIASES, QUESTION_SEARCH_URL,
                            QUESTION_SEARCH_TERM, MIN_DIFFICULTY, MAX_DIFFICULTY, key_or_alias
                            )
from backend.flaskr.model.models import ANS_MATCH_SEPARATOR
from backend.test.base_test import TriviaTestCase
from backend.test.misc import Expect
from backend.test.misc import make_url, MatchParam
from backend.test.test_data import *


class QuestionsTestCase(TriviaTestCase):
    """This class represents the test case for trivia questions"""

    def assert_questions_page(self, page: int, per_page: int, accum_total: int, all_expected: list[EqualDataMixin]):
        """
        Request and verify a page of questions
        :param page:        page to request
        :param per_page:    per page to request
        :param accum_total: accumulated total
        :param all_expected: all expected results
        @:return tuple of next page and new accumulated total
        """
        with self.client as client:
            resp = client.get(
                make_url(QUESTIONS_URL, page=page, per_page=per_page))
            self.assert_ok(resp.status_code)

            page, accum_total = self.assert_data_page(resp, page, per_page, accum_total, all_expected,
                                                      aliases=QUESTION_RESPONSE_ALIASES,
                                                      # additional elements
                                                      categories=ALL_CATEGORY_MAP)

        return page, accum_total

    def test_all_questions(self):
        """
        Test all questions
        Note: In the event the total num exceed the max items per page, this will just check the 1st page
        """
        # get questions from db as not guaranteed to have pristine test data with just ALL_QUESTION_DATA
        questions = [QuestionData.from_model(question) for question in Question.query.order_by(Question.id).all()]
        self.assert_questions_page(1, len(questions) + 1, 0, questions)

    def test_all_questions_pagination(self):
        """ Test all questions pagination """
        # get questions from db as not guaranteed to have pristine test data with just ALL_QUESTION_DATA
        questions = [QuestionData.from_model(question) for question in Question.query.order_by(Question.id).all()]

        page = 1
        per_page = int(len(questions) / 2) + 1
        if per_page > self.max_items_per_page:
            per_page = self.max_items_per_page
        total = 0

        while total < len(questions):
            page, total = self.assert_questions_page(page, per_page, total, questions)

        self.assertEqual(len(questions), total, f'actual total != expected total')

    def test_invalid_question_page(self):
        """ Test an invalid questions page """
        with self.client as client:
            resp = client.get(
                make_url(QUESTIONS_URL, page=1000))
            self.assert_bad_request(resp.status_code)

            data = json.loads(resp.data)
            self.assert_error_response(data, HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.phrase,
                                       MatchParam.CASE_INSENSITIVE, MatchParam.IN)

    def verify_question_by_id(self, expected: QuestionData, ignore: list = None):
        """
        Test getting question by id
        :param expected:    expected value
        :param ignore:      list of attributes to ignore
        """
        with self.client as client:
            resp = client.get(
                make_url(QUESTION_BY_ID_URL, question_id=expected.id))
            self.assert_ok(resp.status_code)

            resp_body = json.loads(resp.data)
            self.assert_success_response(resp_body)

            self.assert_equal_data(expected, resp_body["question"], ignore=ignore)

    def test_question_by_id(self):
        """ Test getting question by id """
        expected = ALL_QUESTION_DATA[random.randrange(0, len(ALL_QUESTION_DATA))]
        self.verify_question_by_id(expected)

    def test_question_by_id_not_found(self):
        """ Test an invalid question by id """
        with self.client as client:
            resp = client.get(
                make_url(QUESTION_BY_ID_URL, question_id=1000))
            self.assert_not_found(resp.status_code)

            resp_body = json.loads(resp.data)
            self.assert_error_response(resp_body, HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase,
                                       MatchParam.CASE_INSENSITIVE, MatchParam.IN)

    def test_questions_search(self):
        """ Test questions search """
        for search_term in ['title', 'Who']:
            questions = questions_by(question_text=search_term)
            if len(questions) == 0:
                self.fail(f'No questions found for search term {search_term}')

            page = 1
            per_page = int(len(questions) / 2) + 1
            if per_page > self.max_items_per_page:
                per_page = self.max_items_per_page
            total = 0

            while total < len(questions):
                with self.client as client:
                    resp = client.post(
                        make_url(QUESTION_SEARCH_URL, page=page, per_page=per_page),
                        json={QUESTION_SEARCH_TERM: search_term}
                    )

                    page, total = self.assert_data_page(resp, page, per_page, total, questions,
                                                        aliases=QUESTION_RESPONSE_ALIASES)

            self.assertEqual(len(questions), total, f'actual total != expected total')

    def _create_question(self, expect: Expect, question: str = None, answer: str = None,
                         difficulty: int = None, category: int = None, tag: str = None):
        """
        Create a question
        :param expect:      Expected result; one of Expect.SUCCESS or Expect.FAILURE
        :param question:    question text
        :param answer:      answer text
        :param difficulty:  difficulty
        :param category:    category id
        """
        # Note 'match' is not an argument as it is automatically created
        new_question = {
            k: v for k, v in {
                M_QUESTION: question, M_ANSWER: answer, M_DIFFICULTY: difficulty, M_CATEGORY: category
            }.items()
            if v is not None
        }
        msg = f'question {new_question} {tag if tag is not None else ""}'
        with self.client as client:
            resp = client.post(QUESTIONS_URL, json=new_question)

            resp_body = json.loads(resp.data)
            if expect == Expect.SUCCESS:
                self.assert_created(resp.status_code, msg=msg)
                self.assert_success_response(resp_body, msg=msg)
                self.assert_body_entry(resp_body, "created", MatchParam.EQUAL, value=1, msg=msg)
            else:
                self.assert_error_response(resp_body, range(400, 500), '', MatchParam.IGNORE, msg=msg)

    def test_create_question(self):
        """ Test create question """
        science = category_by('Science')[0].id
        self._create_question(Expect.SUCCESS, question="1+1", answer="2 in most people's world",
                              difficulty=MIN_DIFFICULTY, category=science)

    def test_create_invalid_question(self):
        """ Test create invalid question """
        # test invalid category
        min_category = ALL_CATEGORY_DATA[0].id
        max_category = ALL_CATEGORY_DATA[0].id
        for index in range(1, len(ALL_CATEGORY_DATA)):
            value = ALL_CATEGORY_DATA[index].id
            if value < min_category:
                min_category = value
            if value > min_category:
                max_category = value

        science = category_by('Science')[0].id

        index = 0
        for question, answer, difficulty, category in [
            # test invalid category
            ("1+1", "2", MIN_DIFFICULTY, min_category - 1),
            ("1+1", "2", MIN_DIFFICULTY, max_category + 1),
            ("1+1", "2", MIN_DIFFICULTY, "Science"),
            # test invalid difficulty
            ("1+1", "2", MIN_DIFFICULTY - 1, min_category),
            ("1+1", "2", MAX_DIFFICULTY + 1, max_category),
            ("1+1", "2", "Easy", max_category),
            # test invalid question
            ("", "2", MIN_DIFFICULTY, science),
            (" ", "2", MIN_DIFFICULTY, science),
            (None, "2", MIN_DIFFICULTY, science),
            # test invalid answer
            ("1+1", "", MIN_DIFFICULTY, science),
            ("1+1", " ", MIN_DIFFICULTY, science),
            ("1+1", None, MIN_DIFFICULTY, science),
        ]:
            self._create_question(Expect.FAILURE,
                                  question=question, answer=answer, difficulty=difficulty, category=category,
                                  tag=f'index {index}')
            index = index + 1

    def test_create_question_with_specified_match(self):
        """ Test create question with the match term specified """
        science = category_by('Science')[0].id
        question = "The Fahrenheit and Celsius scales intersect at what temperature?"
        answer = "-40"  # the '-' would normally be stripped from the '-40' in the match
        self._create_question(Expect.SUCCESS,
                              question=question,
                              answer=f"{answer}{ANS_MATCH_SEPARATOR}{answer}",
                              difficulty=MIN_DIFFICULTY, category=science)

        # get question from db
        db_question = Question.query \
            .filter(and_(
                Question.question == question,
                Question.difficulty == MIN_DIFFICULTY,
                Question.category == science
            )).first()
        self.assertIsNotNone(question)

        expected = QuestionData(question_id=db_question.id, question=question, answer=answer, match=answer,
                                difficulty=MIN_DIFFICULTY, category=science)
        self.verify_question_by_id(expected)

    def test_delete_question(self):
        """ Test delete question """
        science = category_by('Science')[0].id
        question = "1+1+1"
        answer = "3"
        self._create_question(Expect.SUCCESS, question=question, answer=answer, difficulty=MIN_DIFFICULTY,
                              category=science)

        with self.client as client:
            # retrieve question just created
            resp = client.post(
                QUESTION_SEARCH_URL, json={QUESTION_SEARCH_TERM: "1+1+1"}
            )
            self.assert_ok(resp.status_code)

            resp_body = json.loads(resp.data)

            # verify data
            data_key = key_or_alias("data", QUESTION_RESPONSE_ALIASES)
            self.assertTrue(data_key in resp_body.keys(), f'key {data_key} not in response')
            self.assertTrue(len(resp_body[data_key]) > 0, f'no results in response')

            to_delete = resp_body[data_key][0]
            self.assertEqual(question, to_delete[M_QUESTION])
            self.assertEqual(answer, to_delete[M_ANSWER])
            self.assertEqual(MIN_DIFFICULTY, to_delete[M_DIFFICULTY])
            self.assertEqual(science, to_delete[M_CATEGORY])

            resp = client.delete(
                make_url(QUESTION_BY_ID_URL, question_id=to_delete[M_ID]))
            self.assert_ok(resp.status_code)

            resp_body = json.loads(resp.data)
            self.assert_success_response(resp_body)
            self.assert_body_entry(resp_body, "deleted", MatchParam.EQUAL, value=1)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
