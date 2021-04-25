from datetime import datetime
import json
import unittest
from http import HTTPStatus

from backend.flaskr import LOGIN_URL
from backend.flaskr.model import M_USERNAME, M_PASSWORD, M_NUM_QUESTIONS, M_NUM_CORRECT, M_ID
from backend.test.base_test import TriviaTestCase
from backend.test.misc import MatchParam, Expect


class UsersTestCase(TriviaTestCase):
    """This class represents the test case for trivia users"""

    @staticmethod
    def login_user(testcase: TriviaTestCase, username: str, password: str,
                   expect: Expect = Expect.SUCCESS, error_code: int = HTTPStatus.OK):
        """
        Login user
        """
        with testcase.client as client:
            resp = client.post(
                LOGIN_URL, json={
                     M_USERNAME: username, M_PASSWORD: password
                }
            )
            resp_body = json.loads(resp.data)

            if expect == Expect.SUCCESS:
                testcase.assert_ok(resp.status_code)

                testcase.assertTrue('user' in resp_body.keys())
                user_info = resp_body['user']
                testcase.assertTrue(M_ID in user_info.keys())
                testcase.assert_body_entry(user_info, M_USERNAME, MatchParam.EQUAL, value=username)
                testcase.assert_body_entry(user_info, M_NUM_QUESTIONS, MatchParam.EQUAL, value=0)
                testcase.assert_body_entry(user_info, M_NUM_CORRECT, MatchParam.EQUAL, value=0)
            else:
                if error_code == HTTPStatus.UNAUTHORIZED:
                    testcase.assert_unauthorized_request(resp.status_code)
                else:
                    testcase.assert_bad_request(resp.status_code)

                testcase.assertTrue('detailed_message' in resp_body.keys())

    @staticmethod
    def register_user(testcase: TriviaTestCase, username: str, password: str,
                      expect: Expect = Expect.SUCCESS, error_code: int = HTTPStatus.OK):
        """
        Login user
        """
        with testcase.client as client:
            resp = client.post(
                LOGIN_URL, json={
                     M_USERNAME: username, M_PASSWORD: password
                }
            )
            resp_body = json.loads(resp.data)

            if expect == Expect.SUCCESS:
                testcase.assert_ok(resp.status_code)

                testcase.assertTrue('user' in resp_body.keys())
                user_info = resp_body['user']
                testcase.assertTrue(M_ID in user_info.keys())
                testcase.assert_body_entry(user_info, M_USERNAME, MatchParam.EQUAL, value=username)
                testcase.assert_body_entry(user_info, M_NUM_QUESTIONS, MatchParam.EQUAL, value=0)
                testcase.assert_body_entry(user_info, M_NUM_CORRECT, MatchParam.EQUAL, value=0)
            else:
                if error_code == HTTPStatus.UNAUTHORIZED:
                    testcase.assert_unauthorized_request(resp.status_code)
                else:
                    testcase.assert_bad_request(resp.status_code)

                testcase.assertTrue('detailed_message' in resp_body.keys())

    @staticmethod
    def timestamped_username(username: str) -> str:
        return f'{username}_{datetime.now().isoformat()}'

    def test_register_user(self):
        """
        Test user registration
        Note: slightly redundant as new users are currently automatically registered
        """
        UsersTestCase.register_user(self, UsersTestCase.timestamped_username('register_user'), 'secret')

    def test_register_invalid_user(self):
        """
        Test user registration
        Note: slightly redundant as new users are currently automatically registered
        """
        UsersTestCase.register_user(self, '', 'secret', expect=Expect.FAILURE, error_code=HTTPStatus.BAD_REQUEST)
        UsersTestCase.register_user(self, 'bad_user', '', expect=Expect.FAILURE, error_code=HTTPStatus.BAD_REQUEST)

    def test_login_user(self):
        """
        Test user login
        """
        UsersTestCase.login_user(self, UsersTestCase.timestamped_username('login_user'), 'secret')

    def test_login_user_bad_password(self):
        """
        Test bad password login
        """
        username = UsersTestCase.timestamped_username('bad_password_user')
        UsersTestCase.register_user(self, username, 'secret')
        UsersTestCase.login_user(self, username, 'guess', expect=Expect.FAILURE, error_code=HTTPStatus.UNAUTHORIZED)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
