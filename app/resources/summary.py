import pandas as pd
from flask import current_app as app
from flask.json import jsonify
from flask_restful import Resource, marshal, reqparse

from app import auth, db
from app.utils.schema import SummarySchema


class SummaryResource(Resource):
    """This class implements API to filter out information from facts table based on various
    attributes.
    """
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('agency',
                                   type=str,
                                   required=False,
                                   dest='agency_id')
        self.reqparse.add_argument('year',
                                   type=str,
                                   required=False,
                                   dest='date_id')
        self.reqparse.add_argument('product',
                                   type=str,
                                   required=False,
                                   dest='product_id')
        self.reqparse.add_argument('risk_state',
                                   type=str,
                                   required=False,
                                   dest='risk_state_id')
        self.reqparse.add_argument('offset',
                                   type=int,
                                   required=False,
                                   default=0)
        self.reqparse.add_argument('limit',
                                   type=int,
                                   required=False,
                                   default=25)
        super(SummaryResource, self).__init__()

    def get(self):
        """
            Fetches summarised information by filters
        """
        args = self.reqparse.parse_args()
        df = pd.read_sql_table('facts', db.engine)

        df.fillna(value=0, inplace=True)

        # Apply filter query
        query = {
            k: v
            for k, v in args.items() if v and k not in ['offset', 'limit']
        }
        for key, value in query.items():
            _query = "{0} == @value".format(key)
            df = df.query(_query)

        # Limit rows
        df = df.iloc[args.offset:args.offset + args.limit]

        app.logger.debug(
            "Returing {0} rows after applying filters : {1}".format(
                df.shape[0], query))

        response = {
            'data': marshal(df.to_dict('records'), SummarySchema),
            'status': 'success',
            'message': None
        }
        return jsonify(response)
