import json
import random
import unittest

from backend.flaskr import QUIZZES_URL, QUIZ_RESULTS_URL, USER_ID, NUM_CORRECT, NUM_QUESTIONS
from backend.flaskr.model.models import QUESTION_FIELDS, User, M_USERNAME
from backend.flaskr.util import PREVIOUS_QUESTIONS, QUIZ_CATEGORY
from backend.test.base_test import TriviaTestCase
from backend.test.misc import make_url, Expect
from backend.test.test_data import *
from backend.test.test_users import UsersTestCase

ALL_CATEGORY_TYPE = 'All'


class QuizzesTestCase(TriviaTestCase):
    """This class represents the test case for trivia quizzes"""

    def setup_quiz_test(self, category_type: str = None):
        """
        Setup a quiz test
        :param category_type:    name of category to test or if None a random category is selected
        """
        if category_type is None:
            category = ALL_CATEGORY_DATA[random.randrange(0, len(ALL_CATEGORY_DATA))]
        elif category_type == ALL_CATEGORY_TYPE:
            category = CategoryData(0, category_type)
        else:
            category = category_by(category_type)
            self.assertGreater(len(category), 0)
            category = category[0]

        # get questions from db as not guaranteed to have pristine test data with just ALL_QUESTION_DATA
        query = Question.query
        if category.id > 0:
            query = query.filter(Question.category == category.id)

        questions = [QuestionData.from_model(question)
                     for question in query.order_by(Question.id).all()]
        expecting = set([question.id for question in questions])

        return category, questions, expecting

    def verify_question(self, expected_id: int, resp_ques: dict, count: int, received: set):
        expected_question_lst = questions_by(question_id=expected_id)
        if len(expected_question_lst) == 1:
            # it's one of the ALL_QUESTION_DATA questions
            expected_question = expected_question_lst[0]
            self.assertTrue(expected_question.equals(resp_ques))
        elif len(expected_question_lst) > 1:
            self.fail(f'Data error, too many expected questions')
        else:
            # another question, so just verify has a response
            for key in QUESTION_FIELDS:
                self.assertTrue(key in resp_ques)

        received.add(expected_id)
        return count + 1

    def test_all_category_questions(self):
        """
        Test all questions in a category, one at a time
        """
        category, questions, expecting = self.setup_quiz_test()
        received = set()
        count = 0

        while count < len(questions):
            with self.client as client:
                resp = client.post(
                    QUIZZES_URL, json={
                        PREVIOUS_QUESTIONS: list(received),
                        QUIZ_CATEGORY: category.to_dict()
                    })
                self.assert_ok(resp.status_code)

                resp_body = json.loads(resp.data)
                self.assert_success_response(resp_body)

                self.assertTrue('question' in resp_body.keys())
                recv_ques = resp_body['question']
                expected_id = resp_body['question'][M_ID]
                count = self.verify_question(expected_id, recv_ques, count, received)

        self.assertEqual(expecting, received)

    def test_all_category_questions_by_twos(self):
        """
        Test all questions in a category, two at a time
        """
        category, questions, expecting = self.setup_quiz_test()
        received = set()
        count = 0

        while count < len(questions):
            with self.client as client:
                resp = client.post(
                    make_url(QUIZZES_URL, num=2), json={
                        PREVIOUS_QUESTIONS: list(received),
                        QUIZ_CATEGORY: category.to_dict()
                    })
                self.assert_ok(resp.status_code)

                resp_body = json.loads(resp.data)
                self.assert_success_response(resp_body)

                self.assertTrue('questions' in resp_body.keys())
                for recv_ques in resp_body['questions']:
                    expected_id = recv_ques[M_ID]
                    count = self.verify_question(expected_id, recv_ques, count, received)

        self.assertEqual(expecting, received)

    def test_all_no_category_questions(self):
        """
        Test all questions, one at a time
        """
        category, questions, expecting = self.setup_quiz_test(ALL_CATEGORY_TYPE)
        received = set()
        count = 0

        while count < len(questions):
            with self.client as client:
                resp = client.post(
                    QUIZZES_URL, json={
                        PREVIOUS_QUESTIONS: list(received),
                        QUIZ_CATEGORY: category.to_dict()
                    })
                self.assert_ok(resp.status_code)

                resp_body = json.loads(resp.data)
                self.assert_success_response(resp_body)

                self.assertTrue('question' in resp_body.keys())
                recv_ques = resp_body['question']
                expected_id = resp_body['question'][M_ID]
                count = self.verify_question(expected_id, recv_ques, count, received)

        self.assertEqual(expecting, received)

    def test_save_quiz_result(self):
        """
        Test saving a quiz result
        """
        username = UsersTestCase.timestamped_username('quiz_user')
        UsersTestCase.register_user(self, username, 'secret')

        # get user from db
        user = User.query.filter(User.username == username).first()
        self.assertIsNotNone(user)

        user_id = user.id
        start_num_correct = user.num_correct
        start_num_questions = user.num_questions
        new_num_correct = start_num_correct + 4
        new_num_questions = start_num_questions + 5

        with self.client as client:
            resp = client.post(
                QUIZ_RESULTS_URL, json={
                    USER_ID: user_id,
                    NUM_CORRECT: new_num_correct - start_num_correct,
                    NUM_QUESTIONS: new_num_questions - start_num_questions
                })

            UsersTestCase.assert_user(self, resp,
                                      user_id=user_id, username=username,
                                      num_questions=new_num_questions, num_correct=new_num_correct,
                                      expect=Expect.SUCCESS)

    def test_save_invalid_quiz_result(self):
        """
        Test saving a quiz result
        """
        username = UsersTestCase.timestamped_username('invalid_quiz_user')
        UsersTestCase.register_user(self, username, 'secret')

        # get user from db
        user = User.query.filter(User.username == username).first()
        self.assertIsNotNone(user)

        user_id = user.id

        with self.client as client:

            for updates in [
                # invalid user id
                {USER_ID: 1000, NUM_CORRECT: 4, NUM_QUESTIONS: 5},
            ]:
                resp = client.post(
                    QUIZ_RESULTS_URL, json=updates)
                self.assert_not_found(resp.status_code)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
