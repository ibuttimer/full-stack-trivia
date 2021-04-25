from http import HTTPStatus

from flask import Flask
from flask_cors import CORS

from backend.flaskr.model import setup_db, Question, Category
from backend.flaskr.controller import (all_categories, category_by_id, questions_by_category_id, all_questions,
                                       question_by_id, create_question, search_questions, next_question, save_result,
                                       login
                                       )
from backend.flaskr.util import *
from backend import config


def create_app(test_config=None):
    """
    Create the application
    :param test_config:
    :return:
    """
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config if test_config is None else test_config)
    set_config(app.config)
    setup_db(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # endpoint to handle GET requests for all available categories
    app.add_url_rule(CATEGORIES_URL, view_func=all_categories, methods=['GET'])
    # endpoint to GET category using a category ID
    app.add_url_rule(CATEGORY_BY_ID_URL, view_func=category_by_id, methods=['GET'])

    # GET endpoint to get questions based on category
    app.add_url_rule(QUESTIONS_BY_CATEGORY_ID_URL, view_func=questions_by_category_id, methods=['GET'])

    # endpoint to handle GET requests for questions
    app.add_url_rule(QUESTIONS_URL, view_func=all_questions, methods=['GET'])
    # endpoint to GET/DELETE question using a question ID
    app.add_url_rule(QUESTION_BY_ID_URL, view_func=question_by_id, methods=['GET', 'DELETE'])

    # an endpoint to POST a new question
    app.add_url_rule(QUESTIONS_URL, view_func=create_question, methods=['POST'])

    # POST endpoint to get questions based on a search term
    app.add_url_rule(QUESTION_SEARCH_URL, view_func=search_questions, methods=['POST'])

    # POST endpoint to get questions to play the quiz
    app.add_url_rule(QUIZZES_URL, view_func=next_question, methods=['POST'])
    # endpoint to SAVE quiz results
    app.add_url_rule(QUIZ_RESULTS_URL, view_func=save_result, methods=['POST'])

    # POST endpoint to login users
    app.add_url_rule(LOGIN_URL, view_func=login, methods=['POST'])

    # error handlers
    @app.errorhandler(HTTPStatus.BAD_REQUEST)
    def bad_request(error):
        return http_error_result(HTTPStatus.BAD_REQUEST, error)

    @app.errorhandler(HTTPStatus.UNAUTHORIZED)
    def not_implemented(error):
        return http_error_result(HTTPStatus.UNAUTHORIZED, error)

    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def not_found(error):
        return http_error_result(HTTPStatus.NOT_FOUND, error)

    @app.errorhandler(HTTPStatus.METHOD_NOT_ALLOWED)
    def method_not_allowed(error):
        return http_error_result(HTTPStatus.METHOD_NOT_ALLOWED, error)

    @app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
    def unprocessable_entity(error):
        return http_error_result(HTTPStatus.UNPROCESSABLE_ENTITY, error)

    @app.errorhandler(HTTPStatus.NOT_IMPLEMENTED)
    def not_implemented(error):
        return http_error_result(HTTPStatus.NOT_IMPLEMENTED, error)

    @app.errorhandler(HTTPStatus.SERVICE_UNAVAILABLE)
    def service_unavailable(error):
        return http_error_result(HTTPStatus.SERVICE_UNAVAILABLE, error)

    @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    def internal_server_error(error):
        return http_error_result(HTTPStatus.INTERNAL_SERVER_ERROR, error)

    return app


# Default port:
if __name__ == '__main__':
    create_app().run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    create_app().run(host='0.0.0.0', port=port)
"""
