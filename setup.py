"""
https://packaging.python.org/tutorials/distributing-packages/
"""

import io
import os
import re
from setuptools import setup, find_packages

# pylint: disable=missing-docstring

PKG_NAME = 'bromine'
SRC_DIR = 'src'

BASEDIR = os.path.dirname(__file__)


def read(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as fin:
        return fin.read()


def version():
    version_file_content = read(os.path.join(BASEDIR, SRC_DIR, PKG_NAME, '_version.py'))
    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                              version_file_content, re.M)
    if not version_match:
        raise RuntimeError('Unable to find version string.')
    return version_match.group(1)


def long_description():
    return read(os.path.join(BASEDIR, 'README.md'))


setup(
    name=PKG_NAME,
    version=version(),
    description='A high-level web testing library based on Selenium and PageObject Pattern',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/Etiqa/bromine',
    author='Etiqa s.r.l.',
    author_email='',
    license='2-clause BSD License',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

    ],
    keywords='',
    project_urls={},
    # http://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages
    package_dir={'': SRC_DIR},
    packages=find_packages(SRC_DIR),
    package_data={},
    data_files=[],
    install_requires=[
        'Pillow',
        'PyHamcrest',
        'requests',
        'selenium',
        'six',
    ],
    extras_require={},
    python_requires=', '.join([
        '>=3.6',
        '<4',
    ]),
    entry_points={}
)
