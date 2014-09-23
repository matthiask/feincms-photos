#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='feincms-photos',
    version=__import__('photos').__version__,
    description='Photo gallery version 42',
    long_description=read('README'),
    author='Matthias Kestenholz',
    author_email='mk@feinheit.ch',
    url='http://github.com/matthiask/feincms-photos/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=find_packages(
        exclude=['tests', 'example'],
    ),
    package_data={
        '': ['*.html', '*.txt'],
        'photos': [
            'locale/*/*/*.*',
            'static/photos/*.*',
            'static/photos/*/*.*',
            'templates/*.*',
            'templates/*/*.*',
            'templates/*/*/*.*',
            'templates/*/*/*/*.*',
        ],
    },
    install_requires=[
        'Django>=1.4.2',
        'FeinCMS',
        'towel',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
