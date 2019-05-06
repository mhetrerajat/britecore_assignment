import pandas as pd
from flask import current_app as app
from flask.json import jsonify
from flask_restful import Resource, marshal, reqparse

from app import auth, db
from app.exceptions import ApiException
from app.models import DimensionAgency
from app.utils.schema import AgencySchema


class DetailAgency(Resource):
    """This class implements methods to work with multiple agencies. All routes of this resource 
    requires HTTP Basic Auth
    """
    decorators = [auth.login_required]

    def __init__(self):
        #: Parsed request in key value format
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
        """Fetches information about agencies by applying filter
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
        """Creates new agency with parameters passed in request

        :raises ApiException: When agency id is invalid or already exists in database
        """
        args = self.reqparse.parse_args()
        data = {k: v for k, v in args.items() if v}

        if not args.id:
            message = "Agency Id is required to create one."
            app.logger.error(message)
            raise ApiException(message)

        agency = DimensionAgency.query.filter_by(id=args.id).first()
        if agency:
            message = "Agency with given id already exists. Please use another id"
            app.logger.error(message)
            raise ApiException(message)

        app.logger.debug("Adding agency with data : {0}".format(args))

        agency = DimensionAgency(**data)
        db.session.add(agency)
        db.session.commit()

        response = {
            'message': "Successfully created new agency.",
            'data': marshal(data, AgencySchema),
            "status": 'success'
        }
        return jsonify(response)
