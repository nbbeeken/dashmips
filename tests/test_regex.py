"""Test regular expressions for every instruction."""
import unittest


class RegexTests(unittest.TestCase):
    """Test the regex for mips."""

    def la_test(self):
        """Test this format of instruction."""
        self.assertEqual('foo'.upper(), 'FOO')

    def jr_test(self):
        """Test this format of instruction."""
        self.assertEqual(1, 2)
