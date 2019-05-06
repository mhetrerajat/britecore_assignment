from flask import make_response, render_template
from flask_restful import Resource

from app import auth


class DashboardResource(Resource):

    decorators = [auth.login_required]

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)
