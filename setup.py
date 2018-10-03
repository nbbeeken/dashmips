"""Setup for Dashmips."""
import sys
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

if sys.version_info.major <= 2:
    sys.exit('Sorry, Python <= 2.7 is not supported')

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dashmips',
    version='0.0.2',
    author='Neal Beeken',
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
