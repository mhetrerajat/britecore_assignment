from flask import make_response, render_template
from flask_restful import Resource

from app import auth


class DashboardResource(Resource):
    """This class implements all the methods support by dashboard route. 
    This route requires HTTP Basic Auth to access.
    """

    decorators = [auth.login_required]

    def get(self):
        """Access Dashboard

        .. :quickref: Dashboard

        **Example request**:

        .. http:example:: curl

            GET / HTTP/1.1
            Host: britecore-assignment.herokuapp.com
            Authorization: Basic YWRtaW46YWRtaW4=
        """
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)
