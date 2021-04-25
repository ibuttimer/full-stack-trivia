import re
from typing import NewType, Union

from flask import Flask
from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import nltk
from nltk import word_tokenize

from backend.flaskr.util import MIN_DIFFICULTY, MAX_DIFFICULTY

db = SQLAlchemy()

QUESTIONS_TABLE = 'questions'
CATEGORIES_TABLE = 'categories'
USERS_TABLE = 'users'

# names of question model fields
M_ID = 'id'
M_QUESTION = 'question'
M_ANSWER = 'answer'
M_MATCH = 'match'
M_CATEGORY = 'category'
M_DIFFICULTY = 'difficulty'
# names of category model fields
M_TYPE = 'type'
# names of user model fields
M_USERNAME = 'username'
M_PASSWORD = 'password'
M_NUM_QUESTIONS = 'num_questions'
M_NUM_CORRECT = 'num_correct'

QUESTION_FIELDS = [M_ID, M_QUESTION, M_ANSWER, M_MATCH, M_CATEGORY, M_DIFFICULTY]
CATEGORY_FIELDS = [M_ID, M_TYPE]
USER_FIELDS = [M_ID, M_USERNAME, M_PASSWORD, M_NUM_QUESTIONS, M_NUM_CORRECT]

ANS_MATCH_SEPARATOR = '%%%'
__ANS_MATCH_SEP_REGEX__ = re.compile(rf'(.*){ANS_MATCH_SEPARATOR}(.*)')
__NON_WS_REGEX__ = re.compile(r'\S+')           # any character which is not a whitespace character
__NON_WORD_REGEX__ = re.compile(r'^\W+|\W+$')   # any leading/trailing character which is not a word character


def setup_db(app: Flask, config: dict = None):
    """
    Binds a flask application and a SQLAlchemy service
    :param app:     flask application
    :param config:
    """
    if config is not None:
        for entry in config.keys():
            app.config[entry] = config[entry]

    if 'SQLALCHEMY_DATABASE_URI' not in app.config.keys() and 'SQLALCHEMY_BINDS' not in app.config.keys():
        raise EnvironmentError('Database not configured')

    db.app = app
    db.init_app(app)

    # db.create_all()
    migrate = Migrate(app, db)

    # https://github.com/nltk/nltk/wiki/Frequently-Asked-Questions-(Stackoverflow-Edition)#how-to-config-nltk-data-directory-from-code
    if app.config["NLTK_DATA_PATH"] is not None:
        nltk.data.path.append(app.config["NLTK_DATA_PATH"])


def generate_match(answer_str: str) -> (str, str):
    """
    Generate a match list for an answer.
    (Based on https://github.com/nltk/nltk/wiki/Frequently-Asked-Questions-(Stackoverflow-Edition)#how-to-remove-stopwords-with-nltk)
    :param answer_str: answer to generate match list for
    """
    regex_match = __ANS_MATCH_SEP_REGEX__.match(answer_str)
    if regex_match:
        # use specified answer & match
        answer = regex_match.group(1)
        match = regex_match.group(2)
    else:
        # generate match
        stopwords = nltk.corpus.stopwords.words('english')

        stripped = __NON_WS_REGEX__.sub(
            lambda m: __NON_WORD_REGEX__.sub('', m.group()), answer_str)    # just words, no punctuation
        tokenized_answer = word_tokenize(stripped.lower())
        tokenized_no_stop = [token for token in tokenized_answer if token not in stopwords]

        answer = answer_str
        match = " ".join(tokenized_no_stop)

    return answer, match


class Question(db.Model):
    """
    Question model
    :param question:    question text
    :param answer:      answer text
    :param match:       space-separated list of words to match from answer to be considered correct
    :param category:    question category
    :param difficulty:  question difficulty
    """
    __tablename__ = QUESTIONS_TABLE

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False, unique=True)
    answer = Column(String, nullable=False)
    match = Column(String, nullable=False)
    category = Column(Integer, ForeignKey(f"{CATEGORIES_TABLE}.id"), nullable=False)
    category_info = db.relationship('Category')
    difficulty = Column(Integer, CheckConstraint(f'{M_DIFFICULTY}>={MIN_DIFFICULTY} AND {M_DIFFICULTY}<={MAX_DIFFICULTY}'))

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer, self.match = generate_match(answer)
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        Question.update()

    @staticmethod
    def update():
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        Question.update()

    def format(self):
        return {
            M_ID: self.id,
            M_QUESTION: self.question,
            M_ANSWER: self.answer,
            M_MATCH: self.match,
            M_CATEGORY: self.category,
            M_DIFFICULTY: self.difficulty
        }

    def map_kv(self):
        return str(self.id), {k: v for k, v in self.format() if k != M_ID}

    def __repr__(self):
        return f"<Question({M_ID}={self.id}, {M_QUESTION}={self.question}, {M_ANSWER}={self.answer}, " \
               f"{M_MATCH}={self.match}, {M_CATEGORY}={self.category}, {M_DIFFICULTY}={self.difficulty})>"


class Category(db.Model):
    """
    Category model
    :param category_type:   category type
    """
    __tablename__ = CATEGORIES_TABLE

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, unique=True)

    def __init__(self, category_type: str):
        self.type = category_type

    def format(self):
        return {
            M_ID: self.id,
            M_TYPE: self.type
        }

    def map_kv(self):
        return str(self.id), self.type

    def __repr__(self):
        return f"<Category({M_ID}={self.id}, {M_TYPE}={self.type})>"


class User(db.Model):
    """
    User model
    :param username:        username
    :param password:        password
    :param num_questions:   number of questions answered
    :param num_correct:     number of questions correctly answered
    """
    __tablename__ = USERS_TABLE

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    num_questions = Column(Integer, default=0)
    num_correct = Column(Integer, default=0)

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.num_questions = 0
        self.num_correct = 0

    def format(self):
        return {
            M_ID: self.id,
            M_USERNAME: self.username,
            M_PASSWORD: self.password,
            M_NUM_QUESTIONS: self.num_questions,
            M_NUM_CORRECT: self.num_correct
        }

    def map_kv(self):
        return str(self.id), {k: v for k, v in self.format() if k != M_ID}

    def __repr__(self):
        return f"<User({M_ID}={self.id}, {M_USERNAME}={self.username}, {M_PASSWORD}={self.password}, " \
               f"{M_NUM_QUESTIONS}={self.num_questions}, {M_NUM_CORRECT}={self.num_correct})>"


AnyModel = NewType('AnyModel', Union[Question, Category, User])
