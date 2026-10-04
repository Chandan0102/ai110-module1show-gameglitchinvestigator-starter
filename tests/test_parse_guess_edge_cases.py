from logic_utils import parse_guess


def test_parse_guess_rejects_non_numeric_string():
    ok, value, err = parse_guess("banana")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_guess_rejects_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_guess_rejects_none_input():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_guess_accepts_negative_numbers():
    # parse_guess does not reject negative numbers - a negative guess is
    # parsed as a valid int and left for check_guess to report as "Too Low".
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None


def test_parse_guess_truncates_decimal_strings():
    ok, value, err = parse_guess("42.9")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_rejects_whitespace_only_string():
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None
    assert err == "That is not a number."
