from flask.json import jsonify
from flask_restful import Resource

import pandas as pd
from app import db
from app.models import Facts, DimensionProduct
import numpy as np


class Hello(Resource):
    def get(self):
        return jsonify({
            'data': None,
            'message': 'Hello! Britecore Data Engineer Assignment',
            'status': 'success'
        })


class DistinctResource(Resource):
    def get(self):
        """
            Fetches all the unique values for date, agency and product line columns
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