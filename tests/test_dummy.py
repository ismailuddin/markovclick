"""
Module to test markovclick.dummy functions
"""


import unittest

from markovclick.dummy import gen_random_clickstream
from markovclick.utils.helpers import flatten_list


class TestDummy(unittest.TestCase):
    """
    Class to test functions in markovclick.dummy
    """

    def test_gen_random_clickstream(self):
        """
        Tests `gen_random_clickstream` function to ensure it generates
        clickstreams with the attributes equal to what is specified in the
        arguments.
        """
        n_of_streams = 12
        n_of_pages = 14
        length = (15, 20)
        clickstream = gen_random_clickstream(n_of_streams, n_of_pages,
                                             length)
        self.assertEqual(len(clickstream), n_of_streams)
        self.assertEqual(len(set(flatten_list(clickstream))), n_of_pages)
        lengths = [len(stream) for stream in clickstream]
        self.assertGreaterEqual(min(lengths), length[0])
        self.assertLess(min(lengths), length[1])
        self.assertGreater(max(lengths), length[0])
        self.assertLessEqual(max(lengths), length[1])
