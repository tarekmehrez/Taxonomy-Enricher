"""
Contains the setup script for the package.
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = dict(

    # meta data
    name='taxonomy_extractor',
    version='1.0',

    # package
    package_dir={'': 'lib'},
    packages=['taxonomy_extractor',
              'taxonomy_extractor.config',
              'taxonomy_extractor.core',
              'taxonomy_extractor.exceptions',
              'taxonomy_extractor.util',
              'taxonomy_extractor.vectorspace',
              'taxonomy_extractor.main']
)

setup(**config)
