#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# Package meta-data.
NAME = 'tracking'
DESCRIPTION = 'Plot tracking data from video footage onto a 2D plan'
URL = ''
EMAIL = 'fm.le.regent@gmail.com'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = None

REQUIRED = [
        'numpy',
        'opencv-python',
        'matplotlib',
        'seaborn'
    ]

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


setup(
    name=NAME,
    description=DESCRIPTION,
    author_email=EMAIL,
    packages=find_packages(exclude=('tests')),
	install_requires=REQUIRED,
    zip_safe=False,
    include_package_data=True,
)

