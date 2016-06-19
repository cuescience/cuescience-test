#!/usr/bin/env python

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='cuescience-test',
    version='0.2.0',
    description='Custom test runner for all projects',
    maintainer='cuescience',
    maintainer_email='kontakt@cuescience.de',
    license="MIT",
    url='',
    packages=['testing', ],
)
