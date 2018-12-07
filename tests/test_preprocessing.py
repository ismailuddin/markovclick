"""
Module to test markovclick.preprocessing functions
"""


import unittest

import pandas as pd
from datetime import datetime
import uuid
from markovclick import preprocessing


class TestSessionise(unittest.TestCase):
    """
    Class to test preprocessing.Sessionise class
    """

    def test__init__(self):
        date_col = 'date'
        unique_id_col = 'unique_id'
        session_timeout = 60
        data = {
            date_col: [datetime(2018, 1, 1), datetime(2018, 1, 2)],
            unique_id_col: [str(uuid.uuid4()), str(uuid.uuid4())]
        }
        df = pd.DataFrame(data)
        sessionise = preprocessing.Sessionise(
            df,
            unique_id_col,
            date_col,
            session_timeout
        )
        self.assertEqual(sessionise.unique_id_col, unique_id_col)
        self.assertEqual(sessionise.datetime_col, date_col)
        self.assertEqual(sessionise.session_timeout, session_timeout)
        # Test for incorrect datetime column name
        with self.assertRaises(TypeError):
            preprocessing.Sessionise(df, unique_id_col, unique_id_col)
        # Test for unique ID column name which is not in DataFrame
        with self.assertRaises(ValueError):
            preprocessing.Sessionise(df, 'incorrect', date_col)

    def test_add_session_boundaries(self):
        data = {
            'date': [
                datetime(2018, 1, 1, 10, 10),
                datetime(2018, 1, 1, 10, 15),
                datetime(2018, 1, 1, 10, 25),
                datetime(2018, 1, 1, 10, 57),
                datetime(2018, 1, 1, 11, 2),
                datetime(2018, 1, 1, 11, 15),
                datetime(2018, 1, 1, 11, 55),
            ],
            'uniq_id': ['id1', 'id1', 'id1', 'id1', 'id2', 'id2', 'id3']
        }
        _df = pd.DataFrame(data)
        sessionise = preprocessing.Sessionise(_df, 'uniq_id', 'date')
        df = sessionise.df
        sessionise._add_session_boundaries()  # pylint: disable=W0212
        columns = sessionise.df.columns
        self.assertTrue('prev_uniq_id' in columns)
        self.assertTrue('session_boundary' in columns)
        self.assertTrue('time_diff' in columns)
        self.assertEqual(
            df[df['session_boundary'] == True].sum()['session_boundary'],
            2
        )
