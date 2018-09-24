import pytest
from markovclick.models import MarkovClickstream
from markovclick.dummy import genRandClickstreamList
from unittest import mock
import numpy as np
from tqdm import tqdm

@pytest.fixture(scope="function")
def random_clickstream():
    """
    Create a random clickstream for testing
    """

    return genRandClickstreamList(100, 12)


@pytest.fixture(scope='function')
def markov_clickstream(random_clickstream):
    """
    Create MarkovClickstream object for testing.
    """
    
    markovchain = MarkovClickstream(random_clickstream)
    return markovchain


def test_row_prob(markov_clickstream):
    """
    Test each row in the probability matrix for the Markov
    chain adds up to 1.
    """

    probMatrix = markov_clickstream.probMatrix
    rows = range(0, probMatrix.shape[0])
    for row in rows:
        rowSum = round(np.sum(probMatrix[row, :]), 3)
        assert 0.999 <= rowSum <= 1.000


def test_prob_after_n_trans(markov_clickstream):
    """
    Tests the probability of each row sums to 1, after N
    number of transitions.
    
    Sum of reach row is validated to equal 1, after calculating
    multiple dot products of each probability matrix.   
    """

    probMatrix = markov_clickstream.probMatrix
    _probMatrixAfterT = probMatrix
    for n in tqdm(range(0, 100)):
        _probMatrixAfterT = np.dot(_probMatrixAfterT, probMatrix)
        rows = range(0, _probMatrixAfterT.shape[0])

        for row in rows:
            rowSum = round(np.sum(_probMatrixAfterT[row, :]), 3)
            assert 0.999 <= rowSum <= 1.000

