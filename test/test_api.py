import os
import unittest
import json
from unittest.mock import patch

import api
from flask_sqlalchemy import SQLAlchemy

from constant.constant import *
from database.models import Movie, Actor
from dotenv import load_dotenv


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        load_dotenv(dotenv_path='../.flaskenv')
        self.database_name = "casting_agency_test"
        self.database_username = os.getenv('TEST_DATABASE_USERNAME')
        self.database_password = os.getenv('TEST_DATABASE_PASSWORD')
        self.database_url = os.getenv('TEST_DATABASE_URL')
        self.database_path = ('postgresql://{}:{}@{}/{}'.format(
            self.database_username,
            self.database_password,
            self.database_url,
            self.database_name))

        self.app = api.app
        self.app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path

        self.client = self.app.test_client

        self.new_actor = {
            "name": "Test99",
            "age": 56,
            "gender": "Female"
        }

        self.new_movie = {
            "title": "Movie99",
            "release_date": "2024-09-07 21:39:45.859"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_actors_return_200_OK(self):
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       PERMISSION_READ_ACTOR
                                   ]
                               })
        mock_jwt_token.start()

        res = self.client().get(
            "/actors",
            headers={
                'Authorization': 'Bearer dummy',
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["actors"])

    def test_get_actors_when_authorization_is_missing_return_401(self):
        res = self.client().get(
            "/actors"
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_get_actors_when_not_allow_permission_return_403(self):
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       "Dummy Permission"
                                   ]
                               })
        mock_jwt_token.start()

        res = self.client().get(
            "/actors",
            headers={
                'Authorization': 'Bearer dummy',
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], "Invalid permission.")

    def test_get_movies_return_200_OK(self):
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       PERMISSION_READ_MOVIE
                                   ]
                               })
        mock_jwt_token.start()

        res = self.client().get(
            "/movies",
            headers={
                'Authorization': 'Bearer dummy',
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["movies"])

    def test_get_movies_when_authorization_is_missing_return_401(self):
        res = self.client().get(
            "/movies"
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_get_movies_when_not_allow_permission_return_403(self):
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       "Dummy Permission"
                                   ]
                               })
        mock_jwt_token.start()

        res = self.client().get(
            "/movies",
            headers={
                'Authorization': 'Bearer dummy',
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], "Invalid permission.")

    def test_create_actors_return_200_OK(self):
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       PERMISSION_CREATE_ACTOR
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().post(
            "/actor",
            headers={
                'Authorization': 'Bearer dummy',
            },
            json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor']['id'])
        self.assertTrue(data['actor']['name'])
        self.assertTrue(data['actor']['age'])
        self.assertTrue(data['actor']['gender'])

    def test_get_pagination_questions(self):
        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertIsNone(data["currentCategory"])

    def test_get_pagination_questions_not_found(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "Not found")

    def test_delete_question_by_id(self):
        res = self.client().delete("/questions/1")
        self.assertEqual(res.status_code, 204)

    def test_delete_question_by_id_got_bad_request_error(self):
        res = self.client().delete("/questions/dummy")
        self.assertEqual(res.status_code, 400)

    def test_create_question(self):
        res = self.client().post("/question", json=self.new_question)
        self.assertEqual(res.status_code, 204)

    def test_create_question_got_unexpected_error(self):
        error_question = self.new_question.copy()
        error_question["category"] = 1000
        res = self.client().post("/question", json=error_question)
        self.assertEqual(res.status_code, 500)

    def test_search_question(self):
        res = self.client().post("/questions", json=self.search_term)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertIsNone(data['currentCategory'])

    def test_search_question_not_found(self):
        not_found_search_term = self.search_term.copy()
        not_found_search_term['searchTerm'] = 'somedummysearchterm'
        res = self.client().post("/questions", json=not_found_search_term)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "Not found")

    def test_get_questions_by_category_id(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["currentCategory"])

    def test_get_questions_by_category_id_got_bad_request(self):
        res = self.client().get("/categories/dummy/questions")
        self.assertEqual(res.status_code, 400)

    def test_play_quiz(self):
        res = self.client().post("/quizzes", json=self.quiz_body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question']['id'])
        self.assertTrue(data['question']['question'])
        self.assertTrue(data['question']['answer'])
        self.assertTrue(data['question']['category'])
        self.assertTrue(data['question']['difficulty'])

    def test_play_quiz_invalid_request_body(self):
        invalid_request_body = self.quiz_body.copy()
        invalid_request_body['previous_questions'] = None
        res = self.client().post("/quizzes", json=invalid_request_body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
