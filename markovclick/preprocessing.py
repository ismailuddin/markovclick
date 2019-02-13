"""
Functions for preprocessing clickstream datasets
"""

from uuid import uuid4
from multiprocessing import Process, Queue
from datetime import timedelta
import numpy as np
import pandas as pd


class Sessionise:
    """
    Class with functions to sessionise a pandas DataFrame containing
    clickstream data.
    """

    def __init__(self, df, unique_id_col: str, datetime_col: str,
                 session_timeout: int = 30) -> None:
        """
        Instantiates object of ``Sessionise`` class.
        
        
        
        Args:
            df (pd.DataFrame): ``pandas`` DataFrame object containing
                clickstream data. Must contain atleast a timestamp column,
                unique identifier column such as cookie ID.
            unique_id_col (str): Column name of unique identifier, e.g.
                ``cookie_id``
            datetime_col (str): Column name of timestamp column.
            session_timeout (int, optional): Defaults to 30. Maximum time in
                minutes after which a session is broken.
        """
        self._df = df
        self.unique_id_col = unique_id_col
        self.datetime_col = datetime_col
        self._session_timeout = session_timeout
        self.curr_uniq_id = str(uuid4())
        self.columns = [self.unique_id_col, 'prev_uniq_id', 'session_boundary']

    @property
    def df(self):
        """
        Provides access to ``df`` attribute
        """
        return self._df

    @property
    def unique_id_col(self):
        """
        Provides access to ``unique_id_col`` attribute
        """
        return self.__unique_id_col

    @unique_id_col.setter
    def unique_id_col(self, name: str):
        """
        Sets value for ``unique_id_col`` attribute
        """
        if name not in self.df.columns:
            raise ValueError("Unique ID column name not in dataframe.")
        elif isinstance(name, str):
            self.__unique_id_col = name
        else:
            raise ValueError("Unique ID column name should be string.")

    @property
    def datetime_col(self):
        """
        Provides access to ``datetime_col`` attribute
        """
        return self.__datetime_col

    @datetime_col.setter
    def datetime_col(self, name: str):
        """
        Sets value for ``datetime_col`` attribute
        """
        if isinstance(name, str) and np.issubdtype(
                self.df[name], np.datetime64
        ):
            self.__datetime_col = name
        else:
            raise TypeError("Datetime column name should be string referring\
                              to a datetime column.")

    @property
    def session_timeout(self):
        """
        Provides access to ``session_timeout`` attribute
        """
        return self._session_timeout

    def _add_session_boundaries(self):
        """
        Adds a column to denote the session boundaries in clickstream data
        """
        self._df.sort_values(by=[self.unique_id_col, self.datetime_col])
        self._df['prev_uniq_id'] = self._df.shift(1)[self.unique_id_col]
        self._df['time_diff'] = self._df[self.datetime_col].diff(1)
        self._df['time_diff'] = self._df['time_diff'].fillna(timedelta(0))

        self._df['session_boundary'] = self._df['time_diff'] - timedelta(
            minutes=self.session_timeout
        )
        self._df.loc[:, 'session_boundary'] = self._df[
            'session_boundary'
        ].apply(
            lambda row: True if row > timedelta(0) else False
        )

    def _get_or_create_uuid(self, row) -> str:
        """
        Provides a new or returns previous session UUID depending on criteria
        for setting a new session boundary.

        Args:
            row: Row in DataFrame of clickstream dataset

        Returns:
            str: Unique session UUID
        """
        curr_uniq_id = row[self.unique_id_col]
        prev_anon_id = row['prev_uniq_id']
        boundary = row['session_boundary']

        if boundary is True or curr_uniq_id != prev_anon_id:
            self.curr_uniq_id = str(uuid4())
            return self.curr_uniq_id
        else:
            return self.curr_uniq_id

    def _create_partitions(self, partitions: int) -> list:
        """
        Splits clickstream dataset into specified number of partitions, based
        on the unique IDs (e.g. cookie ID) in the DataFrame.

        Args:
            partitions (int): Number of partitions to split into

        Returns:
            list: List of DataFrames partitioned
        """
        uniq_ids = self.df[self.unique_id_col].unique()
        partitions = list(
            filter(lambda x: x.size > 0, np.array_split(uniq_ids, partitions))
        )
        return partitions

    def _assign_sessions_parallel(self, df, partition: list, queue):
        """
        Assigns sessions to partition of DataFrame, created using list of
        unique IDs provided in partition argument.

        Args:
            df (pd.DataFrame): DataFrame containing clickstream data
            partition (list): List of unique IDs to subset DataFrame
            queue: multiprocessing.Queue object to add results to
        """
        _df = df.loc[df[self.unique_id_col].isin(partition), :]
        curr_session_uuid = str(uuid4())

        def get_or_create_uuid(row) -> str:
            nonlocal curr_session_uuid
            curr_uniq_id = row[self.unique_id_col]
            prev_anon_id = row['prev_uniq_id']
            boundary = row['session_boundary']

            if boundary is True or curr_uniq_id != prev_anon_id:
                curr_session_uuid = str(uuid4())
                return curr_session_uuid
            else:
                return curr_session_uuid

        _df.loc[:, 'session_uuid'] = _df.apply(
            lambda row: get_or_create_uuid(row), axis=1
        )
        queue.put(_df)

    def assign_sessions(self, n_jobs: int = 1):
        """
        Assigns unique session IDs to individual clicks that form the
        sessions. Supports parallel processing through setting ``n_jobs`` to
        higher than 1.

        Args:
            n_jobs (int, optional): Defaults to 1. If 2 or higher, enables
                parallel processing.

        Returns:
            pd.DataFrame: Returns sessionised DataFrame, with session IDs 
            stored in ``session_UUID`` column.
        """
        self._add_session_boundaries()
        if n_jobs == 1:
            self._df.loc[:, 'session_uuid'] = self.df[self.columns].apply(
                lambda row: self._get_or_create_uuid(row), axis=1
            )
            return self.df
        if n_jobs > 1:
            partitions = self._create_partitions(n_jobs)
            queue = Queue()
            processes = []
            for partition in partitions:
                processes.append(Process(
                    target=self._assign_sessions_parallel,
                    args=(self.df, partition, queue)
                ))
            for process in processes:
                process.start()
            results = [queue.get() for process in processes]
            for process in processes:
                process.join()

            self._df = pd.concat(results, axis=0)
            self._df = self._df.sort_index()
            return self.df
