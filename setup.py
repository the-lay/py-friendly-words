#!/usr/bin/env python

from setuptools import setup, find_packages

# version fetch
from friendlywords import __version__

# readme fetch
with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='friendlywords',
      version=__version__,
      description='Python package to generate random human-readable strings, e.g. project and experiment names',
      long_description=long_description,
      long_description_content_type='text/markdown',
      license='MIT',
      author='the-lay',
      url='https://github.com/the-lay/py-friendly-words',
      platforms=['any'],
      packages=find_packages(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3 :: Only',
      ]
)

