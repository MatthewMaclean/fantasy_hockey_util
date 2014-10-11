from os import chdir
from os.path import dirname, isfile

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

keep = ""
if isfile('auth'):
    keep = raw_input("Yahoo developer credentials are already detected, "
                     "do you wish to keep them? (y/n) ")

if keep is not "y":
    print ""
    print "Creating auth file to store yahoo developer credentials"
    print "https://developer.yahoo.com"
    print ""
    consumer_key = raw_input("Enter your consumer key: ")
    consumer_secret = raw_input("Enter your consumer secret: ")

    f = open('auth', 'w')
    f.write("%s %s" % (consumer_key, consumer_secret))

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
    test_suite='unittest2.collector',
    tests_require=[
        'unittest2>=0.5.1',
        'pep8>=1.5.7',
    ],
)
