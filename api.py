import datetime
import logging
import os
from json import JSONDecodeError

import jwt
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from constant.constant import *
from database.models import setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth, JWT_SECRET

app = Flask(__name__)
setup_db(app)
CORS(app)

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/actors', methods=['GET'])
@requires_auth(permission=PERMISSION_READ_ACTOR)
def get_actors():
    query_results = Actor.query.all()
    actors = [actor.format() for actor in query_results]
    return jsonify({"success": True,
                    "actors": actors})


@app.route('/movies', methods=['GET'])
@requires_auth(permission=PERMISSION_READ_MOVIE)
def get_movies():
    query_results = Movie.query.all()
    movies = [movie.format() for movie in query_results]
    return jsonify({"success": True,
                    "movies": movies})

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/actor', methods=['POST'])
@requires_auth(permission=PERMISSION_CREATE_ACTOR)
def create_actor():
    request_body = request.get_json()
    if request_body is None:
        abort(400)
    name = request_body.get('name', None)
    age = request_body.get('age', None)
    gender = request_body.get('gender', None)
    actor = Actor(name, age, gender)
    try:
        actor.insert()
    except (JSONDecodeError, TypeError) as json_error:
        logging.error('Invalid request body: %s', repr(json_error))
        abort(status=400)
    except exc.SQLAlchemyError as e:
        logging.error('Error at creating actor: %s', repr(e))
        actor.rollback()
        abort(status=500)
    return jsonify({"success": True,
                    "actor": actor.format()})


@app.route('/movie', methods=['POST'])
@requires_auth(permission=PERMISSION_CREATE_MOVIE)
def create_movie():
    request_body = request.get_json()
    if request_body is None:
        abort(400)
    title = request_body.get('title', None)
    release_date = request_body.get('release_date', None)
    movie = Movie(title, release_date)
    try:
        movie.insert()
    except (JSONDecodeError, TypeError) as json_error:
        logging.error('Invalid request body: %s', repr(json_error))
        abort(status=400)
    except exc.SQLAlchemyError as e:
        logging.error('Error at creating movie: %s', repr(e))
        movie.rollback()
        abort(status=500)
    return jsonify({"success": True,
                    "movie": movie.format()})

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/actor/<actor_id>', methods=['PATCH'])
@requires_auth(permission=PERMISSION_EDIT_ACTOR)
def update_actor(actor_id):
    try:
        actor = Actor.query.filter(Actor.id == actor_id).one()
    except (exc.NoResultFound, TypeError) as sql_error:
        logging.error('Actor id %s is not found: %s', actor_id, repr(sql_error))
        abort(status=404)

    request_body = request.get_json()
    name = request_body.get('name', None)
    age = request_body.get('age', None)
    gender = request_body.get('gender', None)
    if name is not None:
        actor.name = name
    if age is not None:
        actor.age = age
    if gender is not None:
        actor.gender = gender
    try:
        actor.update()
    except (JSONDecodeError, TypeError) as json_error:
        logging.error('Invalid request body: %s', repr(json_error))
        abort(status=400)
    except exc.SQLAlchemyError as e:
        logging.error('Error at updating actor: %s', repr(e))
        actor.rollback()
        abort(status=500)
    return jsonify({"success": True,
                    "actor": actor.format()})


@app.route('/movie/<movie_id>', methods=['PATCH'])
@requires_auth(permission=PERMISSION_EDIT_MOVIE)
def update_movie(movie_id):
    try:
        movie = Movie.query.filter(Movie.id == movie_id).one()
    except (exc.NoResultFound, TypeError) as sql_error:
        logging.error('Movie id %s is not found: %s', movie_id, repr(sql_error))
        abort(status=404)

    request_body = request.get_json()
    title = request_body.get('title', None)
    release_date = request_body.get('release_date', None)
    if title is not None:
        movie.title = title
    if release_date is not None:
        movie.release_date = release_date
    try:
        movie.update()
    except (JSONDecodeError, TypeError) as json_error:
        logging.error('Invalid request body: %s', repr(json_error))
        abort(status=400)
    except exc.SQLAlchemyError as e:
        logging.error('Error at updating movie: %s', repr(e))
        movie.rollback()
        abort(status=500)
    return jsonify({"success": True,
                    "actor": movie.format()})


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/actor/<actor_id>', methods=['DELETE'])
@requires_auth(permission=PERMISSION_DELETE_ACTOR)
def delete_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one()
    if actor is None:
        abort(status=404)
    try:
        actor.delete()
    except exc.SQLAlchemyError as e:
        logging.error('Error at deleting actor: %s', repr(e))
        actor.rollback()
        abort(status=500)
    return jsonify({"success": True,
                    "delete": actor_id})


@app.route('/movie/<movie_id>', methods=['DELETE'])
@requires_auth(permission=PERMISSION_DELETE_MOVIE)
def delete_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one()
    if movie is None:
        abort(status=404)
    try:
        movie.delete()
    except exc.SQLAlchemyError as e:
        logging.error('Error at deleting movie: %s', repr(e))
        movie.rollback()
        abort(status=500)
    return jsonify({"success": True,
                    "delete": movie_id})


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def handle_unauthorized(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


@app.errorhandler(400)
def handle_forbidden(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Invalid request'
    }), 400


@app.errorhandler(500)
def handle_unexpected_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Unexpected server error'
    }), 500
