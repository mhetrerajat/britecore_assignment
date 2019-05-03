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

SummarySchema = {
    'id': fields.Integer,
    'retention_policy_quantity': fields.Integer,
    'policy_inforce_quantity': fields.Integer,
    'prev_policy_inforce_quantity': fields.Integer,
    'new_business_in_written_premium': fields.Float,
    'total_written_premium': fields.Float,
    'earned_premium': fields.Float,
    'incurred_losses': fields.Float,
    'retention_ratio': fields.Float,
    'loss_ratio': fields.Float,
    'loss_ratio_3_year': fields.Float,
    'growth_rate_3_years': fields.Float,
    'bound_quotes': fields.Integer,
    'total_quotes': fields.Integer,
    'date_id': fields.String,
    'agency_id': fields.String,
    'product_id': fields.String,
    'risk_state_id': fields.String
}
