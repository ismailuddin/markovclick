from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '0.0.1'

HERE = path.abspath(path.dirname(__file__))

LONG_DESCRIPTION = """`markovclick` allows you to model clickstream data from\
websites as Markov chains, which can then be used to predict the next likely\
click on a website for a user, given their history and current state.
"""

# Get the dependencies and installs
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    ALL_REQS = f.read().split('\n')

INSTALL_REQUIRES = [x.strip() for x in ALL_REQS if 'git+' not in x]
DEPENDENCY_LINKS = [x.strip().replace('git+', '') for x in ALL_REQS if x.startswith('git+')]

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
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Ismail Uddin',
    INSTALL_REQUIRES=INSTALL_REQUIRES,
    DEPENDENCY_LINKS=DEPENDENCY_LINKS,
    author_email='ismail.sameeuddin@gmail.com'
)
