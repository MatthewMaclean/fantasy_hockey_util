from os import chdir
from os.path import dirname

try:
    from setuptools import setup, find_packages
except ImportError:
    # setuptools wasn't available, so install and try again
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from yfantasy import get_package_version, YFANTASY_MAIN

root_dir = dirname(__file__)

if root_dir != "":
    chdir(root_dir)

setup(
    name='fantasy_hockey_util',
    version=get_package_version(),
    author='Matthew Maclean',
    author_email='matthewcmaclean@gmail.com',
    description='Utility to get stats from the fantasy hockey league.',
    entry_points={
        'console_scripts': {
            '%s = yfantasy.cli:main' % YFANTASY_MAIN,
        }
    },
    packages=find_packages(exclude="test"),
    include_package_data=True,
    install_requires=[
        'rauth>=0.7.0',
    ],
)
