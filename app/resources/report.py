import hashlib
import json
from csv import DictWriter
from datetime import datetime
from io import BytesIO, StringIO

from flask import send_file
from flask.json import jsonify
from flask_restful import Resource, marshal, reqparse

from app import auth
from app.utils.report import ReportGenerator
from app.utils.schema import ReportSchema


class BaseReportResource(Resource):
    """This is base class for Report Generation routes
    """
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('group_by',
                                   type=str,
                                   action='append',
                                   choices=('year', 'agency', 'product_line'),
                                   required=True)
        self.reqparse.add_argument('start_year', type=str, required=True)
        self.reqparse.add_argument('end_year', type=str, required=True)
        self.reqparse.add_argument('aggregation',
                                   type=str,
                                   required=False,
                                   default='sum',
                                   choices=('mean', 'sum'))
        self.reqparse.add_argument('agency', type=str, required=False)
        self.reqparse.add_argument('product_line', type=str, required=False)
        super(BaseReportResource, self).__init__()


class ReportResource(BaseReportResource):
    def get(self):
        """Generates reports based on parameters

        .. :quickref: Generate report

        **Example request**:

        .. http:example:: curl wget httpie python-requests

            GET /api/v1/report/ HTTP/1.1
            Host: britecore-assignment.herokuapp.com
            Accept: application/json
            Authorization: Basic YWRtaW46YWRtaW4=

            :query group_by: year
            :query start_year: 2005
            :query end_year: 2007         

        :query string group_by: Columns by which group by is to perform. One of ``year``, ``ageny``, ``hit``, ``product_line``
        :query string start_year: Start year of date range
        :query string end_year: End year of date range
        :query string aggregation: Aggregation function to use. One of ``sum``, ``mean``. Default is ``sum``. Optional
        :query string agency: Agency Id to consider data only specific to that agency. Optional
        :query string product_line: Product Line to consider data only specific to that product line. Optional
            
        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "data": [
                    {
                    "agency": null,
                    "earned_premium": 274675017.4599997,
                    "incurred_losses": 117393349.14999987,
                    "mean_loss_ratio": 1285.3961976702374,
                    "mean_retention_ratio": 0.3373681922621354,
                    "new_business_in_written_premium": 33192077.359999966,
                    "policy_inforce_quantity": 2824264,
                    "product_line": null,
                    "retention_policy_quantity": 2485771,
                    "total_written_premium": 274320178.95000064,
                    "year": "2005"
                    },
                    {
                    "agency": null,
                    "earned_premium": 410581483.9599992,
                    "incurred_losses": 215616372.25999993,
                    "mean_loss_ratio": 910.8174490424989,
                    "mean_retention_ratio": 0.317405557905061,
                    "new_business_in_written_premium": 53898372.57000006,
                    "policy_inforce_quantity": 4223340,
                    "product_line": null,
                    "retention_policy_quantity": 3708433,
                    "total_written_premium": 412880799.3700002,
                    "year": "2006"
                    },
                    {
                    "agency": null,
                    "earned_premium": 408430805.0600007,
                    "incurred_losses": 232238370.9800001,
                    "mean_loss_ratio": 804.9616474706926,
                    "mean_retention_ratio": 0.3063852120589169,
                    "new_business_in_written_premium": 44707526.20999996,
                    "policy_inforce_quantity": 4125077,
                    "product_line": null,
                    "retention_policy_quantity": 3687600,
                    "total_written_premium": 408545579.0100004,
                    "year": "2007"
                    }
                ],
                "message": null,
                "status": "success"
            }

        :resheader Content-Type: application/json
        :statuscode 200: Everything works fine and returns report based on given date range
        :statuscode 400: Invalid request

        """
        args = self.reqparse.parse_args()

        report = ReportGenerator(args)
        df = report.generate()

        response = {
            'data': marshal(df.to_dict('records'), ReportSchema),
            'status': 'success',
            'message': None
        }
        return jsonify(response)


class CSVReportResource(BaseReportResource):
    def get(self):
        """Generate CSV report with premium information

        .. :quickref: Generate CSV report

        **Example request**:

        .. http:example:: curl wget httpie python-requests

            GET /api/v1/report/csv HTTP/1.1
            Host: britecore-assignment.herokuapp.com
            Accept: text/csv
            Authorization: Basic YWRtaW46YWRtaW4=

            :query group_by: year
            :query start_year: 2005
            :query end_year: 2007         

        :query string group_by: Columns by which group by is to perform. One of ``year``, ``ageny``, ``hit``, ``product_line``
        :query string start_year: Start year of date range
        :query string end_year: End year of date range
        :query string aggregation: Aggregation function to use. One of ``sum``, ``mean``. Default is ``sum``. Optional
        :query string agency: Agency Id to consider data only specific to that agency. Optional
        :query string product_line: Product Line to consider data only specific to that product line. Optional
            
        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: text/csv

            2005,2485771,2824264,33192077.359999966,274320178.95000064,274675017.4599997,117393349.14999987,0.3373681922621354,1285.3961976702374
            2006,3708433,4223340,53898372.57000006,412880799.3700002,410581483.9599992,215616372.25999993,0.317405557905061,910.8174490424989
            2007,3687600,4125077,44707526.20999996,408545579.0100004,408430805.0600007,232238370.9800001,0.3063852120589169,804.9616474706926

        :resheader Content-Type: text/csv
        :statuscode 200: Everything works fine and returns report based on given date range
        :statuscode 400: Invalid request

        """
        args = self.reqparse.parse_args()

        report = ReportGenerator(args)
        df = report.generate()

        request_params = {k: v for k, v in args.items() if v}
        generate_date = datetime.utcnow().strftime('%Y%m%d')

        filename = "report_{unique_hash}_{generate_date}.csv".format(
            unique_hash=hashlib.md5(
                json.dumps(request_params).encode('utf-8')).hexdigest(),
            generate_date=generate_date)

        buffer = StringIO()
        writer = DictWriter(buffer, df.columns, delimiter=',')
        writer.writeheader()
        for row in df.to_dict('records'):
            writer.writerow(row)

        buffer.seek(0)
        buffer = BytesIO(buffer.read().encode('utf-8'))
        mimetype = 'Content-Type: text/csv; charset=utf-8'

        return send_file(buffer,
                         attachment_filename=filename,
                         as_attachment=True,
                         mimetype=mimetype)
