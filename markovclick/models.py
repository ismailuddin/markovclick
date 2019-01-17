"""
Models module which holds MarkovClickstream model.
"""


from itertools import product, chain
from tqdm import tqdm
import numpy as np


class MarkovClickstream:
    """
    Builds a Markov chain from input clickstreams.

    Args:
        clickstream_list (list): List of clickstream data. Each page should be
            encoded as a string, prefixed by a letter e.g. 'P1'
    """

    def __init__(self, clickstream_list: list = None, prefixed=True):
        self.clickstream_list = clickstream_list
        self.pages = []
        self.get_unique_pages(prefixed=prefixed)

        self._count_matrix = None
        self.initialise_count_matrix()
        self._prob_matrix = None

        self.populate_count_matrix()
        self.compute_prob_matrix()

    @property
    def count_matrix(self):
        """
        Sets attribute to access the count matrix
        """
        return self._count_matrix

    @property
    def prob_matrix(self):
        """
        Sets attribute to access the probability matrix
        """
        return self._prob_matrix

    def get_unique_pages(self, prefixed=True):
        """
        Retrieves all the unique pages within the provided list of
        clickstreams.
        """

        populate_count_matrix = chain.from_iterable(self.clickstream_list)
        if prefixed:
            self.pages = sorted(
                list(set(populate_count_matrix)), key=lambda x: int(x[1:])
            )
        else:
            self.pages = sorted(
                list(set(populate_count_matrix)), key=lambda x: int(x)
            )

        return self.pages

    def initialise_count_matrix(self):
        """
        Initialises an empty count matrix.
        """
        self._count_matrix = np.zeros([
            len(self.pages),
            len(self.pages)
        ])

    def populate_count_matrix(self):
        """
        Assembles a matrix of counts of transitions from each possible state,
        to every other possible state.
        """

        self.initialise_count_matrix()
        # For each session in list of sessions
        for session in self.clickstream_list:
            for j in range(0, len(session) - 1):
                next_state = self.pages.index(session[j+1])
                current_state = self.pages.index(session[j])

                self._count_matrix[current_state, next_state] += 1

        return self._count_matrix

    @staticmethod
    def normalise_row(row):
        """
        Normalises each row in count matrix, to produce a probability.

        To be used when iterating over rows of `self.count_matrix`. Sum of each
        row adds up to 1.

        Args:
            row : Each row within numpy matrix to act upon.
        """
        row_sum = np.sum(row)
        if row_sum == 0:
            return row

        normalised = np.nan_to_num(np.divide(row, np.sum(row)))
        return normalised

    def compute_prob_matrix(self):
        """
        Computes the probability matrix for the input clickstream.
        """
        self._prob_matrix = np.apply_along_axis(self.normalise_row, 1,
                                                self.count_matrix)

    def calc_prob_to_page(self, clickstream: list, verbose=True) -> float:
        """
        Calculates the probability for a sequence of clicks (clickstream)
        taking place.

        Args:
            clickstream (list): Sequence of clicks (pages), for which to
                calculate the probability of occuring.
            verbose (bool, optional): Defaults to True. Specifies whether the
                output is printed to the terminal, or simply provided back.
        """

        total_prob = 1

        curr_page = self.pages.index(clickstream[0])

        for i in range(0, len(clickstream) - 1):
            next_page = self.pages.index(clickstream[i + 1])
            total_prob = total_prob * self.prob_matrix[curr_page, next_page]
            curr_page = next_page

        if verbose:
            print("Probability for clickstream: \n {} \nis{}".format(
                ':'.join(clickstream), total_prob
            ))

        return total_prob

    @staticmethod
    def permutations(iterable, r=None):
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

    @staticmethod
    def cartesian_product(iterable, repeats=1):
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

    def calc_prob_all_routes_to(self, clickstream: list, end_page: str,
                                clicks: int, cartesian_product=True):
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

        if cartesian_product:
            potential_routes = list(self.cartesian_product(self.pages,
                                                           repeats=clicks))
        else:
            potential_routes = list(self.permutations(self.pages, r=clicks))

        potential_routes_prob = []

        for route in tqdm(potential_routes):
            for state in clickstream[::-1]:
                route.insert(0, state)
            route.append(end_page)

            prob = self.calc_prob_to_page(route, verbose=False)
            potential_routes_prob.append(prob)

        return potential_routes, potential_routes_prob
