from app import db


class DimensionAgency(db.Model):
    """Acts as a proxy for dimension_agency table in database. It stores all the information
    related to agency.
    """
    __tablename__ = 'dimension_agency'

    #: Id of an agency to uniquely identify it
    id = db.Column(db.String, primary_key=True)

    #: Number of active producers in the agency
    active_producers = db.Column('active_producers', db.Integer)

    #: Year the agency started doing business
    agency_appointment_year = db.Column('agency_appointment_year', db.Integer)

    #: Year the agency stopped using the COMMISIONS vendor
    comissions_end_year = db.Column('comissions_end_year', db.Integer)

    #: Year the agency started using the COMMISIONS vendor
    comissions_start_year = db.Column('comissions_start_year', db.Integer)

    #: Maximum age producer at that agency
    max_age = db.Column('max_age', db.Integer)

    #: Minimum age producer at that agency
    min_age = db.Column('min_age', db.Integer)

    #: The vendor that the agency subscribes to
    vendor = db.Column(db.String(250), default="Unknown")


class DimensionDate(db.Model):
    __tablename__ = "dimension_date"
    #: Year
    id = db.Column(db.String, primary_key=True)


class DimensionRiskState(db.Model):
    __tablename__ = "dimension_risk_state"
    #: Risk State
    id = db.Column(db.String(7), primary_key=True)


class DimensionProduct(db.Model):
    """Stores details about the product
    """
    __tablename__ = "dimension_product"

    #: Product Name
    id = db.Column(db.String(25), primary_key=True)

    #: Product Line
    line = db.Column(db.String(7))
