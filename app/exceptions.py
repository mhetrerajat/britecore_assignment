"""This modules has custom implemented Exceptions
"""
from flask import jsonify


class ApiException(Exception):
    """This is base exception class of API inherited from Python's Exception Class.
    
    :param message: Human readable string describing the exception
    :type message: str
    :param status: HTTP Response Code
    :type status: int
    """

    def __init__(self, message, status=400, *args, **kwargs):
        self.message = message
        self.status = status

    def get_response(self):
        """This method returns response

        :return: Jsonified response dictionary with attributes data, message and status
        :rtype: str
        """
        return jsonify({
            'data': None,
            'message': self.message,
            'status': 'failed'
        }), self.status


class UserAlreadyExistsException(ApiException):
    """Raises when username with given attributes already exists in database

    :param username: Username which raised this exception
    :type username: str
    """

    def __init__(self, username, *args, **kwargs):
        message = "User {0} already exists. Please use different username.".format(
            username)
        super(UserAlreadyExistsException,
              self).__init__(message, *args, **kwargs)


class RequirementParameterMissing(ApiException):
    """Raises when required parameter(s) are missing from the request
    
    :param params: It contains all the attributes which are missing from that request 
    :type params: dict
    """

    def __init__(self, params, *args, **kwargs):
        params = [k for k, _ in params.items()]
        message = "One or more required parameters are missing. Required parameters are : {0}".format(
            ", ".join(params))
        super(RequirementParameterMissing,
              self).__init__(message, *args, **kwargs)
