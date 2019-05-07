import os

import pandas as pd

from app.utils.parser import DataParser
from config import BASE_DIR
from tests.base import BaseTestCase


class ParserTestCase(BaseTestCase):
    PATH = os.path.join(BASE_DIR, 'sample_data.csv')

    def test_uneven_number_of_rows(self):
        p = DataParser(ParserTestCase.PATH, sample_size=0.2)
        p.parse()

        self.assertIsInstance(p.df, pd.DataFrame)
        self.assertGreater(p.df.shape[0], 0)
