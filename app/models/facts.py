from app import db


class Facts(db.Model):
    """This class act as a proxy with facts table in database.
    """
    __tablename__ = "facts"

    #: Unique id of the row/entry. Uniqueness of the row is based on agency, date, product and risk state.
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    #: Current number of policies that are still active from previous year
    retention_policy_quantity = db.Column('retention_policy_quantity',
                                          db.Integer)

    #: Number of policies active for that year
    policy_inforce_quantity = db.Column('policy_inforce_quantity', db.Integer)

    #: Number of policies active in the previous year
    prev_policy_inforce_quantity = db.Column('prev_policy_inforce_quantity',
                                             db.Integer)

    #: New business in written premium
    new_business_in_written_premium = db.Column(
        'new_business_in_written_premium', db.Float)

    #: Total written premium
    total_written_premium = db.Column('total_written_premium', db.Float)

    #: Earned Premium
    earned_premium = db.Column('earned_premium', db.Float)

    #: Losses
    incurred_losses = db.Column('incurred_losses', db.Float)

    #: Retention for that agency writing that particular product in that particular state from the previous year
    retention_ratio = db.Column('retention_ratio', db.Float)

    #: Loss Ratio
    loss_ratio = db.Column('loss_ratio', db.Float)

    #: Computed by agency by line of business by year for the three year period ending in that year
    loss_ratio_3_year = db.Column('loss_ratio_3_year', db.Float)

    #: Measures average growth in written premium for that agency in that line of business
    growth_rate_3_years = db.Column('growth_rate_3_years', db.Float)

    #: Bound Quotes
    bound_quotes = db.Column('bound_quotes', db.Integer)

    #: Total Quotes
    total_quotes = db.Column('total_quotes', db.Integer)

    #: Year
    date_id = db.Column('date_id',
                        db.String,
                        db.ForeignKey('dimension_date.id'),
                        nullable=False)

    #: Unique id of the agency
    agency_id = db.Column('agency_id',
                          db.String,
                          db.ForeignKey('dimension_agency.id'),
                          nullable=False)

    #: Risk State
    risk_id = db.Column('risk_state_id',
                        db.String,
                        db.ForeignKey('dimension_risk_state.id'),
                        nullable=False)

    #: Product
    product_id = db.Column('product_id',
                           db.String,
                           db.ForeignKey('dimension_product.id'),
                           nullable=False)
