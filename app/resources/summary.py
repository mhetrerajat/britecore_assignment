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
        """Fetches summarised information by filters

        .. :quickref: Fetches summarised information by filters
        
        **Example request**:

        .. http:example:: curl wget httpie python-requests

            GET /api/v1/summary/ HTTP/1.1
            Host: britecore-assignment.herokuapp.com
            Accept: application/json
            Authorization: Basic YWRtaW46YWRtaW4=

            :query agency: 3
            :query limit: 1

        :query string agency: Unique id of the agency
        :query string year: Year
        :query string product: Product Name
        :query string risk_state: Risk State
        :query int offset: Offset number. Defaults to 0
        :query int limit: Limit the number of records. Defaults to 25
            
        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "data": [
                    {
                    "agency_id": "3",
                    "bound_quotes": 50,
                    "date_id": "2005",
                    "earned_premium": 297840.14,
                    "growth_rate_3_years": 0,
                    "id": 48952,
                    "incurred_losses": 231671.1,
                    "loss_ratio": 0.813821516,
                    "loss_ratio_3_year": 0,
                    "new_business_in_written_premium": 24625.37,
                    "policy_inforce_quantity": 2947,
                    "prev_policy_inforce_quantity": 3031,
                    "product_id": "ANNIV",
                    "retention_policy_quantity": 2780,
                    "retention_ratio": 0.917189047,
                    "risk_state_id": "IN",
                    "total_quotes": 392,
                    "total_written_premium": 284670.65
                    }
                ],
                "message": null,
                "status": "success"
            }

        :resheader Content-Type: application/json
        :statuscode 200: Returns the filterd data
        :statuscode 400: Invalid request
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
