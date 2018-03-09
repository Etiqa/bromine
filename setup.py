"""
https://packaging.python.org/tutorials/distributing-packages/
"""

import os
import re
from setuptools import setup, find_packages

PKG_NAME = 'bromine'
SRC_DIR = 'src'

def read_version(): # pylint: disable=missing-docstring
    basedir = os.path.dirname(__file__)
    srcdir = os.path.join(basedir, SRC_DIR)
    version_file = os.path.join(srcdir, PKG_NAME, 'version.py')
    with open(version_file, 'r') as fin:
        version_file_content = fin.read()
    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                              version_file_content, re.M)
    if not version_match:
        raise RuntimeError('Unable to find version string.')
    return version_match.group(1)

setup(
    name=PKG_NAME,
    version=read_version(),
    description='',
    long_description='',
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
    packages=find_packages(SRC_DIR),
    # http://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages
    package_dir={'': SRC_DIR},
    package_data={},
    data_files=[],
    install_requires=[],
    extras_require={
        'dev': [],
        'test': [],
    },
    entry_points={},
    project_urls={}
)
