from streamlit.testing.v1 import AppTest


def make_app():
    at = AppTest.from_file("app.py")
    at.run()
    return at


def _guess_input(at):
    return [w for w in at.text_input if w.key.startswith("guess_input_")][0]


def _submit_button(at):
    return [b for b in at.button if b.label == "Submit Guess \U0001f680"][0]


def _new_game_button(at):
    return [b for b in at.button if b.label == "New Game \U0001f501"][0]


def _submit(at, guess_text):
    # The guess box lives inside an st.form, so typing a value alone does
    # not submit it - the form's submit button must also be triggered.
    _guess_input(at).set_value(guess_text)
    _submit_button(at).click()
    at.run()


def test_new_game_resets_status_after_a_win():
    at = make_app()
    secret = at.session_state.secret

    _submit(at, str(secret))
    assert at.session_state.status == "won"

    _new_game_button(at).click()
    at.run()

    assert at.session_state.status == "playing"
    assert not at.error
    assert not at.success


def test_new_game_clears_history():
    at = make_app()
    secret = at.session_state.secret
    wrong_guess = secret + 1 if secret < 100 else secret - 1

    _submit(at, str(wrong_guess))
    assert len(at.session_state.history) == 1

    _new_game_button(at).click()
    at.run()

    assert at.session_state.history == []


def test_new_game_clears_the_guess_input_box():
    at = make_app()
    secret = at.session_state.secret
    wrong_guess = secret + 1 if secret < 100 else secret - 1

    _submit(at, str(wrong_guess))
    assert _guess_input(at).value == str(wrong_guess)

    _new_game_button(at).click()
    at.run()

    assert _guess_input(at).value in (None, "")
