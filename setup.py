#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import os
import sys
from distutils.version import StrictVersion
from setuptools import setup, find_packages, __version__ as setuptool_version

dirname = os.path.abspath(os.path.dirname(__file__))


REQUIREMENTS_FILES = [
    {'name': 'common-requirements.txt'},
    {'name': 'py2-requirements.txt', 'marker': 'python_version<"3.0"', "include": sys.version_info < (3,0)},
    {'name': 'py3-requirements.txt', 'marker': 'python_version>"3.0"', "include": sys.version_info > (3,0)},
]


def get_url(ir):
    if hasattr(ir, 'url'): return ir.url
    if ir.link is None: return
    return ir.link.url


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


def read_requirements_file(path):
    if not os.path.lexists(path):
        return
    with open(path) as f:
        lines = f.readlines()
    for line in lines:
        line = line.split('#', 1)[0]
        line = line.strip()
        if line.startswith('-'):
            continue
        yield line


def read_requirements_files(files):
    reqs = []
    for file in files:
        if StrictVersion(setuptool_version) >= StrictVersion('20.2'):
            reqs.extend([('{};{}'.format(req, file['marker']) if file.get('marker') else req)
                         for req in read_requirements_file(file['name'])])
        elif file.get('include', True):
            # Retrocompatibility mode for setuptools < 20.2
            reqs.extend(list(read_requirements_file(file['name'])))
    return reqs


setup_requirements = [
    # TODO(Nekmo): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='then',
    version='0.1.0',
    description="When \"something\" THEN send email/sms/telegram/event/execute... or Whatever ",
    long_description=readme + '\n\n' + history,
    author="Nekmo",
    author_email='contacto@nekmo.com',
    url='https://github.com/Nekmo/then',
    packages=find_packages(include=['then']),
    entry_points={
        'console_scripts': [
            'then=then.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=read_requirements_files(REQUIREMENTS_FILES),
    license="MIT license",
    zip_safe=False,
    keywords='then',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
