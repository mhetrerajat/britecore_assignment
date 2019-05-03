import pandas as pd
from sqlalchemy.orm import sessionmaker

from app import db
from app.models import DimensionAgency


class DataParser(object):
    def __init__(self, path, sample_size=1, query=None, **kwargs):
        self.path = path
        self.sample_size = sample_size
        self.query = query or {}

        # Initialize data frame
        self.df = self._init_df(path)

    def _init_df(self, path):
        df = pd.read_csv(path)
        df = df.replace(to_replace=['99999', 99999], value=None)

        # Filter out rows based on query parameter
        if self.query:
            for key, value in self.query.items():
                df = df.query("{0} == @value".format(key))

        # Take sample of data randomly
        if self.sample_size != 1:
            df = df.sample(frac=self.sample_size)
        return df

    def _bulk_write(self, df, model_class):
        Session = sessionmaker(bind=db.engine)

        def insert(data):
            session = Session()
            session.bulk_save_objects(data, return_defaults=True)
            session.commit()
            session.close()

        data = []
        BATCH_SIZE = 1000
        CURSOR = 0
        for _, row in df.iterrows():
            data.append(model_class(**row))
            CURSOR += 1

            if CURSOR % BATCH_SIZE == 0 and CURSOR != 0 and data:
                insert(data)
                data = []
                CURSOR = 0

        if data:
            insert(data)

    def _process_agency(self):
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
        df = df.astype({
            'id': str,
        })
        df = df.drop_duplicates(subset=['id'])
        self._bulk_write(df, DimensionAgency)

    def parse(self):
        self._process_agency()
