import os

from flask import Flask, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from app.exceptions import ApiException
from config import config

db = SQLAlchemy()
auth = HTTPBasicAuth()


@auth.error_handler
def unauthorized():
    return make_response(
        jsonify({
            'message': 'Unauthorized access',
            'status': 'failed',
            'data': None
        }), 401)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    dashboard = Api(app, prefix="/")
    api = Api(app, prefix="/api/v1")
    auth_api = Api(app, prefix='/api/v1/auth')
    detail_api = Api(app, prefix="/api/v1/detail")
    summary_api = Api(app, prefix="/api/v1/summary")
    report_api = Api(app, prefix="/api/v1/report")

    # Dashboard Resource
    from app.resources.dashboard import DashboardResource
    dashboard.add_resource(DashboardResource, '')

    from app.resources.hello import Hello, DistinctResource
    api.add_resource(Hello, '/')
    api.add_resource(DistinctResource, '/distinct')

    # Auth Resources
    from app.resources.register import Register
    auth_api.add_resource(Register, '/register')

    # Detail Resources
    from app.resources.detail_agency_item import DetailAgencyItem
    detail_api.add_resource(DetailAgencyItem, '/agency/<string:agency_id>')

    from app.resources.detail_agency import DetailAgency
    detail_api.add_resource(DetailAgency, '/agency')

    # Summary Resources
    from app.resources.summary import SummaryResource
    summary_api.add_resource(SummaryResource, '/')

    # Report Resources
    from app.resources.report import ReportResource, CSVReportResource
    report_api.add_resource(ReportResource, '/')
    report_api.add_resource(CSVReportResource, '/csv')

    # Error Handler
    @app.errorhandler(ApiException)
    def handle_api_error(error):
        return error.get_response()

    return app
