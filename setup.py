"""
https://packaging.python.org/tutorials/distributing-packages/
"""

import codecs
import os
import re
from setuptools import setup, find_packages

# pylint: disable=missing-docstring

PKG_NAME = 'bromine'
SRC_DIR = 'src'

BASEDIR = os.path.dirname(__file__)


def read(file_path):
    with codecs.open(file_path, 'rU', encoding='utf-8') as fin:
        return fin.read()


def version():
    version_file_content = read(os.path.join(BASEDIR, SRC_DIR, PKG_NAME, 'version.py'))
    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                              version_file_content, re.M)
    if not version_match:
        raise RuntimeError('Unable to find version string.')
    return version_match.group(1)


def long_description():
    return read(os.path.join(BASEDIR, 'README.rst'))


setup(
    name=PKG_NAME,
    version=version(),
    description='',
    long_description=long_description(),
    url='',
    author='Etiqa s.r.l.',
    author_email='',
    license='2-clause BSD License',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='',
    project_urls={},
    # http://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages
    package_dir={'': SRC_DIR},
    packages=find_packages(SRC_DIR),
    package_data={},
    data_files=[],
    install_requires=[
        'six',
        'selenium',
    ],
    extras_require={},
    python_requires=', '.join([
        '>=2.7',
        '!=3.0.*',
        '!=3.1.*',
        '!=3.2.*',
        '!=3.3.*',
        '!=3.4.*',
        '!=3.5.*',
        '<4',
    ]),
    entry_points={}
)
