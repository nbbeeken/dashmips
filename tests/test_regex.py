"""Test regular expressions for every instruction."""


def test_la() -> None:
    """Test this format of instruction."""
    assert "foo".upper() == "FOO"


def test_jr() -> None:
    """Test this format of instruction."""
    assert 1 == 2
