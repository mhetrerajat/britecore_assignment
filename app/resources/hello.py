import numpy as np
from flask.json import jsonify
from flask_restful import Resource

from app import auth
from app.models import DimensionProduct, Facts


class Hello(Resource):
    """Introduction"""

    def get(self):
        """Says Hello

        .. :quickref: Introduction

        **Example request**:

        .. http:example:: curl wget httpie python-requests

          GET /api/v1/ HTTP/1.1
          Host: britecore-assignment.herokuapp.com
          Accept: application/json

        **Example response**:

        .. sourcecode:: http

          HTTP/1.1 200 OK
          Vary: Accept
          Content-Type: application/json

          {
            "data": null,
            "message": "Hello! Britecore Data Engineer Assignment",
            "status": "success"
          }

        :resheader Content-Type: application/json
        :status 200: Say Hello
        """
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

        .. :quickref: Fetches all the unique values for date, agency and product line columns

        **Example request**:

        .. http:example:: curl wget httpie python-requests

            GET /api/v1/distinct HTTP/1.1
            Host: britecore-assignment.herokuapp.com
            Accept: application/json
            Authorization: Basic YWRtaW46YWRtaW4=

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "data": {
                    "date_id": ["2005", "2006"],
                    "agency_id": ["1034", "148"],
                    "line": ["CL", "PL"]
                },
                "message": null,
                "status": "success"
            }

        :reqheader Authorization: Basic Auth Required
        :resheader Content-Type: application/json
        :statuscode 200: Everything works fine.
        :statuscode 400: Invalid request
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
