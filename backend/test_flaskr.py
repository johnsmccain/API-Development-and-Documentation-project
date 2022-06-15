import os
import re
from unicodedata import category
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
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format("student","student", 'localhost:5432', self.database_name)

        # self.database_path = "postgres:/{}:{}@{}/{}".format('student','student','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': "who is the father of zoez",
            'answer': 'clatus',
            'category': '1',
            "difficulty": 3
        }

        self.new_category = {
            'id':"1", 
            'type':"Science"
         
        }

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_paginate(self):
        """
            test to get 10 quetions
        """

        res = self.client().get("/questions/")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10)

    # def test_200_on_read_question(self):
    #     res = self.client().get('/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    
        


    def test_create_question(self):
        """
        Test to create a new question successfully
        """
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)

    def test_create_question_with_invalid_data(self):
        """ 
            Test to return error while creating new quetion with 
            an invalid data
        """
        res = self.client().post('/questions', json={"kjdf":''})
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'bad request')

    # def test_200_on_delete_quetion(self):
        """
            Test to delete question successfully
        """
    #     res = self.client().delete('/questions/11')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'],True)
    #     self.assertEqual(data['deleted'], 11)
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(data['questions'])

    def test_delete_question_invalid_id(self):
        """
            Test to return Error when exceeding the 
            available question
        """
        res = self.client().delete('/questions/2004')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_fetch_categorie(self):
        """
            Test to successfully fetch categories
        """
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])

    def test_out_range_categoryId(self):
        """
            Test to return Error while atempting to retrieve
            a  category with an id the does not exist 
        """
        res = self.client().get('/categorie/200')
        data = json.loads(res.data)

        # self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_fetching_questions(self):
        """
            Test to fetch all questions successfully
        """
        res = self.client().get('/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])

    def test_question_invalid_fetch(self):
        """
            Test to return Error while atempting to retrieve
            a  question with an id the does not exist 
        """
        res = self.client().get('/questions/10000')
        data = json.loads(res.data)

        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'method not found')
        self.assertEqual(data['status'],405)

    def test_valid_search(self):
        """Test success to search for question with valid data """
        res = self.client().post('/questions/search', json={'searchTerm': "who"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_invalid_search(self):

        """Test to search question with invalid data"""
        res = self.client().post('/questions/search', json={'idonknow':'why'})
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['status'], 404)

    def test_valid_trivia(self):
        """Test for valid trivia list"""
        res = self.client().post('/quizzes', json={
            "previous_questions": [8, 12],
            "quiz_category": {"type": "Science", "id": "1"}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_invalid_trivia(self):
        """Test to get trivia error when provided with 
        invalid data"""
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()