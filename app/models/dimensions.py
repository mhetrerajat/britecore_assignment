from app import db


class DimensionAgency(db.Model):
    __tablename__ = 'dimension_agency'

    id = db.Column(db.String, primary_key=True)
    primary_agency = db.Column('primary_agency',
                               db.String,
                               db.ForeignKey('dimension_agency.id'),
                               nullable=True)
    active_producers = db.Column('active_producers', db.Integer)
    agency_app_year = db.Column('agency_appointment_year', db.Integer)
    comissions_end_year = db.Column('comissions_end_year', db.Integer)
    comissions_start_year = db.Column('comissions_start_year', db.Integer)
    max_age = db.Column('max_age', db.Integer)
    min_age = db.Column('min_age', db.Integer)
    vendor = db.Column(db.String(250))


class DimensionDate(db.Model):
    __tablename__ = "dimension_date"
    id = db.Column(db.String, primary_key=True)


class DimensionRiskState(db.Model):
    __tablename__ = "dimension_risk_state"
    id = db.Column(db.String(7), primary_key=True)


class DimensionProduct(db.Model):
    __tablename__ = "dimension_product"
    id = db.Column(db.String(25), primary_key=True)
    line = db.Column(db.String(7))
