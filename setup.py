"""Setup for Dashmips."""
import sys
from io import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

if sys.version_info.major <= 2:
    sys.exit('Sorry, Python <= 2.7 is not supported')

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dashmips',
    version='0.0.11',
    author='Neal Beeken',
    url='https://gitlab.com/nbbeeken/dashmips',
    packages=find_packages(),
    description='Mips Interpreter',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Education',
        'Topic :: Software Development :: Assemblers',
        'Programming Language :: Assembly',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'dashmips = dashmips.__main__:main',
        ],
    }
)
