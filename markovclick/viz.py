"""
Functions for visualising Markov chain
"""

from graphviz import Digraph
import numpy as np
from markovclick.models import MarkovClickstream


def visualise_markov_chain(markov_chain: MarkovClickstream) -> Digraph:
    """
    Visualises Markov chain for clickstream as a graph, with individual pages
    as nodes, and edges between the first and second most likely nodes (pages).
    Probabilities for these transitions are annotated on the edges (arrows).

    Args:
        markov_chain (MarkovClickstream): Initialised MarkovClickstream object
            with probabilities computed.

    Returns:
        Digraph: Graphviz Digraph object, which can be rendered as an image or
            PDF, or displayed inside a Jupyter notebook.
    """
    if not isinstance(markov_chain, MarkovClickstream):
        raise TypeError(
            f'Argument `markov_chain` must be of type '
            f'MarkovClickstream. {type(markov_chain)} object provided '
            f'instead.'
        )
    graph = Digraph()
    prob = markov_chain.prob_matrix
    prob_matrix_sorted = np.argsort(markov_chain.prob_matrix, axis=1)
    nodes = markov_chain.pages
    for i, node in enumerate(nodes):
        graph.node(
            node, node, style='filled', fillcolor='#76ff03',
            fontname='Helvetica', penwidth='0', fontcolor='#1a237e'
        )
        first_trans = nodes[prob_matrix_sorted[i, -1]]
        most_prob = prob[i, prob_matrix_sorted[i, -1]]
        graph.edge(
            node, first_trans,
            label=f'{most_prob:.2f}',
            fontname='Helvetica', penwidth='1.5',
            color='#90caf9', arrowsize='0.75'
        )
        second_prob = prob[i, prob_matrix_sorted[i, -2]]
        sec_trans = nodes[prob_matrix_sorted[i, -2]]
        graph.edge(
            node, sec_trans,
            label=f'   {second_prob:.2f}',
            fontname='Helvetica', penwidth='0.75',
            fontsize='10', color='#90caf9', arrowsize='0.5'
        )
        if node != first_trans and node != sec_trans:
            graph.edge(
                node, node,
                label=f'   {prob[i, i]:.2f}',
                fontname='Helvetica', penwidth='1.8',
                fontsize='10', color='#cfd8dc', arrowsize='0.5'
            )
    return graph
