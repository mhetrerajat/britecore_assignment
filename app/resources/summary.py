import pandas as pd
from flask import current_app as app
from flask.json import jsonify
from flask_restful import Resource, reqparse

from app import auth, db


class SummaryResource(Resource):
    """This class implements API to get summmarized agency performance based on parameters like
    product, year and risk state.
    """
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('agency',
                                   type=str,
                                   required=True,
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
        super(SummaryResource, self).__init__()

    def get(self):
        """Fetches summarized agency performance

        .. :quickref: Fetches summarized agency performance
        
        **Example request**:

        .. http:example:: curl wget httpie python-requests

            GET /api/v1/summary/ HTTP/1.1
            Host: britecore-assignment.herokuapp.com
            Accept: application/json
            Authorization: Basic YWRtaW46YWRtaW4=

            :query agency: 3
            :query year: 2005

        :query string agency (*required*): Unique id of the agency.
        :query string year: Year
        :query string product: Product Name
        :query string risk_state: Risk State
            
        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "data": [
                    {
                    "agency": {
                        "bound_quotes": 50.0, 
                        "earned_premium": 30335.288863636364, 
                        "incurred_losses": 8509.397954545455, 
                        "loss_ratio": 0.10471840079545452, 
                        "new_business_in_written_premium": 1057.5259090909092, 
                        "policy_inforce_quantity": 213.6590909090909, 
                        "prev_policy_inforce_quantity": 224.6590909090909, 
                        "retention_policy_quantity": 201.8181818181818, 
                        "retention_ratio": 0.3957753397954546, 
                        "total_quotes": 392.0, 
                        "total_written_premium": 25521.250909090904
                    }, 
                    "note": "Overall Mean Vs Agency Mean for data with filter on date_id = 2005", 
                    "overall": {
                        "bound_quotes": 45.84079420183933, 
                        "earned_premium": 16729.09540532308, 
                        "incurred_losses": 7149.847685608129, 
                        "loss_ratio": 1285.3961976702374, 
                        "new_business_in_written_premium": 2021.5650989707026, 
                        "policy_inforce_quantity": 172.01193738960959, 
                        "prev_policy_inforce_quantity": 174.63042816249467, 
                        "retention_policy_quantity": 151.39600462878371, 
                        "retention_ratio": 0.3373681922621354, 
                        "total_quotes": 320.8753273646385, 
                        "total_written_premium": 16707.483948474368
                    }, 
                    "summarized_on": "date_id", 
                    "value": "2005"
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
        summary_columns = [
            'retention_policy_quantity', 'policy_inforce_quantity',
            'prev_policy_inforce_quantity', 'new_business_in_written_premium',
            'total_written_premium', 'earned_premium', 'incurred_losses',
            'retention_ratio', 'loss_ratio', 'bound_quotes', 'total_quotes'
        ]

        df.fillna(value=0, inplace=True)

        # Filter out data for given agency id
        agency_df = df.query('agency_id == @args.agency_id')

        # Calculate overall average vs agency average
        query = {k: v for k, v in args.items() if v and k not in ['agency_id']}
        data = []
        if not query:
            app.logger.debug(
                "As other params are not given, calculating summary at agency level"
            )
            # Summary at agency level
            data.append({
                'summarized_on':
                'agency',
                'value':
                args.agency_id,
                'overall':
                df[summary_columns].mean().fillna(value=0).to_dict(),
                'agency':
                agency_df[summary_columns].mean().fillna(value=0).to_dict(),
                'note':
                'Overall Mean Vs Agency Mean'
            })
        else:
            for key, value in query.items():
                _query = '{0} == "{1}"'.format(key, value)
                app.logger.debug(
                    "Calculating summary at {0} level : {1} | {2}".format(
                        key, value, _query))
                tmp = {
                    'summarized_on':
                    key,
                    'value':
                    value,
                    'overall':
                    df.query(_query)[summary_columns].mean().fillna(
                        value=0).to_dict(),
                    'agency':
                    agency_df.query(_query)[summary_columns].mean().fillna(
                        value=0).to_dict(),
                    'note':
                    'Overall Mean Vs Agency Mean for data with filter on {0} = {1}'
                    .format(key, value)
                }
                data.append(tmp)

        response = {'data': data, 'status': 'success', 'message': None}
        return jsonify(response)
