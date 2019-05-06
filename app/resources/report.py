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
        """
            Generates reports based on parameters
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
        """
            Generate CSV report with premium information
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
