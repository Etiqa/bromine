# pylint: disable=missing-docstring

from setuptools import setup, find_packages

setup(
    name='bromine',
    version='0.0.1.dev2',
    description='',
    long_description='',
    url='',
    author='',
    author_email='',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='',
    packages=find_packages('src'),
    # http://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages
    package_dir={'': 'src'},
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
