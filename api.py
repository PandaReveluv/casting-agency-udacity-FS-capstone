import logging
import os
from json import JSONDecodeError

from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import setup_db
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_drinks():
    query_results = Drink.query.all()
    short_recipe_drinks = [drink.short() for drink in query_results]
    return jsonify({"success": True,
                    "drinks": short_recipe_drinks})


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth(permission="get:drinks-detail")
def get_drinks_detail():
    query_results = Drink.query.all()
    long_recipe_drinks = [drink.long() for drink in query_results]
    return jsonify({"success": True,
                    "drinks": long_recipe_drinks})


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth(permission="post:drinks")
def create_drink():
    request_body = request.get_json()
    recipes = request_body.get('recipe', None)
    title = request_body.get('title', None)
    drink = Drink()
    drink.recipe = json.dumps(recipes)
    drink.title = title
    try:
        if not drink.is_long_recipe():
            logging.error('Invalid data representation')
            abort(status=400)
        drink.insert()
    except (JSONDecodeError, TypeError) as json_error:
        logging.error('Invalid request body: %s', repr(json_error))
        abort(status=400)
    except exc.SQLAlchemyError as e:
        logging.error('Error at creating drink: %s', repr(e))
        drink.rollback()
        abort(status=500)
    result = list()
    result.append(drink.long())
    return jsonify({"success": True,
                    "drinks": result})


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


@app.route('/drinks/<drink_id>', methods=['PATCH'])
@requires_auth(permission="patch:drinks")
def update_drink(drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one()
    if drink is None:
        abort(status=404)

    request_body = request.get_json()
    recipes = request_body.get('recipe', None)
    title = request_body.get('title', None)
    if recipes is not None:
        drink.recipe = json.dumps(recipes)
    if title is not None:
        drink.title = title
    try:
        if drink.recipe is not None and not drink.is_long_recipe():
            logging.error('Invalid data representation')
            abort(status=400)
        drink.update()
    except (JSONDecodeError, TypeError) as json_error:
        logging.error('Invalid request body: %s', repr(json_error))
        abort(status=400)
    except exc.SQLAlchemyError as e:
        logging.error('Error at updating drink: %s', repr(e))
        drink.rollback()
        abort(status=500)
    result = list()
    result.append(drink.long())
    return jsonify({"success": True,
                    "drinks": result})


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


@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth(permission="delete:drinks")
def delete_drink(drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one()
    if drink is None:
        abort(status=404)
    try:
        drink.delete()
    except exc.SQLAlchemyError as e:
        logging.error('Error at updating drink: %s', repr(e))
        drink.rollback()
        abort(status=500)
    return jsonify({"success": True,
                    "delete": drink_id})


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
        "message": "resource not found"
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
