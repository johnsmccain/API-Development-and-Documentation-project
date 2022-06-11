
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import null

# import sqlalchemy

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatedQuestions = [question.format() for question in selection]
    return formatedQuestions[start:end]

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    db = SQLAlchemy(app)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def agter_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers","Content-Type, Authorization, true"
        )
        response.headers.add(
            "Access-Controll-Allow-Methods","GET, PUT, POST, DELETE, OPTIONS"
        )
        return response
    """

    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    current_category = null
    @app.route('/categories')
    def read_categories():
        try:
            category = Category.query.all()
            formated_data = [data.format() for data in category]
            return jsonify({
                'success': True,
                'categories': formated_data,
            })
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    
    @app.route("/questions/")
    def read_questions():
        selections = Question.query.all()
        formatData = paginate(request, selections)
        categories = Category.query.all()
        formatedCategories = [category.format() for category in  categories]
        # currentCategory = Category.query.filter( formatData.category== id ).one_or_none()
        # print(formatData)
        # print(i for i in formatedCategories)
        # print(categories)
        # catObj ={}
        # for i in formatedCategories:
        #     catObj[i['id']] = i["type"]
        # print(catObj)
        if len(formatData) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "questions": formatData,
            "total_questions": len(selections),
            "categories": formatedCategories,
            # "current_category": current_category.type if current_category else 
            
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            question.delete()
            dqQuestions = Question.query.all()
            questions =  paginate(request,  dqQuestions)

            return jsonify({
                'success': True,
                "deleted": question_id,
                "questions": questions,
                'total_questions': len(dqQuestions)
                
            })
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_question = body.get('question', None)
        new_difficulty = body.get('difficulty', None)
        try:
            question = Question(answer=new_answer, question=new_question, category=new_category, difficulty=new_difficulty)

            question.insert()
            return jsonify({
                "success": True,
                "questions": []
            })
        except :
            abort(405)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/search", methods=["POST"])
    def search_term():
        body = request.get_json()
        search_term = body.get("search_term", None)

        selection = Question.query.filter(Question.question.ilike(f'%{search_term}')).all()
        formatedQuestion = paginate(request, selection )
        print(formatedQuestion)
        return jsonify({
            "success": True,
            "questions": formatedQuestion,
            "total_questions": len(selection),
            "current_category": current_category.type if current_category else "all"
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<string:cat_id>/questions")
    def get_categories(cat_id):
        try:
            questions = Question.query.filter(Question.category == cat_id).all()
            current_category = Category.query.filter(Category.id == int(cat_id)).one_or_none()
            if current_category is None:
                abort(404)
            # print(current_category.type)
            return jsonify({
                "success": True,
                "questions": paginate(request, questions),
                # 'questions': result.questions,
                'total_questions': len(questions),
                'current_category': current_category.type,
                
            })
        except:
            abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def quiz_questions():

        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)

        
        selection = Question.query.filter(Question.category == quiz_category['id']).all()
        questions = paginate(request,selection)
        current_question = {}
        count = 0

        for question in questions:
            if len(previous_questions) > 0:
                for prevQuest in previous_questions:
                    # print(question['id'])
                    if prevQuest != question['id']:
                        current_question = question
                        break
            current_question = question
            break
                    
            

        return jsonify({
            "success": True,
            'question': current_question
        })
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

