import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgresql://postgres:medo@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)

    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)

    def test_get_question_unvalid_paginationt(self):
        res = self.client().get('/questions?page=5')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    def test_delete_questions(self):
        # if question with id 10 will success if found or failed if not found
        res = self.client().delete('/questions/10')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)

    def test_add_question(self):
        res = self.client().post('/questions',json={'question':'question','answer':'answer',
        'difficulty':3,'category':1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)

    
    def test_add_question_faild(self):
        res = self.client().post('/questions',json={'question':'','answer':'answer',
        'difficulty':3,'category':1})

        self.assertEqual(res.status_code,422)

    def test_search(self):
        res = self.client().post('/search',json={'searchTerm':'box'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)

    
    def test_get_category(self):
        res = self.client().get('/category/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)

    
    def test_get_category_failed(self):
        res = self.client().get('/category/10/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)


    def test_quizz(self):
        res = self.client().post('/quizzes',json={'previous_questions':[],
        "quiz_category":{'id':0}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()