#!/usr/bin/env python

from setuptools import setup
import sys

setup(
    name='find-meaning',
    version='0.0.1',
    description='Finds the meaning for a particular word',
    long_description=open('README.rst').read(),
    author='Taranjeet Singh',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stablegit
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords="dictionary cli, word meaning, meaning-cli",
    author_email='reachtotj@gmail.com',
    url='https://github.com/staranjeet/dictionary-cli',
    packages=['findmeaning'],
    install_requires=[
        'docopt>=0.6.2',
        "requests>=2.7.0",
        'colorama==0.3.3'
    ],
    entry_points={
        'console_scripts': [
            'findmeaning = findmeaning.meaning:main'
            ],
    }
)
