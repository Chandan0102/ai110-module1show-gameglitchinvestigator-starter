from logic_utils import check_guess


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_guess_too_high_outcome():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low_outcome():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_guess_too_high_message_tells_player_to_go_lower():
    # Regression test for the reversed-hint glitch: when the guess is
    # ABOVE the secret, the message must tell the player to go LOWER,
    # not higher.
    _, message = check_guess(60, 50)
    assert "LOWER" in message
    assert "HIGHER" not in message


def test_guess_too_low_message_tells_player_to_go_higher():
    # Regression test for the reversed-hint glitch: when the guess is
    # BELOW the secret, the message must tell the player to go HIGHER,
    # not lower.
    _, message = check_guess(40, 50)
    assert "HIGHER" in message
    assert "LOWER" not in message


def test_guess_too_high_message_matches_outcome_for_string_secret():
    # Every other attempt in app.py compares against a string secret,
    # which routes check_guess through the TypeError fallback branch.
    # That branch must have the same (fixed) hint direction.
    outcome, message = check_guess(60, "50")
    assert outcome == "Too High"
    assert "LOWER" in message
    assert "HIGHER" not in message


def test_guess_too_low_message_matches_outcome_for_string_secret():
    outcome, message = check_guess(40, "50")
    assert outcome == "Too Low"
    assert "HIGHER" in message
    assert "LOWER" not in message
