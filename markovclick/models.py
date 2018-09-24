import numpy as np
import random
from tqdm import tqdm
import pandas as pd
from itertools import product, chain


class MarkovClickstream:
    """
    Builds a Markov chain from input clickstreams.

    Args:
        clickstream_list (list): List of clickstream data. Each page should be
            encoded as a string, prefixed by a letter e.g. 'P1'
    """

    def __init__(self, clickstream_list: list=None):
        self.clickstream_list = clickstream_list
        self.pages = []
        self.getUniquePages()

        self.countMatrix = np.zeros([
            len(self.pages),
            len(self.pages)
        ])
        self.probMatrix = None

        self.populateCountMatrix()
        self.computeProbabilityMatrix()

    def getUniquePages(self):
        """
        Retrieves all the unique pages within the provided list of
        clickstreams.
        """

        allPages = chain.from_iterable(self.clickstream_list)
        self.pages = sorted(list(set(allPages)), key=lambda x: int(x[1:]))

        return self.pages

    def populateCountMatrix(self):
        """
        Assembles a matrix of counts of transitions from each possible state,
        to every other possible state.
        """
        
        # For each session in list of sessions
        for session in self.clickstream_list:
            for j in range(0, len(session) - 1):
                nextState = self.pages.index(session[j+1])
                currentState = self.pages.index(session[j])

                self.countMatrix[currentState, nextState] += 1

        return self.countMatrix

    def normaliseRow(self, row):
        """
        Normalises each row in count matrix, to produce a probability.
        
        To be used when iterating over rows of `self.countMatrix`. Sum of each
        row adds up to 1.
        
        Args:
            row : Each row within numpy matrix to act upon.

        Returns:

        """

        sumOfEachRow = np.sum(row)
        return np.nan_to_num(row / sumOfEachRow)

    def computeProbabilityMatrix(self):
        """
        Computes the probability matrix for the input clickstream.
        
        """

        self.probMatrix = np.apply_along_axis(self.normaliseRow, 1,
                                              self.countMatrix)

    def calcProbToPage(self, clickstream: list, verbose=True):
        """
        Calculates the probability for a sequence of clicks (clickstream)
        taking place.
                
        Args:
            clickstream (list): Sequence of clicks (pages), for which to
                calculate the probability of occuring.
            verbose (bool, optional): Defaults to True. Specifies whether the
                output is printed to the terminal, or simply provided back.
        """

        totalProb = 1

        currPage = self.pages.index(clickstream[0])

        for i in range(0, len(clickstream) - 1):
            nextPage = self.pages.index(clickstream[i + 1])
            totalProb = totalProb * self.probMatrix[currPage, nextPage]

            currPage = nextPage
        
        if verbose:
            print("Probability for clickstream: \n {} \nis{}".format(
                ':'.join(clickstream), totalProb
            ))
        
        return totalProb

    def permutations(self, iterable, r=None):
        """
            Modification of `itertools.permutations()` function to yield a 
            mutable list rather than an immutable tuple. 

            Unlike the Cartesian product, this does not return a sequence
            with repetitions in it.
        """
        pool = tuple(iterable)
        n = len(pool)
        r = n if r is None else r
        for indices in product(range(n), repeat=r):
            if len(set(indices)) == r:
                yield [pool[i] for i in indices]

    def cartesianProduct(self, iterable, repeats=1):
        """
            Modifies Python's `itertools.product()` function
            to return a list of lists, rather than list of
            tuples.

            Args:
                iterable (list): List of iterables to assemble
                    Cartesian product from
                repeats (int): Number of elements in each list of
                    the Cartesian product

            Returns:
                List of lists of Cartesian product
        """

        return list(list(p) for p in product(iterable, repeat=repeats))

    def calcProbForAllRoutesTo(self, clickstream: list, end_page: str,
                               clicks: int, cartesianProduct=True):
        """
            Calculates the probability given an input sequence of page clicks, 
            to reach the specified end state with the specified number of
            transitions before the end state.

            Args:
                clickstream (list): List (sequence) of states
                end_state (str): Desired end to state to calculate
                    probability towards
                transitions (int): Number of transitions to make after input
                    sequence, before reaching end state.

            Returns:
                float: Probability
        """

        if cartesianProduct:
            potentialRoutes = list(self.cartesianProduct(self.pages, 
                                                         repeats=clicks))
        else:
            potentialRoutes = list(self.permutations(self.pages, r=clicks))

        potentialRouteProbs = []

        for i, route in tqdm(enumerate(potentialRoutes)):
            for state in clickstream[::-1]:
                route.insert(0, state)
            route.append(end_page)

            prob = self.calcProbToPage(route, verbose=False)
            potentialRouteProbs.append(prob)

        return potentialRoutes, potentialRouteProbs
