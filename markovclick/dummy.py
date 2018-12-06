"""
Functions for generating dummy content.
"""

import random


def gen_random_clickstream(n_of_streams: int, n_of_pages: int,
                           length: tuple = (8, 12)) -> list:
    """
    Generates a list of random clickstreams, to use in absence of real
    data.

    Args:
        n_of_streams (int): Number of unique clickstreams to generate
        n_of_pages (int): Number of unique pages, from which to use to
            generate clickstreams.
        length (tuple): Range of length for each clickstream.
    Returns:
        list: List of clickstreams, to use as dummy data.
    """

    clickstream_list = []

    def page(x):
        return random.randrange(0, x)

    for _ in range(n_of_streams):
        _length = random.randrange(length[0], length[1])

        clickstream = ['P{}'.format(page(n_of_pages)) for x in range(_length)]
        clickstream_list.append(clickstream)

    return clickstream_list
