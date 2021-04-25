# Routes related.
CATEGORY_ID = 'category_id'

CATEGORIES_URL = '/api/categories'
CATEGORY_BY_ID_URL = f'{CATEGORIES_URL}/<int:{CATEGORY_ID}>'
QUESTIONS_BY_CATEGORY_ID_URL = f'{CATEGORY_BY_ID_URL}/questions'

QUESTION_ID = 'question_id'

QUESTIONS_URL = '/api/questions'
QUESTION_BY_ID_URL = f'{QUESTIONS_URL}/<int:{QUESTION_ID}>'
QUESTION_SEARCH_URL = f'{QUESTIONS_URL}/search'

QUIZZES_URL = '/api/quizzes'
QUIZ_RESULTS_URL = F'{QUIZZES_URL}/results'

LOGIN_URL = '/api/login'

# Request related.
REQ_ARG_PAGE = 'page'  # Request page argument.
REQ_ARG_PER_PAGE = 'per_page'  # Request per page argument.
REQ_ARG_PAGINATION = 'pagination'  # Request pagination flag argument.
REQ_ARG_TYPE = 'type'  # Request response type argument.

ENTITY_TYPE = 'entity'  # Request response type entity; {id, ..}.
MAP_TYPE = 'map'  # Request response type map; id, xxx or id, {..} if more than one property other than id.

QUESTION_SEARCH_TERM = 'searchTerm'

PREVIOUS_QUESTIONS = 'previous_questions'
QUIZ_CATEGORY = 'quiz_category'

REQ_ARG_NUM = 'num'  # Request number argument.

USERNAME = 'username'
PASSWORD = 'password'

USER_ID = 'user_id'
NUM_CORRECT = 'num_correct'
NUM_QUESTIONS = 'num_questions'

# Response related.
# Aliases for standard response entries used in questions responses.
QUESTION_RESPONSE_ALIASES = {
    "data": "questions",
    "total": "total_questions"
}
# Aliases for standard response entries used in categories responses.
CATEGORY_RESPONSE_ALIASES = {
    "data": "categories"
}

# Model related.
MIN_DIFFICULTY = 1
MAX_DIFFICULTY = 5

