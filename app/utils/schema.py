"""This module implements various schemas which will be used to marshal the complex objects
at the time of generating response. These schemas act as filter to limit attributes that to be
shown in response and validates their data types.

- Schemas
    -   AgencySchema : Used in agency specific resources
    -   SummarySchema: Used for limiting the number of attributes in response of all resources associated with facts table
    -   ReportSchema: Used in case of report resources
"""

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

ReportSchema = {
    'agency': fields.String(attribute='agency_id'),
    'product_line': fields.String(attribute='line'),
    'year': fields.String(attribute='date_id'),
    'retention_spolicy_quantity': fields.Float,
    'policy_inforce_quantity': fields.Float,
    'new_business_in_written_premium': fields.Float,
    'total_written_premium': fields.Float,
    'earned_premium': fields.Float,
    'incurred_losses': fields.Float,
    'mean_retention_ratio': fields.Float,
    'mean_loss_ratio': fields.Float
}
