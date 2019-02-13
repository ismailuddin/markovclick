"""
Setup file for installing package.
"""

from setuptools import setup, find_packages

__version__ = '0.1.1'

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name='markovclick',
    version=__version__,
    description='Package for modelling clickstream data using Markov chains',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/ismailuddin/markovclick',
    download_url='https://github.com/ismailuddin/markovclick/tarball/' + __version__,
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='markov chain data science machine learning statistics clickstream',
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Ismail Uddin'
)
