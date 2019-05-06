from flask import make_response, render_template
from flask_restful import Resource

from app import auth


class DashboardResource(Resource):
    """This class implements all the methods support by dashboard route. 
    This route requires HTTP Basic Auth to access.
    """

    decorators = [auth.login_required]

    def get(self):
        """This method implements GET method of route
        """
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)
