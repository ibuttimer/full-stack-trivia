import os
from . import FILE_CFG_AVAILABLE

#
# NOTE: Database configuration
#       Create a copy of /secrets-sample.py, update it with the database details, and save it as `secrets.py`.
#

SECRET_KEY = 'dev'
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database.
if FILE_CFG_AVAILABLE:
    from . import SERVER, PORT, USERNAME, PASSWORD
    DATABASE = 'trivia_test'
    db_info = f'{USERNAME}:{PASSWORD}@{SERVER}:{PORT}/{DATABASE}'
else:
    db_info = os.getenv('DATABASE_URI', '')

SQLALCHEMY_DATABASE_URI = f'postgresql://{db_info}'

SQLALCHEMY_TRACK_MODIFICATIONS = False  # disable FSADeprecationWarning

# General

# Max number of items per page.
MAX_ITEMS_PER_PAGE = 50
# Number of questions per page.
QUESTIONS_PER_PAGE = 10
# Number of categories per page.
CATEGORIES_PER_PAGE = 10

# Additional path to ntlk data; set to None to use just the nltk installation default locations.
NLTK_DATA_PATH = '../nltk_data'
