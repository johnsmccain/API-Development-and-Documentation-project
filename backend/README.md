# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation:

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
- Example: http://localhost:5000/categories

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```
  ### `GET '/categories/<int:categories_id>/questions'`
  
  - Return a list questions with a given category
  - Results are paginated in groups of 10.
  - Sample http://localhost:5000//categories/2/questions
```json
{
    "current_category": "Art",
    "questions": [
        {
            "answer": "Mona Lisa",
            "category": "2",
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "hsjdh",
            "category": "2",
            "difficulty": 4,
            "id": 24,
            "question": "njasdkjskadjka"
        }
    ],
    "success": true,
    "total_questions": 2
}
```
### `GET '/questions'`
- General:
  - Returns a list of questions, categories, success value and total_questions
  - Result are paginated in groups of 10. Include a request argument to choose page number, starting from 1,
  - Sample: http://localhost:5000/questions
```json
{
    "categories": [
        {
            "id": 1,
            "type": "Science"
        },
        {
            "id": 2,
            "type": "Art"
        },
        {
            "id": 3,
            "type": "Geography"
        },
        {
            "id": 4,
            "type": "History"
        },
        {
            "id": 5,
            "type": "Entertainment"
        },
        {
            "id": 6,
            "type": "Sports"
        }
    ],
    "questions": [
        {
            "answer": "Mona Lisa",
            "category": "2",
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "Blood",
            "category": "1",
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "Scarab",
            "category": "4",
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        },
        {
            "answer": "hsjdh",
            "category": "2",
            "difficulty": 4,
            "id": 24,
            "question": "njasdkjskadjka"
        },
        {
            "answer": "hi",
            "category": "1",
            "difficulty": 1,
            "id": 32,
            "question": "hello "
        },
        {
            "answer": "michael Jackson",
            "category": "4",
            "difficulty": 2,
            "id": 34,
            "question": "who is the king of pop"
        },
       
    ],
    "success": true,
    "total_questions": 17
}
```
### `POST '/questions'`
- General:
  - Create a new question
  - Sample http://localhost:5000/questions/ json = {
            "answer": "Mona Lisa",
            "category": "2",
            "difficulty": 3,
            "question": "La Giaconda is better known as what?"
        }

  ```json
  {
    "questions": [],
    "success": true
  }
  ```
  ### `DELETE '/questions/<int:question_id>'`
- General:
  - Delete question with the given id
  - Sample http://localhost:5000/questions/7
```json
{
  "deleted": 7,
  "success": true
}
```

### `POST '/questions'`
- General:
  - Searches base on searchTerm
  - Returns currentCategory, list of questions, success value and the total numbers of questions related with searchTerm values
  - Sample http://localhost:5000/questions json= {"searchTerm": "who"}

```json
  }
  "currentCategories": null,
  "questions":[
        
        {
            "answer": "michael Jackson",
            "category": "4",
            "difficulty": 2,
            "id": 34,
            "question": "who is the king of pop"
        },
       
    ],
    "success": true,
    "total_questions": 1
  }
```
### `POST '/quizzes'`
- General:
  - Returns a random question and a success value
  - Sample localhost:5000/quizzes/ json = {
    "previous_questions": [8, 12],
    "quiz_category": {"type": "Science", "id": "1"}
}
```json
{
    "question": {
        "answer": "hi",
        "category": "1",
        "difficulty": 1,
        "id": 45,
        "question": "who is the king of pop"
    },
    "success": true
}
```
## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
