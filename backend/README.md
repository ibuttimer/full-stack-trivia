# Udacitrivia

Udacitrivia is a trivia quiz application, which allows users to undertake quizzes in general or specific categories. 
Results can be recorded to maintain an overall correct score for individual users. New questions may be
added to the database and, questions may be reviewed and deleted.

## Table of Contents
1. [Getting Started](#getting-started)
    1. [Pre-requisites and Local Development](#pre-requisites-and-local-development)
     1. [Guidelines](#guidelines)
     1. [Backend Project Structure](#backend-project-structure)
     1. [Technology Stack](#technology-stack)
   1. [Setup](#setup)
      1. [Virtual Environment](#virtual-environment)
      1. [Terminal](#terminal)
      1. [Install dependencies](#install-dependencies)
      1. [Database Setup](#database-setup)
         1. [Configuration](#configuration)
         1. [Migration](#migration)
         1. [Load Sample Data](#load-sample-data)
   1. [Run the application](#run-the-application)
   1. [Test](#test)
1. [API](#api)
    1. [Basic Formats](#basic-formats)
      1. [Success Response](#success-response)
      1. [Error Response](#error-response)
      1. [Paginated Request](#paginated-request)
      1. [Paginated Response](#paginated-response)
   1. [Login](#login)
      1. [User Entity](#user-entity)
   1. [Categories](#categories)
      1. [Category Entity](#category-entity)
      1. [Category Map](#category-map)
   1. [Category By Id](#category-by-id)
   1. [Questions By Category Id](#questions-by-category-id)
   1. [Questions](#questions)
      1. [Question Entity](#question-entity)
   1. [Question By Id](#question-by-id)
   1. [Create Question](#create-question)
   1. [Questions Search](#questions-search)
   1. [Quiz](#quiz)
   1. [Quiz Results](#quiz-results)

### Getting Started
#### Pre-requisites and Local Development
[Python3](https://wiki.python.org/moin/BeginnersGuide/Download), [nodejs](https://nodejs.org/en/download/), 
[pip](https://docs.python.org/3/installing/index.html) and [PostgresSQL](https://www.postgresql.org/) 
must be installed to work with this project.

#### Guidelines
All backend code follows [PEP8](https://www.python.org/dev/peps/pep-0008/) style guidelines.

#### Backend Project Structure
The backend application structure is as follows:
  ```shell
  ├── README.md
  ├── backend               - backend application
  │   ├── flaskr            - backend application code
  │   │   ├── controller    - controllers for processing API requests
  │   │   ├── model         - database ORM models
  │   │   ├── service       - service layer interfacing between controllers and database
  │   │   └── util          - miscellaneous application code
  │   ├── migrations        - database management
  │   ├── nltk_data         - NLTK data files, see XXXXX
  │   ├── setup             - setup related files
  │   ├── test              - unittest test scripts
  │   ├── config.py         - application configuration
  │   ├── requirements.txt  - The dependencies to be installed with "pip3 install -r requirements.txt"
  │   ├── secrets.py        - Database URLs, see [Database setup](#database-setup)
  │   └── test_config.py    - unittest application configuration
  └── frontend              - frontend application
      └── ...
  ```

#### Technology Stack
The backend consists of a Python application running a [Flask](https://flask.palletsprojects.com/) web server, and 
utilising [PostgresSQL](https://www.postgresql.org/) for data persistence.
[SQLAlchemy](https://www.sqlalchemy.org/), [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) and
[Flask-Migrate](https://flask-migrate.readthedocs.io/) are used for database management and operations, and 
[Flask-CORS](https://flask-cors.readthedocs.io/) is used to process cross origin requests.

#### Setup
##### Virtual Environment
It is recommended that a virtual environment be used for development purposes. 
Please see [Creating a virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) for details.

>**Note:** The following instructions are intended to be executed from a terminal window in the `backend` folder, 
> in which the [virtual environment is activated](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment)

##### Terminal
Run the following commands to configure a terminal:
```bash
For Linux and Mac:                            For Windows:
$ export FLASK_APP=flaskr                     > set FLASK_APP=flaskr
$ export FLASK_ENV=development                > set FLASK_ENV=development
```
See [Run The Application](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/#run-the-application) for other operating systems.

##### Install dependencies
Run the following command:
````shell
> pip3 install -r requirements.txt
````
Also see [Using requirements files](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#using-requirements-files).

##### Database Setup
###### Configuration
The database URI may be configured in two ways:
1. Create a copy of [secrets-sample.py](secrets-sample.py), update it with the database details, and save it as `secrets.py` 
in the project root folder.

   E.g.
     ```sh
     SERVER = 'localhost'
     PORT = '5432'
     DATABASE = 'trivia'
     USERNAME = 'username'
     PASSWORD = 'password'
     ```
1. Set the environment variable `DATABASE_URI` to `{username}:{password}@{server}:{port}/{database}`

   E.g.
   ```bash
   For Linux and Mac:                            
   $ export DATABASE_URI=dbowner:password@localhost:5432/trivia
   
   For Windows:
   > set DATABASE_URI=dbowner:password@localhost:5432/trivia
   ```

> **Note:** In the event both, options are available, the environment variable `DATABASE_URI` will be used.

###### Migration
Once a blank database, as specified in [Configuration](#configuration) is available, it may be prepared for the 
application by running the following command in a [Terminal](#terminal):

```bash
$ flask db upgrade 
```
This will configure the database to the state required by the application, using the script 
[3cbfb3ae2f14_.py](migrations/versions/3cbfb3ae2f14_.py).

###### Load Sample Data
The sample data may be loaded using the script [load_initial_data.py](setup/load_initial_data.py).
Run the following commands to set the `PYTHONPATH` environment variable, and run the script:
```bash
For Linux and Mac:                            For Windows:
$ cd /path/to/project/backend/setup           > cd \path\to\project\backend\setup
$ export PYTHONPATH=/path/to/project          > set PYTHONPATH=/path/to/project
$ python -m load_initial_data                 > python -m load_initial_data
```
> **Note:** On Windows, use the short names generated for folders with names which include spaces.
##### Run the application
Run the following commands:
```bash
$ flask run 
```
See [Run The Application](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/#run-the-application) for other operating systems.

##### Test
A number of unit tests are available in the [test](#test) folder.

* Create a database called `trivia_test` on the PostgresSQL server. 
  (To use an alternative name update the `DATABASE` value in [test_config.py](test_config.py))
* Initialise the database using [trivia.psql](setup/trivia.psql) from the [setup](setup) folder.
  > **Note:** Replace `dbowner` with the database owner's username.
* Run the following commands to set the `PYTHONPATH` environment variable, and run the script:
   ```bash
   For Linux and Mac:                            For Windows:
   $ cd /path/to/project/backend/test            > cd \path\to\project\backend\test
   $ export PYTHONPATH=/path/to/project          > set PYTHONPATH=/path/to/project
   $ python -m test_flaskr                       > python -m test_flaskr
   ```

### API
The application exposes the following API:

#### Basic Formats
In general, the following basic formats are followed:

##### Success Response
The standard success response has the following the format:

| Field            | Description |
|------------------|-------------|
| ``success``      | success flag, always *true* for an successful response |
| *payload*        | results, endpoint dependant and may be a list or json object |

##### Error Response
The standard error response has the following format:

| Field            | Description |
|------------------|-------------|
| ``success``          | success flag, always *false* for an error response |
| ``error``            | http status code |
| ``message``          | message corresponding to http status code |
| ``detailed_message`` | optional, detailed message |

For example, an invalid login would result in the following response:
```json
{
  "success": false,
  "error": 401,
  "message": "Unauthorized",
  "detailed_message": "Invalid username or password"
}
```

##### Paginated Request
Paginated requests may be made against various endpoints. The endpoints accept the following query parameters:

| Parameter        | Description |
|------------------|-------------|
| ``page``         | page of results, beginning at *1* |
| ``per_page``     | results per page, default *10* |

##### Paginated Response
Paginated responses may be returned by various endpoints. The basic response follows the format:

| Field            | Description |
|------------------|-------------|
| ``success``      | success flag, always *true* for an successful response |
| ``page``         | page of results, beginning at *1* |
| ``num_pages``    | total number page of results |
| ``per_page``     | results per page, default *10* |
| ``total``        | total number of results |
| ``offset``       | start offset of returned results (included) from beginning of result set |
| ``limit``        | end offset of returned results (excluded) from beginning of result set |
| *payload*        | response results, field name is endpoint dependant and may be a list or json object |

For example, a successful all categories request would result in the following response:
```json
{
  "success": true,
  "page": 1,
  "num_pages": 1,
  "per_page": 10,
  "total": 6,
  "offset": 0,
  "limit": 6,
  "categories": [ ... ]
}
```

#### Login
The application requires users to login. Users are auto-registered on initial login.  

|                   | Description |
|------------------:|-------------|
| **Endpoint**      | `/api/login` |
| **Method**        | POST |
| **Query**         | - |
| **Request Body**  | `username`: login username <br> `password`: user password |
| **Data type**     | json |
| **Content-Type**  | application/json |
| **Response**      | 200 - OK|
| **Response Body** | A [Success Response](#success-response) with the *payload* attribute named `user` |
| ```user```        | a [User Entity](#user-entity) |
| **Errors**        | 400 - BAD REQUEST <br> 401 - UNAUTHORIZED |

##### User Entity
A user entity contains the following attributes

`id`: id of user <br>`num_correct`: total number of correct answers <br>```num_questions```: total number of questions attempted <br>`username` : username


For example, a successful login would result in the following:

*Request*

POST `/api/login`
```json
{
  "username": "fred",
  "password": "isasecret"
}
```
*Response*
```json
{
  "success": true,
  "user": {
    "id": 1,
    "num_correct": 75,
    "num_questions": 208,
    "username": "fred"
  }
}
```

#### Categories
A listing of all categories. By default, this endpoint returns a [Paginated Response](#paginated-response).

|                   | Description |
|------------------:|-------------|
| **Endpoint**      | `/api/categories` |
| **Method**        | GET |
| **Query**         | A [Paginated Request](#paginated-request) with the additional parameters <br> `pagination`: pagination flag; *'y'* or *'n'*, default *'y'* <br>`type`: response type; *'entity'* or *'map'*, default *'entity'* |
| **Request Body**  | - |
| **Data type**     | - |
| **Content-Type**  | - |
| **Response**      | 200 - OK|
| **Response Body** | A [Paginated Response](#paginated-response) with the *payload* attribute named `categories`. |
| `categories`      | *entity* response : a list of [Category Entity](#category-entity) <br>or<br> *map* response : a [Category Map](#category-map) |
| **Errors**        | 400 - BAD REQUEST |

##### Category Entity
A category entity contains the following attributes

`id`: question id <br>`type`: category name

##### Category Map
A category map contains category id as the keys, and the corresponding category names as the values.

````json
{
  "1": "Science",
  "2": "Art" 
}
````

For example,

*Request*

GET `/api/categories`

*Response*
```json
{
  "success": true,
  "page": 1,
  "num_pages": 1,
  "per_page": 10,
  "total": 6,
  "offset": 0,
  "limit": 6,
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    ...
  ]
}
```
*Request*

GET `/api/categories?pagination=n&type=map`

*Response*
```json
{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

#### Category By Id
An individual category retrieved by id. 

|                   | Description |
|------------------:|-------------|
| **Endpoint**      | `/api/categories/<category_id>` <br> where `<category_id>` is the id of the requested category |
| **Method**        | GET |
| **Query**         | - |
| **Request Body**  | - |
| **Data type**     | - |
| **Content-Type**  | - |
| **Response**      | 200 - OK|
| **Response Body** | A [Success Response](#success-response) with the *payload* attribute named `category`. |
| `category`        | a [Category Entity](#category-entity) |
| **Errors**        | 404 - NOT FOUND |

For example,

*Request*

GET `/api/categories/1`

*Response*
```json
{
  "success": true,
  "category": {
    "id": 1,
    "type": "Science"
  }
}
```

#### Questions By Category Id
A listing of all questions for a particular category. This endpoint returns a [Paginated Response](#paginated-response).

|                   | Description |
|------------------:|-------------|
| **Endpoint**      | `api/categories/<category_id>/questions` <br> where `<category_id>` is the id of the requested category |
| **Method**        | GET |
| **Query**         | - |
| **Request Body**  | - |
| **Data type**     | - |
| **Content-Type**  | - |
| **Response**      | 200 - OK|
| **Response Body** | A [Paginated Response](#paginated-response) with a multi-part *payload*. <br> **Note:** The `total` attribute in the standard paginated response is named `total_questions`. |
| `questions`       | a list of [Question Entity](#question-entity) |
| `categories`      | a [Category Map](#category-map) |
| `current_category`| requested category id |
| **Errors**        | 404 - NOT FOUND |

For example,

*Request*

GET `/api/categories/1/questions`

*Response*
```json
{
  "success": true,
  "page": 1,
  "num_pages": 3,
  "per_page": 10,
  "total_questions": 29,
  "offset": 0,
  "limit": 10,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 16,
      "match": "liver",
      "question": "What is the heaviest organ in the human body?"
    },
    ...
  ]
}
```

#### Questions
A listing of all questions. This endpoint returns a [Paginated Response](#paginated-response).

|                   | Description |
|------------------:|-------------|
| **Endpoint**      | `/api/questions` |
| **Method**        | GET |
| **Query**         | See [Paginated Request](#paginated-request) |
| **Request Body**  | - |
| **Data type**     | - |
| **Content-Type**  | - |
| **Response**      | 200 - OK|
| **Response Body** | A [Paginated Response](#paginated-response) with a multi-part *payload*. <br> **Note:** The `total` attribute in the standard paginated response is named `total_questions`. |
| `questions`       | a list of [Question Entity](#question-entity) |
| `categories`      | a [Category Map](#category-map) |
| **Errors**        | 400 - BAD REQUEST |

##### Question Entity
A question entity contains the following attributes

`id`: question id <br>`question`: question text <br>`answer`: answer text <br>`match`: space-separated list of words to match from answer to be considered correct <br>`category`: id of question category <br>`difficulty`: difficulty value; range *1-5*

For example,

*Request*

GET `/api/questions`

*Response*
```json
{
  "success": true,
  "page": 1,
  "per_page": 10,
  "num_pages": 18,
  "total_questions": 175,
  "offset": 0,
  "limit": 10,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "id": 1,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
      "answer": "Maya Angelou",
      "match": "maya angelou",
      "category": 4,
      "difficulty": 2
    },
    ...
  ]
}
```

#### Question By Id
An individual question retrieved by id.

|                   | Description |
|------------------:|-------------|
| **Endpoint**      | `/api/questions/<question_id>` <br> where `<question_id>` is the id of the requested question |
| **Method**        | GET |
| **Query**         | - |
| **Request Body**  | - |
| **Data type**     | - |
| **Content-Type**  | - |
| **Response**      | 200 - OK|
| **Response Body** | A [Success Response](#success-response) with the *payload* attribute named `question`. |
| `question`        | a [Question Entity](#question-entity) |
| **Errors**        | 404 - NOT FOUND |

For example,

*Request*

GET `/api/questions/1`

*Response*
```json
{
  "success": true,
  "question": {
    "id": 1,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
    "answer": "Maya Angelou",
    "match": "maya angelou",
    "category": 4,
    "difficulty": 2
  }
}
```

#### Create Question
Add a new question. In the event a question with the same question text already exists, the request is rejected.

|                   | Description |
|------------------:|-------------|
| **Endpoint**      | `/api/questions` |
| **Method**        | POST |
| **Query**         | - |
| **Request Body**  | `question`: question text <br>`answer`: answer text <br>`category`: id of category to which the questions belongs <br>`difficulty`: difficulty value; range *1-5* |
| **Data type**     | json |
| **Content-Type**  | application/json |
| **Response**      | 201 - CREATED |
| **Response Body** | A [Success Response](#success-response) with the *payload* attribute named `created`. |
| `created`         | number of questions created  |
| **Errors**        | 400 - BAD REQUEST <br> 422 - UNPROCESSABLE ENTITY |

For example,

*Request*

POST `/api/questions`
````json
{
   "question": "1+1",
   "answer": "2",
   "category": 1,
   "difficulty": 1
}
````
*Response*
```json
{
  "success": true,
  "created": 1
}
```

#### Questions Search
A listing of all questions with question text matching the specified search term. This endpoint returns a [Paginated Response](#paginated-response).

|                   | Description |
|------------------:|-------------|
| **Endpoint**      | `/api/questions/search` |
| **Method**        | POST |
| **Query**         | See [Paginated Request](#paginated-request) |
| **Request Body**  | `searchTerm`: question search term |
| **Data type**     | json |
| **Content-Type**  | application/json |
| **Response**      | 200 - OK|
| **Response Body** | A [Paginated Response](#paginated-response) with a multi-part *payload*. <br> **Note:** The `total` attribute in the standard paginated response is named `total_questions`. |
| `questions`       | a list of [Question Entity](#question-entity) |
| `categories`      | a [Category Map](#category-map) |
| **Errors**        | 400 - BAD REQUEST |

For example,

*Request*

POST `/api/questions/search`
```json
{
  "searchTerm": "title"
}
```
*Response*
```json
{
  "success": true,
  "page": 1,
  "per_page": 10,
  "num_pages": 1,
  "total_questions": 6,
  "offset": 0,
  "limit": 6,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 1,
      "match": "maya angelou",
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    ...
  ]
}
```


#### Quiz
Return a randomly selected question from the specified category excluding any questions previously answered.
If no category is specified, a random question is chosen from all questions.

|                   | Description |
|------------------:|-------------|
| **Endpoint**      | `/api/quizzes` |
| **Method**        | GET |
| **Query**         | `num`: number of questions to return, default *1* |
| **Request Body**  | `previous_questions`: a list of ids of previously answered questions <br> `quiz_category`: optional, a [Category Entity](#category-entity) of the selected category |
| **Data type**     | json |
| **Content-Type**  | application/json |
| **Response**      | 200 - OK|
| **Response Body** | A [Success Response](#success-response) with the *payload* attribute named `question` or `questions` |
| `question`        | a [Question Entity](#question-entity) |
| `questions`       | a list of [Question Entity](#question-entity) |
| **Errors**        | 400 - BAD REQUEST |

For example,

*Request*

GET `/api/quizzes`
```json
{
   "previous_questions": [],
   "quiz_category": {
      "type": "Art", 
      "id": "2"
   }
}
```
*Response*
```json
{
   "success": true,
   "question": {
      "id": 54,
      "question": "What are the names of the three \u2018Darling\u2019 children in J.M. Barrie\u2019s \u2018Peter Pan\u2019?"
      "answer": "Wendy, John and Michael",
      "match": "wendy john michael",
      "category": 2,
      "difficulty": 4
   }
}
```
*Request*

GET `/api/quizzes?num=2`
```json
{
   "previous_questions": []
}
```
*Response*
```json
{
   "success": true,
   "questions": [
      {
         "id": 54,
         "question": "What are the names of the three \u2018Darling\u2019 children in J.M. Barrie\u2019s \u2018Peter Pan\u2019?",
         "answer": "Wendy, John and Michael",
         "match": "wendy john michael",
         "category": 2,
         "difficulty": 4
      },
      {
         "id": 73,
         "question": "Alberta is a province of which country?",
         "answer": "Canada",
         "match": "canada",
         "category": 3,
         "difficulty": 1
      }
   ]
}
```

#### Quiz Results
Updates the result totals for the specified user with a quiz result.

|                   | Description |
|------------------:|-------------|
| **Endpoint**      | `/api/quizzes/results` |
| **Method**        | POST |
| **Query**         | - |
| **Request Body**  | `user_id`: id of user <br>`num_correct`: number of correctly answered questions <br>`num_questions`: number of attempted questions |
| **Data type**     | json |
| **Content-Type**  | application/json |
| **Response**      | 200 - OK|
| **Response Body** | A [Success Response](#success-response) with the *payload* attribute named `user` |
| `user`            | a [User Entity](#user-entity) |
| **Errors**        | 400 - BAD REQUEST |

For example,

*Request*

POST `/api/quizzes/results`
```json
{
   "num_correct": 2,
   "num_questions": 6,
   "user_id": 1
}
```
*Response*
```json
{
   "success": true,
   "user": {
      "id": 1,
      "num_correct": 77,
      "num_questions": 214,
      "username": "fred"
   }
}
```


