import pandas as pd

from app import db
from app.models import (DimensionAgency, DimensionDate, DimensionProduct,
                        DimensionRiskState)


class DataParser(object):
    def __init__(self, path, sample_size=1, query=None, **kwargs):
        self.path = path
        self.sample_size = sample_size
        self.query = query or {}

        # Initialize data frame
        self.df = self._init_df(path)

    def _init_df(self, path):
        df = pd.read_csv(path, dtype={'AGENCY_ID': str})
        df.replace({key: None for key in [99999, '99999']}, inplace=True)

        # Filter out rows based on query parameter
        if self.query:
            for key, value in self.query.items():
                df = df.query("{0} == @value".format(key))

        # Take sample of data randomly
        if self.sample_size != 1:
            df = df.sample(frac=self.sample_size)
        return df

    def _bulk_write(self, df, model_class):
        def insert(data):
            conn = db.engine.connect()
            # TODO: This sytanx is specific to sqlite
            conn.execute(
                model_class.__table__.insert().prefix_with("OR REPLACE"), data)

        data = []
        BATCH_SIZE = 1000
        CURSOR = 0
        for _, row in df.iterrows():
            data.append(dict(row))
            CURSOR += 1

            if CURSOR % BATCH_SIZE == 0 and CURSOR != 0 and data:
                insert(data)
                data = []
                CURSOR = 0

        if data:
            insert(data)

    def _transform_agency(self):
        df = self.df[[
            'AGENCY_ID', 'AGENCY_APPOINTMENT_YEAR', 'ACTIVE_PRODUCERS',
            'MAX_AGE', 'MIN_AGE', 'VENDOR', 'COMMISIONS_START_YEAR',
            'COMMISIONS_END_YEAR'
        ]]
        df = df.rename(
            columns={
                'AGENCY_ID': 'id',
                'AGENCY_APPOINTMENT_YEAR': 'agency_appointment_year',
                'ACTIVE_PRODUCERS': 'active_producers',
                'MAX_AGE': 'max_age',
                'MIN_AGE': 'min_age',
                'VENDOR': 'vendor',
                'COMMISIONS_START_YEAR': 'comissions_start_year',
                'COMMISIONS_END_YEAR': 'comissions_end_year'
            })
        df = df.drop_duplicates(subset=['id'])
        self._bulk_write(df, DimensionAgency)

    def _transform_date(self):
        df = self.df[['STAT_PROFILE_DATE_YEAR']]
        df = df.rename(columns={'STAT_PROFILE_DATE_YEAR': 'id'})
        df = df.drop_duplicates(subset=['id'])
        self._bulk_write(df, DimensionDate)

    def _transform_product(self):
        df = self.df[['PROD_LINE', 'PROD_ABBR']]
        df = df.rename(columns={'PROD_LINE': 'line', 'PROD_ABBR': 'id'})
        df = df.drop_duplicates(subset=['id'])
        self._bulk_write(df, DimensionProduct)

    def _transform_risk_state(self):
        df = self.df[['STATE_ABBR']]
        df = df.rename(columns={'STATE_ABBR': 'id'})
        df = df.drop_duplicates(subset=['id'])
        self._bulk_write(df, DimensionRiskState)

    def parse(self):
        self._transform_agency()
        self._transform_date()
        self._transform_product()
        self._transform_risk_state()
