"""Run all dashmips tests."""
import os
import unittest

from tap import TAPTestRunner

if __name__ == '__main__':
    tests_dir = os.path.dirname(os.path.abspath('test'))

    loader = unittest.TestLoader()
    tests = loader.discover(tests_dir, 'test_*.py')

    runner = TAPTestRunner()
    runner.set_format('{method_name}: {short_description}')
    runner.run(tests)
