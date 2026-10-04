def get_range_for_difficulty(difficulty: str):
    """
    Return the inclusive secret-number range for a difficulty level.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard". Any other value
            falls back to the "Normal" range.

    Returns:
        A (low, high) tuple of ints, both inclusive.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse raw text input from the guess box into an integer guess.

    Accepts plain integer strings ("42") and decimal strings ("42.9",
    truncated toward zero via int(float(raw))). Rejects None, empty
    strings, and any value that cannot be converted to a number
    (including whitespace-only strings).

    Args:
        raw: The raw text the player typed, or None.

    Returns:
        A (ok, guess_int, error_message) tuple:
            - ok: True if parsing succeeded.
            - guess_int: The parsed int guess, or None if parsing failed.
            - error_message: A user-facing error string, or None on success.
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def validate_range(value: int, low: int, high: int):
    """
    Check whether a parsed guess falls within the secret's range.

    Args:
        value: The parsed guess (an int).
        low: The low end of the difficulty's range.
        high: The high end of the difficulty's range.

    Returns:
        A (ok, error_message) tuple. error_message is None when ok is
        True, otherwise a user-facing string naming the valid range.
    """
    if low <= value <= high:
        return True, None
    return False, f"Enter a number between {low} and {high}."


def check_guess(guess, secret):
    """
    Compare a player's guess to the secret number and report the result.

    secret is normally an int, but app.py intentionally passes it as a
    str on alternating attempts; the TypeError fallback branch handles
    that case with an equivalent string comparison so the outcome and
    hint direction stay consistent either way.

    Args:
        guess: The player's parsed guess (an int).
        secret: The secret number, as an int or a str.

    Returns:
        An (outcome, message) tuple:
            - outcome: One of "Win", "Too High", "Too Low".
            - message: A player-facing hint string for that outcome.
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def get_proximity_hint(guess: int, secret: int, low: int, high: int) -> str:
    """
    Return a Hot/Cold style proximity label for how close a guess is.

    Distance is measured relative to the size of the difficulty's secret
    range, so "hot" means the same thing on Easy (1-20) as it does on
    Normal (1-100).

    Args:
        guess: The player's guess.
        secret: The secret number (always compared as an int).
        low: The low end of the difficulty's range.
        high: The high end of the difficulty's range.

    Returns:
        An emoji-prefixed proximity label, from "Burning Hot" (closest)
        to "Freezing Cold" (farthest).
    """
    span = max(high - low, 1)
    ratio = abs(guess - secret) / span

    if ratio <= 0.05:
        return "🔥🔥🔥 Burning Hot"
    if ratio <= 0.15:
        return "🔥 Hot"
    if ratio <= 0.35:
        return "🌤️ Warm"
    if ratio <= 0.6:
        return "❄️ Cool"
    return "🥶 Freezing Cold"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Apply one guess's outcome to the running score.

    A win awards points that decrease with attempt_number (minimum 10).
    A "Too High" outcome awards +5 on even attempt numbers and -5 on
    odd ones; a "Too Low" outcome always costs -5. Any other outcome
    leaves the score unchanged.

    Args:
        current_score: The score before this guess.
        outcome: One of "Win", "Too High", "Too Low" (as returned by
            check_guess).
        attempt_number: The 1-based attempt count for this guess.

    Returns:
        The updated score as an int.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
