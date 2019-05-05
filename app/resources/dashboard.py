from flask import render_template, make_response
from flask_restful import Resource


class DashboardResource(Resource):
    def __init__(self):
        pass

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)
