import random

import altair as alt
import pandas as pd
import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    get_proximity_hint,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "game_id" not in st.session_state:
    st.session_state.game_id = 0

st.subheader("Make a guess")

st.caption(f"Guess a number between {low} and {high}.")

metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    st.metric("Score", st.session_state.score)
with metric_col2:
    st.metric("Attempts Left", attempt_limit - st.session_state.attempts)
with metric_col3:
    st.metric("Difficulty", difficulty)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

with st.form(key=f"guess_form_{difficulty}_{st.session_state.game_id}"):
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}_{st.session_state.game_id}"
    )
    submit = st.form_submit_button("Submit Guess 🚀")

col1, col2 = st.columns(2)
with col1:
    new_game = st.button("New Game 🔁")
with col2:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.game_id += 1
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(
            {"guess": raw_guess, "outcome": "Invalid"}
        )
        st.error(err)
    else:
        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        st.session_state.history.append(
            {"guess": guess_int, "outcome": outcome}
        )

        if show_hint:
            st.warning(message)
            if outcome != "Win":
                proximity = get_proximity_hint(
                    guess_int, st.session_state.secret, low, high
                )
                st.caption(f"Proximity: {proximity}")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.sidebar.divider()
st.sidebar.subheader("📜 Guess History")

HISTORY_ICONS = {
    "Win": "🎉",
    "Too High": "📉",
    "Too Low": "📈",
    "Invalid": "⚠️",
}

if st.session_state.history:
    numbered_history = list(enumerate(st.session_state.history, start=1))
    for position, entry in reversed(numbered_history):
        icon = HISTORY_ICONS.get(entry["outcome"], "")
        st.sidebar.write(
            f"{icon} #{position}: {entry['guess']} -> {entry['outcome']}"
        )
else:
    st.sidebar.caption("No guesses yet this game.")

st.divider()
st.subheader("🔢 Numbers Guessed")

numeric_guesses = [
    entry for entry in st.session_state.history
    if isinstance(entry["guess"], int)
]

if numeric_guesses:
    guesses_df = pd.DataFrame(numeric_guesses)
    OUTCOME_LABELS = {"Too Low": "Low", "Too High": "High", "Win": "Win"}
    guesses_df["label"] = guesses_df["outcome"].map(OUTCOME_LABELS)
    outcome_colors = alt.Scale(
        domain=["Low", "High", "Win"],
        range=["#1f77b4", "#d62728", "#2ca02c"],
    )
    points = (
        alt.Chart(guesses_df)
        .mark_circle(size=200)
        .encode(
            x=alt.X(
                "guess:Q",
                scale=alt.Scale(domain=[low, high]),
                title=f"Guess range ({low} to {high})",
            ),
            y=alt.value(0),
            color=alt.Color("label:N", scale=outcome_colors, title="Result"),
            tooltip=["guess", "outcome"],
        )
    )
    labels = points.mark_text(dy=-15).encode(text="guess:Q")
    number_line = (points + labels).properties(height=120)
    st.altair_chart(number_line, width="stretch")
else:
    st.caption("No guesses yet this game.")

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
