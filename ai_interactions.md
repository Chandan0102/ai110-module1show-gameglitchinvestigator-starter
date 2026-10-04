# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Claude Code to add a visible Guess History sidebar as a new feature, instead of guesses only being visible inside the hidden "Developer Debug Info" expander. I was offered a choice between a High Score tracker, a Guess History sidebar, or both, and picked the Guess History sidebar.

**What did the agent do?**

Files touched: `app.py` only.
1. Changed `st.session_state.history` entries from plain values (a raw int or raw invalid string) to dicts of `{"guess": ..., "outcome": ...}`, so each entry carries its own result ("Win", "Too High", "Too Low", or "Invalid") instead of only the final outcome of the latest guess.
2. Moved the `history.append(...)` call for valid guesses to after `check_guess` runs, so the outcome is known before it's recorded.
3. Added a new sidebar section (`st.sidebar.subheader`, with an icon map for each outcome) that lists every guess this game, most recent first, e.g. `🎉 #4: 55 -> Win`.
4. Placed the new sidebar code near the bottom of the script, after the guess-submission and New Game logic run, specifically to avoid a stale-display bug: if it had been placed earlier in the script (before `st.session_state.history` is updated for the current rerun), it would always be one guess behind, the same class of bug as the earlier New Game stale-message issue.
5. Verified the feature by driving the app with Streamlit's `AppTest` framework: submitted a sequence of guesses (including an invalid one), confirmed the sidebar listed all of them in the right order with the right icons, then clicked New Game and confirmed the sidebar correctly reset to "No guesses yet this game."
6. Ran the full pytest suite (16 tests) to confirm the change to the history entry format didn't break the existing New Game reset tests, since those tests only check the list's length and emptiness, not its old int-based contents.

**What did you have to verify or fix manually?**

I ran the app in the browser myself, played a full game with a mix of too-high, too-low, and one invalid guess, and confirmed the sidebar updated immediately after each submit and reset correctly after New Game. I didn't need to correct anything the agent did, but I did make it explain why the new sidebar code had to go after the submit/New Game logic rather than near the other sidebar settings at the top, since that ordering wasn't obvious to me at first.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Non-numeric string ("banana") | "Add pytest edge-case tests for parse_guess covering non-numeric strings, negative numbers, and empty/None input" | `test_parse_guess_rejects_non_numeric_string` | Yes | A player will eventually type letters by mistake; this confirms parse_guess rejects it with a clean error instead of crashing. |
| Empty string ("") | (same prompt) | `test_parse_guess_rejects_empty_string` | Yes | Submitting the form with nothing typed is the single most likely accidental input, so it needs its own test even though it was already handled in code. |
| `None` input | (same prompt) | `test_parse_guess_rejects_none_input` | Yes | parse_guess explicitly checks for `None`, separate from the empty-string check; worth confirming that branch is actually reachable and correct. |
| Negative number ("-5") | (same prompt) | `test_parse_guess_accepts_negative_numbers` | Yes | This test revealed that parse_guess currently accepts negative numbers as a valid guess (no range check against 1-100), which is worth documenting as known behavior rather than a silent gap. |
| Decimal string ("42.9") | "What happens if parse_guess gets a decimal number, and is there a test for it?" | `test_parse_guess_truncates_decimal_strings` | Yes | parse_guess has special-case handling for a "." in the input (`int(float(raw))`); this confirms it truncates toward zero instead of rounding or raising. |
| Whitespace-only string ("   ") | "Are there any inputs that look valid but would still break parse_guess, like whitespace?" | `test_parse_guess_rejects_whitespace_only_string` | Yes | A player pressing the space bar instead of a digit should get the same "not a number" message as any other bad input, not an unhandled exception. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Run flake8 against logic_utils.py, app.py, and tests/, fix anything it
flags, and upgrade the docstrings in logic_utils.py to a professional
Args/Returns style for every function.
```

**Linting output before:**

```
(.venv) PS ...\ai110-module1show-gameglitchinvestigator-starter> python -m flake8 logic_utils.py app.py tests/
app.py:102:80: E501 line too long (83 > 79 characters)
app.py:112:80: E501 line too long (81 > 79 characters)
app.py:150:80: E501 line too long (88 > 79 characters)
app.py:152:80: E501 line too long (87 > 79 characters)
```

`logic_utils.py` and the `tests/` files had zero violations even before this pass; all 4 findings were in `app.py`.

**Linting output after:**

```
(.venv) PS ...\ai110-module1show-gameglitchinvestigator-starter> python -m flake8 logic_utils.py app.py tests/
(no output - clean)
```

**Changes applied:**

- Wrapped the 4 over-long lines in `app.py` (two `history.append({...})` calls and the sidebar history loop/write) across multiple lines so each stays under 79 characters. Logic is unchanged, only formatting.
- Rewrote every docstring in `logic_utils.py` (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) from one-line summaries into full Args/Returns docstrings, including the non-obvious behavior each function has (e.g. that `check_guess`'s `secret` can arrive as a `str` on alternating attempts, and that `parse_guess` truncates decimals toward zero).
- Re-ran the full pytest suite (16 tests) after both sets of changes to confirm nothing broke, since the formatting and docstring changes touched the same functions the tests exercise. All 16 still pass.
- Added `flake8` to `requirements.txt` so the lint step is reproducible.

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
