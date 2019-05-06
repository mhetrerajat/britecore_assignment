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
