from flask import current_app as app
from flask.json import jsonify
from flask_restful import Resource, marshal, reqparse

from app import auth
from app.exceptions import ApiException
from app.models import DimensionAgency
from app.utils.schema import AgencySchema


class DetailAgencyItem(Resource):
    """This class implements all methods associated with agencies. All routes in this resource
    requires HTTP Basic Auth
    """
    decorators = [auth.login_required]

    def __init__(self):
        #: Parsed request in key value format
        self.reqparse = reqparse.RequestParser()
        super(DetailAgencyItem, self).__init__()

    def get(self, agency_id):
        """Fetches all the information about the agency

        .. :quickref: Fetch agency by id
        
        **Example request**:

        .. http:example:: curl wget httpie python-requests

            GET /api/v1/detail/agency/3 HTTP/1.1
            Host: britecore-assignment.herokuapp.com
            Accept: application/json
            Content-Type: application/json
            Authorization: Basic YWRtaW46YWRtaW4=

        :param string agency_id: Unique id of the agency
            
        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "data": {
                    "active_producers": 14,
                    "agency_appointment_year": 1957,
                    "comissions_end_year": 0,
                    "comissions_start_year": 0,
                    "id": "3",
                    "max_age": 85,
                    "min_age": 48,
                    "vendor": "Unknown"
                },
                "message": null,
                "status": "success"
            }

        :resheader Content-Type: application/json
        :statuscode 200: Returns information about the given agency
        :statuscode 400: When agency id is invalid or missing in the request
        
        :param agency_id: Unique id of an agency
        :type agency_id: str
        :raises ApiException: When agency id is invalid or missing in the request
        """
        agency = DimensionAgency.query.filter_by(id=agency_id).first()

        if not agency:
            message = "Invalid agency id : {0}".format(agency_id)
            app.logger.error(message)
            raise ApiException(message)

        response = {
            'data': marshal(agency, AgencySchema),
            'status': 'success',
            'message': None
        }
        return jsonify(response)
