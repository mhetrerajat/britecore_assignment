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
        super(DetailAgency, self).__init__()

    def get(self):
        """Fetches information about agencies by applying filter

        .. :quickref: Fetches information about agencies by applying filter
        
        **Example request**:

        .. http:example:: curl wget httpie python-requests

            GET /api/v1/detail/agency HTTP/1.1
            Host: britecore-assignment.herokuapp.com
            Accept: application/json
            Authorization: Basic YWRtaW46YWRtaW4=

            :query agency_appointment_year: 1999
            :query vendor: C

        :query int agency_appointment_year: Year the agency started doing business
        :query int active_producers: Number of active producers in the agency
        :query int comissions_end_year: Year the agency stopped using the COMMISIONS vendor
        :query int comissions_start_year: Year the agency started using the COMMISIONS vendor
        :query int max_age: Maximum age producer at that agency
        :query int min_age: Minimum age producer at that agency
        :query string vendor: The vendor that the agency subscribes to
        :query string id: Unique id of the agency
            
        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "data": [
                    {
                    "active_producers": 13,
                    "agency_appointment_year": 1999,
                    "comissions_end_year": 0,
                    "comissions_start_year": 0,
                    "id": "2558",
                    "max_age": 72,
                    "min_age": 39,
                    "vendor": "C"
                    },
                    {
                    "active_producers": 15,
                    "agency_appointment_year": 1999,
                    "comissions_end_year": 0,
                    "comissions_start_year": 0,
                    "id": "2565",
                    "max_age": 64,
                    "min_age": 33,
                    "vendor": "C"
                    },
                    {
                    "active_producers": 10,
                    "agency_appointment_year": 1999,
                    "comissions_end_year": 0,
                    "comissions_start_year": 0,
                    "id": "2946",
                    "max_age": 68,
                    "min_age": 46,
                    "vendor": "C"
                    },
                    {
                    "active_producers": 50,
                    "agency_appointment_year": 1999,
                    "comissions_end_year": 2015,
                    "comissions_start_year": 2015,
                    "id": "6084",
                    "max_age": 73,
                    "min_age": 26,
                    "vendor": "C"
                    },
                    {
                    "active_producers": 6,
                    "agency_appointment_year": 1999,
                    "comissions_end_year": 0,
                    "comissions_start_year": 0,
                    "id": "8582",
                    "max_age": 60,
                    "min_age": 53,
                    "vendor": "C"
                    },
                    {
                    "active_producers": 14,
                    "agency_appointment_year": 1999,
                    "comissions_end_year": 0,
                    "comissions_start_year": 0,
                    "id": "9998",
                    "max_age": 83,
                    "min_age": 44,
                    "vendor": "C"
                    }
                ],
                "message": null,
                "status": "success"
                }

        :resheader Content-Type: application/json
        :statuscode 200: Returns list of agencies matching filter criteria
        :statuscode 400: Invalid request

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

        .. :quickref: Create New Agency
        
        **Example request**:

        .. http:example:: curl wget httpie python-requests

            POST /api/v1/detail/agency HTTP/1.1
            Host: britecore-assignment.herokuapp.com
            Accept: application/json
            Content-Type: application/json
            Authorization: Basic YWRtaW46YWRtaW4=

            {
                "id": "999999",
                "agency_appointment_year": 1957,
                "active_producers": 14,
                "max_age": 85,
                "min_age": 48,
                "vendor": "Unknown",
                "comissions_start_year": 2011,
                "comissions_end_year": 2013
            }

        :jsonparam int agency_appointment_year: Year the agency started doing business
        :jsonparam int active_producers: Number of active producers in the agency
        :jsonparam int comissions_end_year: Year the agency stopped using the COMMISIONS vendor
        :jsonparam int comissions_start_year: Year the agency started using the COMMISIONS vendor
        :jsonparam int max_age: Maximum age producer at that agency
        :jsonparam int min_age: Minimum age producer at that agency
        :jsonparam string vendor: The vendor that the agency subscribes to
        :jsonparam string id: Unique id of the agency
            
        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "data": {
                    "active_producers": 14,
                    "agency_appointment_year": 1957,
                    "comissions_end_year": 2013,
                    "comissions_start_year": 2011,
                    "id": "999999",
                    "max_age": 85,
                    "min_age": 48,
                    "vendor": "Unknown"
                },
                "message": "Successfully created new agency.",
                "status": "success"
            }

        :resheader Content-Type: application/json
        :statuscode 200: Creates new agency
        :statuscode 400: When agency id is invalid or already exists in database

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
