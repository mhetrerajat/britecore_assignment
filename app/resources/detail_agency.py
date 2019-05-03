import pandas as pd
from flask import current_app as app
from flask.json import jsonify
from flask_restful import Resource, marshal, reqparse

from app import db
from app.exceptions import ApiException
from app.utils.schema import AgencySchema


class DetailAgency(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('agency_appointment_year',
                                   type=int,
                                   required=False)
        self.reqparse.add_argument('active_producers',
                                   type=int,
                                   required=False)
        self.reqparse.add_argument('comissions_end_year',
                                   type=int,
                                   required=False)
        self.reqparse.add_argument('comissions_start_year',
                                   type=int,
                                   required=False)
        self.reqparse.add_argument('max_age', type=int, required=False)
        self.reqparse.add_argument('min_age', type=int, required=False)

        self.reqparse.add_argument('vendor', type=str, required=False)
        self.reqparse.add_argument('id', type=str, required=False)
        self.reqparse.add_argument('primary_agency', type=str, required=False)
        super(DetailAgency, self).__init__()

    def get(self):
        """
            Fetches information about agencies by applying filter
        """
        args = self.reqparse.parse_args()
        df = pd.read_sql_table('dimension_agency', db.engine)

        # Apply filter query
        query = {k: v for k, v in args.items() if v}
        for key, value in query.items():
            _query = "{0} == @value".format(key)
            df = df.query(_query)

        app.logger.info(
            "Returing {0} agencies after applying filters : {1}".format(
                df.shape[0], query))
        
        df.fillna(value=0, inplace=True)

        response = {
            'data': marshal(df.to_dict('records'), AgencySchema),
            'status': 'success',
            'message': None
        }
        return jsonify(response)

    def post(self):
        args = self.reqparse.parse_args()
        data = {k: v for k, v in args.items() if v}

        if not args.id:
            message = "Agency Id is required to create one."
            app.logger.error(message)
            raise ApiException(message)

        response = {
            'message': "Successfully created new agency.",
            'data': marshal(data, AgencySchema),
            "status": 'success'
        }
        return jsonify(response)
