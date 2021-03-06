# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

Original base code available at https://github.com/udacity/FSND/tree/master/projects/02_trivia_api/starter as part of [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044) by Udacity.

## Tasks

There are `TODO` comments throughout project. Start by reading the READMEs in:

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

We recommend following the instructions in those files in order. This order will look familiar from our prior work in the course.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup.

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency.

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API.

[View the README.md within ./frontend for more details.](./frontend/README.md)


## Implementation
### Features
* An additional field has been added to the questions table to specify the words to be matched to determine if the supplied answer is correct. 
  [Natural Language Toolkit](https://www.nltk.org/) is used to remove stop words from answers, to improve answer check accuracy.
    > To avoid the necessity to download the required NTLK Stopwords Corpus and tokeniser, they are included in the [backend/nltk_data](backend/nltk_data) folder, and the application appends this folder to the default NLTK data paths. 
* Users have been added to the database, and their overall game score is tracked. Users are auto-registered on initial login.
* The frontend application has been re-styled.
* The project structure has been reorganised to aid maintenance.

> Please see the backend [README.md](backend/README.md) for details of how to configure and run the application.
> 
> The API documentation is available at [API](backend/README.md#api).


#### Project Structure
The application is structure as follows:
  ```shell
  ????????? README.md
  ????????? backend               - backend application
  ???   ????????? flaskr            - backend application code
  ???   ???   ????????? controller    - controllers for processing API requests
  ???   ???   ????????? model         - database ORM models
  ???   ???   ????????? service       - service layer interfacing between controllers and database
  ???   ???   ????????? util          - miscellaneous application code
  ???   ????????? migrations        - database management
  ???   ????????? nltk_data         - NLTK data files, see XXXXX
  ???   ????????? setup             - setup related files
  ???   ????????? test              - unittest test scripts
  ???   ????????? config.py         - application configuration
  ???   ????????? requirements.txt  - The dependencies to be installed with "pip3 install -r requirements.txt"
  ???   ????????? secrets.py        - Database URLs, see [Database setup](./backend/README.md#database-setup)
  ???   ????????? test_config.py    - unittest application configuration
  ????????? frontend              - frontend application
      ????????? public            - static web files
      ????????? src               - React source files
  ```
