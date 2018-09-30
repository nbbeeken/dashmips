"""Setup for Dashmips."""
from setuptools import setup

setup(
    name='dashmips',
    version='0.0.1',
    packages=['dashmips'],
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': [
            'dashmips = dashmips.__main__:main',
        ],
    }
)
