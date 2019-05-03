from app import db


class Facts(db.Model):
    __tablename__ = "facts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    retention_policy_quantity = db.Column('retention_policy_quantity',
                                          db.Integer)
    policy_inforce_quantity = db.Column('policy_inforce_quantity', db.Integer)
    prev_policy_inforce_quantity = db.Column('prev_policy_inforce_quantity',
                                             db.Integer)
    new_business_in_written_premium = db.Column(
        'new_business_in_written_premium', db.Float)
    total_written_premium = db.Column('total_written_premium', db.Float)
    earned_premium = db.Column('earned_premium', db.Float)
    incurred_losses = db.Column('incurred_losses', db.Float)
    retention_ratio = db.Column('retention_ratio', db.Float)
    loss_ratio = db.Column('loss_ratio', db.Float)
    loss_ratio_3_year = db.Column('loss_ratio_3_year', db.Float)
    growth_rate_3_years = db.Column('growth_rate_3_years', db.Float)
    bound_quotes = db.Column('bound_quotes', db.Integer)
    total_quotes = db.Column('total_quotes', db.Integer)
    date_id = db.Column('date_id',
                        db.String,
                        db.ForeignKey('dimension_date.id'),
                        nullable=False)
    agency_id = db.Column('agency_id',
                          db.String,
                          db.ForeignKey('dimension_agency.id'),
                          nullable=False)
    risk_id = db.Column('risk_state_id',
                        db.String,
                        db.ForeignKey('dimension_risk_state.id'),
                        nullable=False)
    product_id = db.Column('product_id',
                           db.String,
                           db.ForeignKey('dimension_product.id'),
                           nullable=False)
