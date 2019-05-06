from flask import make_response
from flask.json import jsonify
from flask_restful import Resource, reqparse

from app import db
from app.exceptions import (ApiException, RequirementParameterMissing,
                            UserAlreadyExistsException)
from app.models import User


class Register(Resource):
    """This class implements methods to create new user which will eventually used in HTTP Basic Auth
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username',
                                   type=str,
                                   required=True,
                                   location="json",
                                   help="username cannot be blank!")
        self.reqparse.add_argument('password',
                                   type=str,
                                   required=True,
                                   location="json",
                                   help="password cannot be blank!")

        super(Register, self).__init__()

    def post(self):
        """This method creates new user using parameters given in request

        .. :quickref: Create New User
        
        **Example request**:

        .. http:example:: curl wget httpie python-requests

            POST /api/v1/auth/register HTTP/1.1
            Host: britecore-assignment.herokuapp.com
            Accept: application/json
            Content-Type: application/json

            {
            "username": "dummy",
            "password": "dummy"
            }

        :jsonparam string username: Alphanumeric username of an user
        :jsonparam string password: Password
            
        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {"data":{"username":"dummy"},"message":"User created successfully!","status":"success"}

        :resheader Content-Type: application/json
        :statuscode 200: Everything works fine and user has been created
        :statuscode 400: Invalid request or user already exists

        :raises RequirementParameterMissing: When any required parameters are missing in request
        :raises UserAlreadyExistsException: When another user exists with same username
        """
        args = self.reqparse.parse_args()

        if any([not args.username, not args.password]):
            raise RequirementParameterMissing(args)

        user = User.query.filter_by(username=args.username).first()
        if user:
            raise UserAlreadyExistsException(args.username)

        user = User(args.username, args.password)
        db.session.add(user)
        db.session.commit()

        response = {
            'data': {
                'username': args.username
            },
            'message': "User created successfully!",
            'status': 'success'
        }

        return make_response(jsonify(response))
