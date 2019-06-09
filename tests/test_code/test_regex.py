"""Test regular expressions for every instruction."""
import re
from dashmips.instructions import Instructions


def test_add() -> None:
    """Test this format of instruction."""
    add_regex = Instructions["add"].regex
    assert re.match(add_regex, "add $t0, $t1, $t2") is not None
    assert re.match(add_regex, "add $t0, $zero, $t2") is not None
    assert re.match(add_regex, "add $t0, hi, lo") is not None
