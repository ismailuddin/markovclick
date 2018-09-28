import random

"""
Functions for generating dummy content.
"""


def genRandClickstreamList(nOfStreams: int, nOfPages: int, length: list=[8, 12]) -> list:
    """
    Generates a list of random clickstreams, to use in absence of real
    data.
            
    Args:
        nOfStreams (int): Number of unique clickstreams to generate
        nOfPages (int): Number of unique pages, from which to use to 
            generate clickstreams.
        length (list): Range of length for each clickstream.
    Returns:
        list: List of clickstreams, to use as dummy data.
    """

    clickstreamList = []

    def page(x):
        return random.randrange(0, x)

    for _ in range(nOfStreams):
        _length = random.randrange(length[0], length[1]) 
        
        clickstream = ['P{}'.format(page(nOfPages)) for x in range(_length)]
        clickstreamList.append(clickstream)

    return clickstreamList
