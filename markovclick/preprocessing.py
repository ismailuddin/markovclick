import numpy as np
import pandas as pd


def getUniqueURLs(clickstream: list=None, dataframe=None, column: str=None):
    """
    Extracts unique URLs from a clickstream.
    
    Args:
        clickstream (list): Python list of URLs, from which to extract URLs
            form
        dataframe ([type]): Alternatively, specify a pandas DataFrame alongside
            the column name to extract URLs from, specified in `column` 
            argument.
        column (str): Column name from pandas DataFrame to extract unique
            URLs from

    Returns:
        uniqueURLs (list): List of unique URLs to use for generating 
            Markov chain clickstream.        
    """

    
