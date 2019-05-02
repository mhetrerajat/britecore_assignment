from flask_restful import fields

AgencySchema = {
    'id': fields.String,
    'active_producers': fields.Integer,
    'agency_appointment_year': fields.Integer,
    'comissions_end_year': fields.Integer,
    'comissions_start_year': fields.Integer,
    'max_age': fields.Integer,
    'min_age': fields.Integer,
    'vendor': fields.String
}