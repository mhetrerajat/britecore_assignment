from flask.json import jsonify
from flask_restful import Resource


class Hello(Resource):
    def get(self):
        return jsonify({
            'data': None,
            'message': 'Hello! Britecore Data Engineer Assignment',
            'status': 'success'
        })
