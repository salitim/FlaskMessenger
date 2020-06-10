import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from sqlalchemy.sql.expression import func
import random
import json

from models import setup_db, Room, Message
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={r"*": {"origins": "*"}},
         supports_credentials=True)
    '''
  after_request decorator to set Access-Control-Allow
  '''
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/', methods=['GET'])
    def get_home():
        return "hello home"

    @app.route('/messages/', methods=['GET'])
    def get_messages():
        try:
            messages = Message.query.all()
            formated_messages = [
                message.format() for message in messages]
            return jsonify({
                'success': True,
                'messages': formated_messages
            })
        except:
            abort(422)

    @app.route('/rooms/', methods=['GET'])
    def get_rooms():
        return "hello home"

    @app.route('/messages/', methods=['POST'])
    def new_message():
        return "hello home"

    @app.route('/messages/', methods=['PATCH'])
    def update_message():
        return "hello home"

    @app.route('/messages/', methods=['DELETE'])
    def delete_message():
        return "hello home"

        # Error Handling
    '''
    error handling for unprocessable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    '''
        implement error handler for 404
        error handler should conform to general task above 
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    '''
        error handler for AuthError
        error handler should conform to general task above 
    '''

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app
