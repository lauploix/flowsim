'''
Created on Aug 4, 2016

@author: plume
'''
from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import os

import flowsim

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md') #, 'CHANGES.txt')

setup(
    name='flowsim',
    version=flowsim.__version__,
    url='https://github.com/lauploix/flowsim/',
    license='Apache Software License',
    author='Laurent Ploix',
    tests_require=[],
    install_requires=[],
    #cmdclass={'test': PyTest},
    author_email='laurent.ploix@gmail.com',
    description='Simulation of software development flows',
    long_description=long_description,
    packages=['flowsim'],
    include_package_data=True,
    platforms='any',
    test_suite='flowsim.test.test_sandman',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    extras_require={
        'testing': [],
    }
)