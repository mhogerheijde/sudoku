from setuptools import setup, find_packages

setup(
    name = "sudoku-solver",
    version = "0.0.0-dev",
    author = 'Matthias Hogerheijde',
    author_email = 'spamfilter@hogerheijde.net',
    url = 'http://hogerheijde.net',
    license = 'GPL',
    description = 'Sudoku Solver',
    packages = find_packages(exclude=('tests',)),
    test_suite = 'unittest2.collector',
    install_requires = [
        'distribute'
    ],
)
