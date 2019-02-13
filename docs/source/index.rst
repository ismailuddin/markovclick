markovclick
===============

.. figure:: _static/img/header.png
   :width: 750px
   
.. image:: https://readthedocs.org/projects/markovclick/badge/?version=latest
    :target: https://markovclick.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://circleci.com/gh/ismailuddin/markovclick/tree/master.svg?style=svg
    :target: https://circleci.com/gh/ismailuddin/markovclick/tree/master

.. image:: https://img.shields.io/aur/license/yaourt.svg


.. toctree::
    :hidden:
    :maxdepth: 2
    :caption: Contents:
    :glob:

    api/index
    usage

`markovclick` allows you to model clickstream data from websites as Markov
chains, which can then be used to predict the next likely click on a website
for a user, given their history and current state.

Requirements
------------

- Python 3.X
- numpy
- matplotlib
- seaborn (Recommended)
- pandas

Installation
-------------

Install either via the ``setup.py`` file:

.. code-block:: shell

    python setup.py install

or via ``pip``:

.. code-block:: shell

    pip install markovclick


Tests
------

Tests can be run using ``pytest`` or ``tox`` command from the root directory.

Documentation
--------------

To build the documentation, run ``make html`` inside the ``/docs`` directory,
or whatever output is preferred e.g. ``make latex``.
