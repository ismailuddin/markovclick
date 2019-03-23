"""
Module to run tests for the markovclick/models.py file
"""


import unittest
import numpy as np
from markovclick.models import MarkovClickstream
from markovclick.dummy import gen_random_clickstream
from markovclick.utils.helpers import flatten_list


class TestModels(unittest.TestCase):
    """
    Class to test models.py
    """

    def test_get_unique_pages(self):
        """
        Tests the `get_unique_pages` function
        """
        clickstream = gen_random_clickstream(n_of_streams=100, n_of_pages=12)
        markov_clickstream = MarkovClickstream(
            clickstream_list=clickstream
        )
        pages = markov_clickstream.get_unique_pages()
        self.assertEqual(len(pages), len(set(pages)))
        clickstream_pages = flatten_list(clickstream)
        self.assertEqual(set(pages), set(clickstream_pages))

    def test_initialise_count_matrix(self):
        """
        Test `initialise_count_matrix` function
        """
        clickstream = gen_random_clickstream(n_of_streams=100, n_of_pages=12)
        markov_clickstream = MarkovClickstream(
            clickstream_list=clickstream
        )
        markov_clickstream.initialise_count_matrix()
        count_matrix = markov_clickstream.count_matrix
        pages = set(flatten_list(clickstream))
        expected = np.zeros((len(pages), len(pages)))
        self.assertTrue((count_matrix == expected).all())

    def test_populate_count_matrix(self):
        """
        Tests the `populate_count_matrix` function
        """
        clickstream = [
            ['P1', 'P2', 'P2', 'P2'],
            ['P3', 'P4', 'P5']
        ]
        markov_clickstream = MarkovClickstream(
            clickstream_list=clickstream
        )

        markov_clickstream.populate_count_matrix()
        expected_count_matrix = np.array([
            [0., 1., 0., 0., 0.],
            [0., 2., 0., 0., 0.],
            [0., 0., 0., 1., 0.],
            [0., 0., 0., 0., 1.],
            [0., 0., 0., 0., 0.]
        ])

        self.assertTrue(
            (expected_count_matrix == markov_clickstream.count_matrix).all()
        )

    def test_normalise_row(self):
        """
        Tests `normalise_row` function
        """
        test_cases = [
            (np.array([5.0, 0.0]), np.array([1.0, 0.0])),
            (np.array([0.0, 0.0]), np.array([0.0, 0.0])),
        ]
        for row, expected in test_cases:
            normalised = MarkovClickstream.normalise_row(row)
            print(row, expected, normalised)
            self.assertTrue((normalised == expected).all())

    def test_compute_prob_matrix(self):
        """
        Test `compute_prob_matrix` function
        """
        clickstream = gen_random_clickstream(n_of_streams=100, n_of_pages=12)
        markov_clickstream = MarkovClickstream(
            clickstream_list=clickstream
        )
        markov_clickstream.compute_prob_matrix()
        prob_matrix = markov_clickstream.prob_matrix
        for row in range(prob_matrix.shape[0]):
            self.assertAlmostEqual(np.sum(prob_matrix[row, :]), 1)
