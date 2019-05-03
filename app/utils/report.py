import numpy as np
import pandas as pd
from app import db
from flask import current_app as app


class ReportGenerator(object):
    def __init__(self, request_args):
        self.request = request_args

    def generate(self):
        df = pd.read_sql_table('facts', db.engine)

        # Filter out rows based on start_date and end_date
        app.logger.info(
            "Filtering rows from facts table based on date range -> {0} - {1}".
            format(self.request.start_year, self.request.end_year))
        df = df.query(
            'date_id >= @self.request.start_year and date_id <= @self.request.end_year')

        # Filter out based on agency id
        if self.request.agency:
            app.logger.info("Filtering out rows of agency -> {0}".format(
                self.request.agency))
            df = df.query('agency_id == @self.request.agency')

        # Filters out based on product line
        if self.request.product_line or 'product_line' in self.request.group_by:
            app.logger.debug(
                "As product_line given in parameter {0}, merging product table with facts"
                .format(self.request.product_line))
            product_df = pd.read_sql_table('dimension_product', db.engine)
            df = pd.merge(df, product_df, left_on='product_id', right_on='id')

        df.fillna(value=0, inplace=True)

        # Get aggregate function
        agg_func = np.sum if self.request.aggregation == "sum" else np.mean
        aggregates = {
            field: agg_func
            for field in [
                'retention_policy_quantity', 'policy_inforce_quantity',
                'new_business_in_written_premium', 'total_written_premium',
                'earned_premium', 'incurred_losses'
            ]
        }
        aggregates.update(
            {field: np.mean
             for field in ['retention_ratio', 'loss_ratio']})

        # Calculate based on params
        field_map = {
            'year': 'date_id',
            'agency': 'agency_id',
            'product_line': 'line'
        }
        df = df.groupby(
            by=[v for k, v in field_map.items()
                if k in self.request.group_by]).agg(aggregates)

        df.reset_index(inplace=True)

        df.rename(columns={
            'loss_ratio': 'mean_loss_ratio',
            'retention_ratio': 'mean_retention_ratio'
        },
                  inplace=True)

        return df