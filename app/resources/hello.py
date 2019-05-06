import numpy as np
from flask.json import jsonify
from flask_restful import Resource

from app import auth
from app.models import DimensionProduct, Facts


class Hello(Resource):
    def get(self):
        return jsonify({
            'data': None,
            'message': 'Hello! Britecore Data Engineer Assignment',
            'status': 'success'
        })


class DistinctResource(Resource):
    """This class implements methods to fetch distinct values of various columns in facts table.
    All routes requires HTTP Basic Auth
    """
    decorators = [auth.login_required]

    def get(self):
        """Fetches all the unique values for date, agency and product line columns
        """
        data = {
            'date_id':
            np.array(
                Facts.query.with_entities(
                    Facts.date_id).distinct().all()).flatten().tolist(),
            'agency_id':
            np.array(
                Facts.query.with_entities(
                    Facts.agency_id).distinct().all()).flatten().tolist(),
            'line':
            np.array(
                DimensionProduct.query.with_entities(DimensionProduct.line).
                distinct().all()).flatten().tolist(),
        }
        response = {'data': data, 'message': None, 'status': 'success'}
        return jsonify(response)
