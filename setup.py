#!/usr/bin/env python
from setuptools import setup

setup(
    name='snakecharmer',
    version='1.0.1',
    description="A collection of utilities for working with python",
    long_description=open('README.md').read(),
    author='HubSpot Dev Team',
    author_email='devteam+hapi@hubspot.com',
    url='https://github.com/HubSpot/snakecharmer',
    download_url='https://github.com/HubSpot/snakecharmer/tarball/v1.0.0',
    license='LICENSE.txt',
    packages=['snakecharmer'],
    install_requires=[
        'nose==1.1.2',
        'unittest2==0.5.1',
    ],
)
