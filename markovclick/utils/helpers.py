"""
Helper utility functions
"""


def flatten_list(nested_list: [list]) -> list:
    """
    Function to flatten a two level nested lisst

    Args:
        nested_list (list): Nested list

    Returns:
        list: Flattened list
    """
    return [item for sublist in nested_list for item in sublist]
