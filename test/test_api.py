import os
import unittest
import json
from unittest.mock import patch

import api

from constant.constant import *
from database.models import Movie, Actor
from dotenv import load_dotenv


class CastingAgencyTestCase(unittest.TestCase):
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

        if Movie.query.get(1) is None:
            init_movie = Movie("Title", "2024-09-07 21:39:45.859")
            init_movie.id = 1
            init_movie.insert()
        if Actor.query.get(1) is None:
            init_actor = Actor("Actor", 20, "Male")
            init_actor.id = 1
            init_actor.insert()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def prepare_data_for_delete(self):
        init_actor = Actor("InitName", 20, "Male")
        init_actor.id = 404
        init_actor.clean_all_data()
        init_actor.insert()
        init_movie = Movie("InitTitle", "2024-09-07 21:39:45.859")
        init_movie.id = 404
        init_movie.clean_all_data()
        init_movie.insert()

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

    def test_get_actors_when_authorization_is_missing_return_401(self):
        res = self.client().get(
            "/actors"
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"], "Authorization header is expected.")

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

    def test_get_movies_when_authorization_is_missing_return_401(self):
        res = self.client().get(
            "/movies"
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_create_actor_return_200_OK(self):
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

    def test_create_actor_when_invalid_body_return_400(self):
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
            json=None)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], "Invalid request")

    def test_create_actor_when_not_allow_permission_return_403(self):
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       "Dummy Permission"
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
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], "Invalid permission.")

    def test_create_actor_when_authorization_is_missing_return_401(self):
        res = self.client().post(
            "/actor",
            json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_create_movie_return_200_OK(self):
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       PERMISSION_CREATE_MOVIE
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().post(
            "/movie",
            headers={
                'Authorization': 'Bearer dummy',
            },
            json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie']['id'])
        self.assertTrue(data['movie']['title'])
        self.assertTrue(data['movie']['release_date'])

    def test_create_movie_when_invalid_body_return_400(self):
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       PERMISSION_CREATE_MOVIE
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().post(
            "/movie",
            headers={
                'Authorization': 'Bearer dummy',
            },
            json=None)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], "Invalid request")

    def test_create_movie_when_not_allow_permission_return_403(self):
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       "Dummy Permission"
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().post(
            "/movie",
            headers={
                'Authorization': 'Bearer dummy',
            },
            json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], "Invalid permission.")

    def test_create_movie_when_authorization_is_missing_return_401(self):
        res = self.client().post(
            "/movie",
            json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_edit_actor_return_200_OK(self):
        to_be_edit_actor = {
            "name": "Test2",
            "age": 46,
            "gender": "Female"
        }
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       PERMISSION_EDIT_ACTOR
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().patch(
            "/actor/1",
            headers={
                'Authorization': 'Bearer dummy',
            },
            json=to_be_edit_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor']['name'])
        self.assertTrue(data['actor']['age'])
        self.assertTrue(data['actor']['gender'])

    def test_edit_actor_when_id_is_not_found_return_404(self):
        to_be_edit_actor = {
            "name": "Test2",
            "age": 46,
            "gender": "Female"
        }
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       PERMISSION_EDIT_ACTOR
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().patch(
            "/actor/999",
            headers={
                'Authorization': 'Bearer dummy',
            },
            json=to_be_edit_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "Resource not found")

    def test_edit_actor_when_invalid_body_return_400(self):
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       PERMISSION_EDIT_ACTOR
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().patch(
            "/actor/1",
            headers={
                'Authorization': 'Bearer dummy',
            },
            json=None)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], "Invalid request")

    def test_edit_actor_when_not_allow_permission_return_403(self):
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       "Dummy Permission"
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().patch(
            "/actor/1",
            headers={
                'Authorization': 'Bearer dummy',
            },
            json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], "Invalid permission.")

    def test_edit_actor_when_authorization_is_missing_return_401(self):
        res = self.client().patch(
            "/actor/1",
            json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_edit_movie_return_200_OK(self):
        to_be_edit_movie = {
            "title": "Test_edit",
            "release_date": "2024-09-07 21:39:45.859"
        }
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       PERMISSION_EDIT_MOVIE
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().patch(
            "/movie/1",
            headers={
                'Authorization': 'Bearer dummy',
            },
            json=to_be_edit_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor']['title'])
        self.assertTrue(data['actor']['release_date'])

    def test_edit_movie_when_id_is_not_found_return_404(self):
        to_be_edit_movie = {
            "title": "Test_edit",
            "release_date": "2024-09-07 21:39:45.859"
        }
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       PERMISSION_EDIT_MOVIE
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().patch(
            "/movie/999",
            headers={
                'Authorization': 'Bearer dummy',
            },
            json=to_be_edit_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "Resource not found")

    def test_edit_movie_when_invalid_body_return_400(self):
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       PERMISSION_EDIT_MOVIE
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().patch(
            "/movie/1",
            headers={
                'Authorization': 'Bearer dummy',
            },
            json=None)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], "Invalid request")

    def test_edit_movie_when_not_allow_permission_return_403(self):
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       "Dummy Permission"
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().patch(
            "/movie/1",
            headers={
                'Authorization': 'Bearer dummy',
            },
            json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], "Invalid permission.")

    def test_edit_movie_when_authorization_is_missing_return_401(self):
        res = self.client().patch(
            "/movie/1",
            json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_delete_actor_return_200_OK(self):
        self.prepare_data_for_delete()
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       PERMISSION_DELETE_ACTOR
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().delete(
            "/actor/404",
            headers={
                'Authorization': 'Bearer dummy',
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['delete'], "404")

    def test_delete_actor_when_id_is_not_found_return_404(self):
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       PERMISSION_DELETE_ACTOR
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().delete(
            "/actor/999",
            headers={
                'Authorization': 'Bearer dummy',
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "Resource not found")

    def test_delete_actor_when_not_allow_permission_return_403(self):
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       "Dummy Permission"
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().delete(
            "/actor/1",
            headers={
                'Authorization': 'Bearer dummy',
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], "Invalid permission.")

    def test_delete_actor_when_authorization_is_missing_return_401(self):
        res = self.client().delete(
            "/actor/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_delete_movie_return_200_OK(self):
        self.prepare_data_for_delete()
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       PERMISSION_DELETE_MOVIE
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().delete(
            "/movie/404",
            headers={
                'Authorization': 'Bearer dummy',
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['delete'], "404")

    def test_delete_movie_when_id_is_not_found_return_404(self):
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       PERMISSION_DELETE_MOVIE
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().delete(
            "/movie/999",
            headers={
                'Authorization': 'Bearer dummy',
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "Resource not found")

    def test_delete_movie_when_not_allow_permission_return_403(self):
        mock_jwt_token = patch('auth.auth.verify_decode_jwt',
                               return_value={
                                   'user_id': "dummy",
                                   'permissions': [
                                       "Dummy Permission"
                                   ]
                               })
        mock_jwt_token.start()
        res = self.client().delete(
            "/movie/1",
            headers={
                'Authorization': 'Bearer dummy',
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], "Invalid permission.")

    def test_delete_movie_when_authorization_is_missing_return_401(self):
        res = self.client().delete(
            "/movie/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"], "Authorization header is expected.")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
