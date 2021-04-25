"""
Test data as loaded by backend/setup/trivia.psql
"""
from backend.flaskr import Question
from backend.flaskr.model import M_QUESTION, M_ANSWER, M_CATEGORY, M_DIFFICULTY, M_ID
from backend.flaskr.model.models import M_MATCH


class EqualDataMixin:
    """
    Mixin class to add dict entries equality test
    """
    def equals(self, other: dict, ignore: list = None):
        """
        Equality test
        :param other:   data to compare with
        :param ignore:  list of attributes to ignore
        :return:
        """
        if ignore is None:
            ignore = []
        equal = isinstance(other, dict)
        if equal:
            for k, v in vars(self).items():
                if k not in ignore:
                    equal = (other[k] == v)
                    if not equal:
                        break
        return equal

    def to_dict(self):
        return {
            k: v for k, v in vars(self).items()
        }


class CategoryData(EqualDataMixin):
    """
    Data class representing a category
    :param category_id:     primary id of category
    :param category_type:   category type
    """

    def __init__(self, category_id: int, category_type: str):
        self.id = category_id
        self.type = category_type

    def map_kv(self):
        return str(self.id), self.type

    def __repr__(self):
        return f"<CategoryData(id={self.id}, type={self.type})>"


# all the categories configured by backend/setup/trivia.psql
ALL_CATEGORY_DATA = [
    CategoryData(1, 'Science'),
    CategoryData(2, 'Art'),
    CategoryData(3, 'Geography'),
    CategoryData(4, 'History'),
    CategoryData(5, 'Entertainment'),
    CategoryData(6, 'Sports'),
]
ALL_CATEGORY_DATA.sort(key=lambda c: c.id)
ALL_CATEGORY_MAP = {k: v for k, v in [c.map_kv() for c in ALL_CATEGORY_DATA]}


def category_by(type_text: str = None):
    """
    Get filtered categories
    :param type_text:   category type
    :return:
    """
    def match_type_text(c):
        return type_text.lower() in c.type.lower()

    if type_text is not None:
        func = match_type_text
    else:
        func = None
    return list(filter(func, ALL_CATEGORY_DATA)) if func is not None else []


class QuestionData(EqualDataMixin):
    """
    Data class representing a question
    :param question_id:     primary id of category
    :param question:        question
    :param answer:          answer
    :param match:           space-separated list of words to match from answer to be considered correct
    :param category:        id of category
    :param difficulty:      difficulty
    """

    def __init__(self, question_id: int, question: str, answer: str, match: str, difficulty: int, category: int):
        self.id = question_id
        self.question = question
        self.answer = answer
        self.match = match
        self.difficulty = difficulty
        self.category = category

    def map_kv(self):
        return str(self.id), {
            M_QUESTION: self.question,
            M_ANSWER: self.answer,
            M_MATCH: self.match,
            M_CATEGORY: self.category,
            M_DIFFICULTY: self.difficulty
        }

    @staticmethod
    def from_model(question: Question):
        return QuestionData(question_id=question.id, question=question.question, answer=question.answer,
                            match=question.match, difficulty=question.difficulty, category=question.category)

    @staticmethod
    def from_dict(question: dict):
        return QuestionData(question_id=question[M_ID], question=question[M_QUESTION], answer=question[M_ANSWER],
                            match=question.question[M_MATCH], difficulty=question[M_DIFFICULTY],
                            category=question[M_CATEGORY])

    def __repr__(self):
        return f"<QuestionData(id={self.id}, question={self.question}, answer={self.answer}, match={self.match}, " \
               f"difficulty={self.difficulty}, category={self.category})>"


# all the categories configured by backend/setup/trivia.psql
ALL_QUESTION_DATA = [
    #            question_id, question, answer, match, difficulty, category
    QuestionData(5, "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?", "Maya Angelou",
                 "maya angelou", 2, 4),
    QuestionData(9, "What boxer's original name is Cassius Clay?", "Muhammad Ali", "muhammad ali", 1, 4),
    QuestionData(2, "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?", "Apollo 13",
                 "apollo 13", 4, 5),
    QuestionData(4, "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
                 "Tom Cruise", "tom cruise", 4, 5),
    QuestionData(6,
                 "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed "
                 "appendages?",
                 "Edward Scissorhands", "edward scissorhands", 3, 5),
    QuestionData(10, "Which is the only team to play in every soccer World Cup tournament?", "Brazil", "brazil", 3, 6),
    QuestionData(11, "Which country won the first ever soccer World Cup in 1930?", "Uruguay", "uruguay", 4, 6),
    QuestionData(12, "Who invented Peanut Butter?", "George Washington Carver", "george washington carver", 2, 4),
    QuestionData(13, "What is the largest lake in Africa?", "Lake Victoria", "lake victoria", 2, 3),
    QuestionData(14, "In which royal palace would you find the Hall of Mirrors?", "The Palace of Versailles",
                 "palace versailles", 3, 3),
    QuestionData(15, "The Taj Mahal is located in which Indian city?", "Agra", "agra", 2, 3),
    QuestionData(16, "Which Dutch graphic artist–initials M C was a creator of optical illusions?", "Escher",
                 "escher", 1, 2),
    QuestionData(17, "La Giaconda is better known as what?", "Mona Lisa", "mona lisa", 3, 2),
    QuestionData(18, "How many paintings did Van Gogh sell in his lifetime?", "One", "one", 4, 2),
    QuestionData(19,
                 "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action "
                 "painting?",
                 "Jackson Pollock", "jackson pollock", 2, 2),
    QuestionData(20, "What is the heaviest organ in the human body?", "The Liver", "liver", 4, 1),
    QuestionData(21, "Who discovered penicillin?", "Alexander Fleming", "alexander fleming", 3, 1),
    QuestionData(22, "Hematology is a branch of medicine involving the study of what?", "Blood", "blood", 4, 1),
    QuestionData(23, "Which dung beetle was worshipped by the ancient Egyptians?", "Scarab", "scarab", 4, 4),
]
ALL_QUESTION_DATA.sort(key=lambda q: q.id)
ALL_QUESTION_MAP_DATA = [q.map_kv() for q in ALL_QUESTION_DATA]


def questions_by(category: int = None, difficulty: int = None, question_text: str = None, question_id: int = None):
    """
    Get filtered questions
    :param category:        category id to match
    :param difficulty:      difficulty to match
    :param question_text:   partial question text
    :param question_id:     id of question
    :return:
    """
    def match_category(q):
        return q.category == category

    def match_difficulty(q):
        return q.difficulty == difficulty

    def match_question_text(q):
        return question_text.lower() in q.question.lower()

    def match_question_id(q):
        return q.id == question_id

    if category is not None:
        func = match_category
    elif difficulty is not None:
        func = match_difficulty
    elif question_text is not None:
        func = match_question_text
    elif question_id is not None:
        func = match_question_id
    else:
        func = None
    return list(filter(func, ALL_QUESTION_DATA)) if func is not None else []
