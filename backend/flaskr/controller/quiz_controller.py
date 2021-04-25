from http import HTTPStatus

from flask import request
from flask_restful import abort
from sqlalchemy import and_, not_

from ..model import Question, M_ID, M_PASSWORD
from ..service import (QueryParam, get_random_questions, update_user_by_id
                       )
from ..util import (get_request_arg, success_result, PREVIOUS_QUESTIONS, QUIZ_CATEGORY, REQ_ARG_NUM, USER_ID,
                    NUM_CORRECT, NUM_QUESTIONS
                    )


def next_question():
    """
    Get next quiz question.
    :return: question

    Request body:
    previous_questions: list of id's of previous questions
    quiz_category:      category id for quiz
    """
    data = request.get_json()
    num = get_request_arg(REQ_ARG_NUM, 1)
    previous_questions = data[PREVIOUS_QUESTIONS] if PREVIOUS_QUESTIONS in data else []
    quiz_category = data[QUIZ_CATEGORY] if QUIZ_CATEGORY in data else None

    multi_sel = (num > 1)

    # generate criteria list
    criteria = [not_(Question.id.in_(previous_questions))]
    if quiz_category is not None and int(quiz_category[M_ID]) > 0:
        criteria.append(Question.category == quiz_category[M_ID])

    selection = get_random_questions(
        criteria=and_(*criteria) if len(criteria) > 1 else criteria[0],
        pick=num, param=QueryParam.GET_ALL if multi_sel else QueryParam.GET_FIRST
    )

    if selection is not None:
        if multi_sel:
            result = {'questions': [q.format() for q in selection]}
        else:
            result = {'question': selection[0].format()}
    else:
        result = dict()

    return success_result(**result)


def save_result():
    """
    Save a quiz result.
    :return: user's updated info

    Request body:
    user_id:        id of user
    num_correct:    number of questions answered correctly
    num_questions:  number of questions answered
    """
    data = request.get_json()
    user_id = data[USER_ID] if USER_ID in data.keys() else None
    num_correct = data[NUM_CORRECT] if NUM_CORRECT in data.keys() else None
    num_questions = data[NUM_QUESTIONS] if NUM_QUESTIONS in data.keys() else None

    if user_id is None or num_correct is None or num_questions is None:
        abort(HTTPStatus.BAD_REQUEST.value, detailed_message="Invalid request")

    user = update_user_by_id(user_id, {
        NUM_CORRECT: num_correct,
        NUM_QUESTIONS: num_questions
    })
    result = {
        'user': {k: v for k, v in user.items() if k != M_PASSWORD}
    }
    return success_result(**result)
