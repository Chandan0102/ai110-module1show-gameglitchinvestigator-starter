from streamlit.testing.v1 import AppTest

DIFFICULTY_RANGES = {
    "Easy": (1, 20),
    "Normal": (1, 100),
    "Hard": (1, 50),
}


def test_secret_regenerates_in_range_when_switching_to_easy():
    at = AppTest.from_file("app.py")
    at.run()

    # Force a secret that is valid for Normal but out of range for Easy.
    at.session_state.secret = 83
    at.selectbox[0].set_value("Easy").run()

    low, high = DIFFICULTY_RANGES["Easy"]
    assert low <= at.session_state.secret <= high


def test_secret_regenerates_in_range_when_switching_to_hard():
    at = AppTest.from_file("app.py")
    at.run()

    # Force a secret that is valid for Normal but out of range for Hard.
    at.session_state.secret = 83
    at.selectbox[0].set_value("Hard").run()

    low, high = DIFFICULTY_RANGES["Hard"]
    assert low <= at.session_state.secret <= high


def test_switching_difficulty_resets_attempts_and_history():
    at = AppTest.from_file("app.py")
    at.run()

    guess_input = [
        w for w in at.text_input if w.key.startswith("guess_input_")
    ][0]
    submit_button = [
        b for b in at.button if b.label == "Submit Guess \U0001f680"
    ][0]
    guess_input.set_value("1")
    submit_button.click()
    at.run()
    assert len(at.session_state.history) == 1

    at.selectbox[0].set_value("Hard").run()

    assert at.session_state.history == []
    assert at.session_state.attempts == 0
    assert at.session_state.status == "playing"


def test_switching_difficulty_updates_the_range_caption():
    at = AppTest.from_file("app.py")
    at.run()

    at.selectbox[0].set_value("Easy").run()
    captions = [c.value for c in at.caption]
    assert "Guess a number between 1 and 20." in captions
