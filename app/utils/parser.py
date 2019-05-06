import numpy as np
import pandas as pd
from flask import current_app as app

from app import db
from app.models import (DimensionAgency, DimensionDate, DimensionProduct,
                        DimensionRiskState, Facts)


class DataParser(object):
    """This class implements CSV data parser. It first cleans the data and then extract
    information from file. The extracted information is then transformed into various 
    entities to load it into database by performing certain checks and validations
    
    :param path: Path of the csv file
    :type path: str
    :param sample_size: The ratio of rows to be choosen from actual file. 
    Default value is 1 i.e it loads entire data of file
    :type sample_size: float
    :param query: Query to filter out data from file.
    :type query: dict
    """

    def __init__(self, path, sample_size=1, query=None, **kwargs):
        self.path = path
        self.sample_size = sample_size
        self.query = query or {}

        # Initialize data frame
        self.df = self._init_df(path)

    def _init_df(self, path):
        app.logger.debug("Extracting file : {0}".format(path))
        df = pd.read_csv(path, dtype={'AGENCY_ID': str})
        df.replace({key: None for key in [99999, '99999']}, inplace=True)

        # Filter out rows based on query parameter
        if self.query:
            for key, value in self.query.items():
                df = df.query("{0} == @value".format(key))

            app.logger.debug("Rows post filter -> {0} rows".format(
                df.shape[0]))

        # Take sample of data randomly
        if self.sample_size != 1:
            df = df.sample(frac=self.sample_size)
            app.logger.debug(
                "Randomly choose sample from actual data -> {0} rows".format(
                    df.shape[0]))
        return df

    def _bulk_write(self, df, model_class):
        """This method loads data into database in chunks of size 1000
        
        :param df: Dataframe containing transformed data
        :type df: pd.DataFrame
        :param model_class: Model of the table in which this data is to load
        :type model_class: db.Model
        """

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

        app.logger.debug("Number of rows inserted : {0}".format(df.shape[0]))

    def _transform_agency(self):
        """Transform the data from file to store agency specific informatiom in dimension_agency table
        """
        app.logger.debug("Processing data for agency data")
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
        """Transform the data from file to store date specific informatiom in dimension_date table
        """
        app.logger.debug("Processing data for date data")
        df = self.df[['STAT_PROFILE_DATE_YEAR']]
        df = df.rename(columns={'STAT_PROFILE_DATE_YEAR': 'id'})
        df = df.drop_duplicates(subset=['id'])
        self._bulk_write(df, DimensionDate)

    def _transform_product(self):
        """Transform the data from file to store product specific informatiom in dimension_product table
        """
        app.logger.debug("Processing data for product data")
        df = self.df[['PROD_LINE', 'PROD_ABBR']]
        df = df.rename(columns={'PROD_LINE': 'line', 'PROD_ABBR': 'id'})
        df = df.drop_duplicates(subset=['id'])
        self._bulk_write(df, DimensionProduct)

    def _transform_risk_state(self):
        """Transform the data from file to store risk state specific informatiom table
        """
        app.logger.debug("Processing data for risk state data")
        df = self.df[['STATE_ABBR']]
        df = df.rename(columns={'STATE_ABBR': 'id'})
        df = df.drop_duplicates(subset=['id'])
        self._bulk_write(df, DimensionRiskState)

    def _transform_summary(self):
        """Transform the data from file to store in facts table
        """
        app.logger.debug("Processing to get summarized data")
        bound_q = [
            'CL_BOUND_CT_MDS', 'CL_BOUND_CT_SBZ', 'CL_BOUND_CT_eQT',
            'PL_BOUND_CT_ELINKS', 'PL_BOUND_CT_PLRANK', 'PL_BOUND_CT_eQTte',
            'PL_BOUND_CT_APPLIED', 'PL_BOUND_CT_TRANSACTNOW'
        ]
        total_q = [
            'CL_QUO_CT_MDS', 'CL_QUO_CT_SBZ', 'CL_QUO_CT_eQT',
            'PL_QUO_CT_ELINKS', 'PL_QUO_CT_PLRANK', 'PL_QUO_CT_eQTte',
            'PL_QUO_CT_APPLIED', 'PL_QUO_CT_TRANSACTNOW'
        ]

        df = self.df

        df['bound_quotes'] = df[bound_q].sum(axis=1)
        df['total_quotes'] = df[total_q].sum(axis=1)

        df = df[[
            'RETENTION_POLY_QTY', 'POLY_INFORCE_QTY', 'PREV_POLY_INFORCE_QTY',
            'NB_WRTN_PREM_AMT', 'WRTN_PREM_AMT', 'PREV_WRTN_PREM_AMT',
            'PRD_ERND_PREM_AMT', 'PRD_INCRD_LOSSES_AMT', 'RETENTION_RATIO',
            'LOSS_RATIO', 'LOSS_RATIO_3YR', 'GROWTH_RATE_3YR', 'AGENCY_ID',
            'STAT_PROFILE_DATE_YEAR', 'PROD_ABBR', 'STATE_ABBR',
            'bound_quotes', 'total_quotes'
        ]]

        df = df.rename(
            columns={
                'AGENCY_ID': 'agency_id',
                'STAT_PROFILE_DATE_YEAR': 'date_id',
                'PROD_ABBR': 'product_id',
                'STATE_ABBR': 'risk_state_id',
                'RETENTION_POLY_QTY': 'retention_policy_quantity',
                'POLY_INFORCE_QTY': 'policy_inforce_quantity',
                'PREV_POLY_INFORCE_QTY': 'prev_policy_inforce_quantity',
                'NB_WRTN_PREM_AMT': 'new_business_in_written_premium',
                'WRTN_PREM_AMT': 'total_written_premium',
                'PREV_WRTN_PREM_AMT': 'prev_wrtitten_premium',
                'PRD_ERND_PREM_AMT': 'earned_premium',
                'PRD_INCRD_LOSSES_AMT': 'incurred_losses',
                'RETENTION_RATIO': 'retention_ratio',
                'LOSS_RATIO': 'loss_ratio',
                'LOSS_RATIO_3YR': 'loss_ratio_3_year',
                'GROWTH_RATE_3YR': 'growth_rate_3_years',
            })

        df = df.astype({
            column: str if column in [
                'agency_id', 'date_id', 'product_id', 'risk_state_id'
            ] else np.float64
            for column in df.columns
        })

        # Validate index fields
        df['is_valid'] = df.apply(lambda x: all([
            x[field] for field in
            ['agency_id', 'date_id', 'product_id', 'risk_state_id']
        ]),
                                  axis=1)

        app.logger.debug("Invalid rows from csv for facts table : {0}".format(
            df.query('is_valid == False').shape[0]))

        summary = df.pivot_table(
            index=['agency_id', 'date_id', 'product_id', 'risk_state_id'],
            aggfunc={
                'bound_quotes': 'sum',
                'earned_premium': 'sum',
                'growth_rate_3_years': 'sum',
                'incurred_losses': 'sum',
                'loss_ratio': 'mean',
                'loss_ratio_3_year': 'mean',
                'new_business_in_written_premium': 'sum',
                'policy_inforce_quantity': 'sum',
                'prev_policy_inforce_quantity': 'sum',
                'prev_wrtitten_premium': 'sum',
                'retention_policy_quantity': 'sum',
                'retention_ratio': 'mean',
                'total_quotes': 'sum',
                'total_written_premium': 'sum'
            })
        summary.reset_index(inplace=True)
        self._bulk_write(summary, Facts)

    def parse(self):
        """This method underneath calls all transformations that to be run on data
        """
        self._transform_agency()
        self._transform_date()
        self._transform_product()
        self._transform_risk_state()

        self._transform_summary()
