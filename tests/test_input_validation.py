from logic_utils import validate_range
from streamlit.testing.v1 import AppTest


def test_validate_range_accepts_value_within_range():
    ok, err = validate_range(50, 1, 100)
    assert ok is True
    assert err is None


def test_validate_range_accepts_boundary_values():
    ok_low, err_low = validate_range(1, 1, 100)
    ok_high, err_high = validate_range(100, 1, 100)
    assert ok_low is True and err_low is None
    assert ok_high is True and err_high is None


def test_validate_range_rejects_value_above_high():
    ok, err = validate_range(500, 1, 100)
    assert ok is False
    assert err == "Enter a number between 1 and 100."


def test_validate_range_rejects_value_below_low():
    ok, err = validate_range(-5, 1, 100)
    assert ok is False
    assert err == "Enter a number between 1 and 100."


def _submit(at, guess_text):
    guess_input = [
        w for w in at.text_input if w.key.startswith("guess_input_")
    ][0]
    submit_button = [
        b for b in at.button if b.label == "Submit Guess \U0001f680"
    ][0]
    guess_input.set_value(guess_text)
    submit_button.click()
    at.run()


def test_out_of_range_guess_does_not_count_as_an_attempt_or_history():
    at = AppTest.from_file("app.py")
    at.run()
    at.session_state.secret = 55  # Normal difficulty, range 1-100

    attempts_before = at.session_state.attempts

    _submit(at, "500")

    assert at.session_state.attempts == attempts_before
    assert at.session_state.history == []
    assert [e.value for e in at.error] == ["Enter a number between 1 and 100."]


def test_non_numeric_guess_does_not_count_as_an_attempt_or_history():
    at = AppTest.from_file("app.py")
    at.run()
    at.session_state.secret = 55

    attempts_before = at.session_state.attempts

    _submit(at, "banana")

    assert at.session_state.attempts == attempts_before
    assert at.session_state.history == []
    assert [e.value for e in at.error] == ["That is not a number."]


def test_valid_guess_still_counts_as_an_attempt_and_history():
    at = AppTest.from_file("app.py")
    at.run()
    at.session_state.secret = 55

    attempts_before = at.session_state.attempts

    _submit(at, "40")

    assert at.session_state.attempts == attempts_before + 1
    assert at.session_state.history == [{"guess": 40, "outcome": "Too Low"}]
