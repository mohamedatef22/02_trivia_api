import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
from models import setup_db, Question, Category
import json
from random import randint
QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
    @TOD: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/localhost:5000*": {"origins": "*"}})
    '''
    @TOD: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
    @TOD:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    @cross_origin()
    def get_all_categories():
        allCategories = Category.query.all()
        res = {}
        for cat in allCategories:
            res[cat.id] = cat.type
        return jsonify(res)

    '''
    @TOD:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of
    the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''

    @app.route('/questions')
    @cross_origin()
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        allQuestions = Question.query.all()
        if len(allQuestions) <= start:
            abort(404)
        return jsonify({
          "questions": [question.format() for question in
                        allQuestions[start: end]],
          "total_questions": len(allQuestions),
          "categories": [cat.type for cat in Category.query.all()],
        })
    '''
    @TOD:
    Create an endpoint to DELETE question using a question ID.
    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    @cross_origin()
    def delete_question(question_id):
        try:
            Question.query.get(question_id).delete()
            return jsonify({
              "success": True
            })
        except Exception:
            abort(422)

    '''
    @TOD:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at
    the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    @cross_origin()
    def create_question():
        question = request.get_json()['question']
        answer = request.get_json()['answer']
        difficulty = request.get_json()['difficulty']
        category = request.get_json()['category']
        if(question is None or answer is None or difficulty is
           None or category is None or answer == '' or question == ''):
            abort(422)
        else:
            try:
                question_ = Question(question, answer, category, difficulty)
                question_.insert()
                return jsonify({
                  "success": True
                })
            except Exception:
                abort(422)

    '''
    @TOD:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route("/search", methods=['POST'])
    @cross_origin()
    def search():
        searchTerm = json.loads(request.data.decode('utf-8'))
        questions = Question.query.filter(Question.question.ilike(
                    f"%{searchTerm['searchTerm']}%")).all()
        return jsonify({
          "questions": [question.format() for question in questions]
        })

    '''
    @TOD:
    Create a GET endpoint to get questions based on category.
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/category/<int:category_id>/questions')
    @cross_origin()
    def get_questions_by_category(category_id):
        questions = Question.query.filter(Question.category ==
                                          category_id).all()
        if len(questions) == 0:
            abort(404)
        return jsonify({
          "questions": [question.format() for question in questions],
          "current_category": category_id,
          "total_questions": len(questions)
        })
    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    @cross_origin()
    def get_quiz():
        request_ = json.loads(request.data.decode('utf-8'))
        previous_questions = request_['previous_questions']
        quiz_category = request_['quiz_category']
        all_questions = []

        if quiz_category["id"] == 0:
            all_questions = Question.query.all()
        else:
            all_questions = Question.query.filter(Question.category ==
                                                  quiz_category["id"]).all()

        for i in range(100000):
            if len(previous_questions) == len(all_questions):
                return jsonify({
                  "game_ended": True
                })
            randomNumber = randint(0, len(all_questions)-1)
            questionId = all_questions[randomNumber].id
            if questionId in previous_questions:
                continue

            return jsonify({
              "question": all_questions[randomNumber].format()
              })

        abort(422)

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          "success": False,
          "error": 404,
          "message": "Not found"
          }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable"
          }), 422
    return app
