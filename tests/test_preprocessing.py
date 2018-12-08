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
    def setUp(self):
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
            'unique_id': ['id1', 'id1', 'id1', 'id1', 'id2', 'id2', 'id3']
        }
        self._df = pd.DataFrame(data)

    def test__init__(self):
        """
        Tests the constructor function
        """
        date_col = 'date'
        unique_id_col = 'unique_id'
        session_timeout = 60
        sessionise = preprocessing.Sessionise(
            self._df,
            unique_id_col,
            date_col,
            session_timeout
        )
        self.assertEqual(sessionise.unique_id_col, unique_id_col)
        self.assertEqual(sessionise.datetime_col, date_col)
        self.assertEqual(sessionise.session_timeout, session_timeout)
        # Test for incorrect datetime column name
        with self.assertRaises(TypeError):
            preprocessing.Sessionise(self._df, unique_id_col, unique_id_col)
        # Test for unique ID column name which is not in DataFrame
        with self.assertRaises(ValueError):
            preprocessing.Sessionise(self._df, 'incorrect', date_col)

    def test__add_session_boundaries(self):
        """
        Tests the `add_session_boundaries` function.
        """
        sessionise = preprocessing.Sessionise(self._df, 'unique_id', 'date')
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

    def test__get_or_create_uuid(self):
        """
        Tests `_get_or_create_uuid` function with known cases.
        """
        sessionise = preprocessing.Sessionise(self._df, 'unique_id', 'date')
        sessionise._add_session_boundaries()
        df = sessionise.df
        df.loc[:, 'session_uuid'] = df.apply(
            lambda row: sessionise._get_or_create_uuid(row), axis=1
        )
        self.assertEqual(df.loc[0, 'session_uuid'], df.loc[1, 'session_uuid'])
        self.assertNotEqual(
            df.loc[2, 'session_uuid'], df.loc[3, 'session_uuid']
        )
        self.assertNotEqual(
            df.loc[3, 'session_uuid'], df.loc[4, 'session_uuid']
        )
        self.assertEqual(df.loc[4, 'session_uuid'], df.loc[5, 'session_uuid'])
        self.assertNotEqual(
            df.loc[5, 'session_uuid'], df.loc[6, 'session_uuid']
        )

    def test__create_partitions(self):
        """
        Tests the `_create_partitions` function
        """
        sessionise = preprocessing.Sessionise(self._df, 'unique_id', 'date')
        df = sessionise.df
        _partitions = sessionise._create_partitions(4)
        partitions = [list(p) for p in _partitions]
        for partition in partitions:
            self.assertEqual(len(set(partition)), len(partition))

    def test_assign_sessions(self):
        """
        Test for `assign_sessions` function in single and multiprocessing mode
        """
        sess_single = preprocessing.Sessionise(self._df, 'unique_id', 'date')
        df_single = sess_single.assign_sessions(n_jobs=1)
        sess_parallel = preprocessing.Sessionise(self._df, 'unique_id', 'date')
        df_parallel = sess_parallel.assign_sessions(n_jobs=4)
        self.assertEqual(
            df_single['session_uuid'].nunique(),
            df_parallel['session_uuid'].nunique()
        )
