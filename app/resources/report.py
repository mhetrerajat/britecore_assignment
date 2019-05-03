import pandas as pd
from flask import current_app as app
from flask.json import jsonify
from flask_restful import Resource, marshal, reqparse

from app import db
import numpy as np

from app.utils.schema import ReportSchema


class ReportResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('group_by',
                                   type=str,
                                   action='append',
                                   choices=('year', 'agency', 'product_line'),
                                   required=True)
        self.reqparse.add_argument('start_year', type=str, required=True)
        self.reqparse.add_argument('end_year', type=str, required=True)
        self.reqparse.add_argument('aggregation',
                                   type=str,
                                   required=False,
                                   default='sum',
                                   choices=('mean', 'sum'))
        self.reqparse.add_argument('agency', type=str, required=False)
        self.reqparse.add_argument('product_line', type=str, required=False)
        super(ReportResource, self).__init__()

    def get(self):
        """
            Generate CSV report with premium information
        """
        args = self.reqparse.parse_args()

        df = pd.read_sql_table('facts', db.engine)

        # Filter out rows based on start_date and end_date
        app.logger.info(
            "Filtering rows from facts table based on date range -> {0} - {1}".
            format(args.start_year, args.end_year))
        df = df.query(
            'date_id >= @args.start_year and date_id <= @args.end_year')

        # Filter out based on agency id
        if args.agency:
            app.logger.info("Filtering out rows of agency -> {0}".format(
                args.agency))
            df = df.query('agency_id == @args.agency')

        # Filters out based on product line
        if args.product_line or 'product_line' in args.group_by:
            app.logger.debug(
                "As product_line given in parameter {0}, merging product table with facts"
                .format(args.product_line))
            product_df = pd.read_sql_table('dimension_product', db.engine)
            df = pd.merge(df, product_df, left_on='product_id', right_on='id')

        df.fillna(value=0, inplace=True)

        # Get aggregate function
        agg_func = np.sum if args.aggregation == "sum" else np.mean
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
                if k in args.group_by]).agg(aggregates)

        df.reset_index(inplace=True)

        df.rename(columns={
            'loss_ratio': 'mean_loss_ratio',
            'retention_ratio': 'mean_retention_ratio'
        },
                  inplace=True)

        response = {
            'data': marshal(df.to_dict('records'), ReportSchema),
            'status': 'success',
            'message': None
        }
        return jsonify(response)
