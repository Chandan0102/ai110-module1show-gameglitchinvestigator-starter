# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Secret 31, input 55| GO LOWER | GO Higher| no error| Location: App.py   function: check_guess |
| Click on "New Game"| game reset | the last message contineus to display | no error| Location: App.py |
| Change Difficulty to "Hard"| Make a guess to show "Guess a number between 1 and 50"|Make a guess shows "Guess a number between 1 and 100" | no error | Location : App.py  function: get_range_for_difficulty |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? Claude Code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
My input - I found a glicth in the code, when the usert input is higher or lower, game says to guess lower or higher. so the logic is reversed, please find relevent code section and advsie on fix
Claude suggestion  - Found it. The glitch is in check_guess: the hint messages are swapped relative to the comparison.

When guess > secret (the guess is too high), it returns "📈 Go HIGHER!" — but since the guess was already above the secret, the player should be told to go lower. Same mirrored mistake in the except TypeError fallback block (lines 45-47), which handles the string-compared secret case (triggered every other attempt via the attempts % 2 == 0 toggle at app.py:158).

Fix — swap the messages (keep the outcome labels "Too High"/"Too Low" as-is, since those are correct).

I accepted above suggestion.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed? Asked Claude to write test cases and verify . I did manual verfication as well by running the program and checking if outout values are not right. 
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  Scenario 1 - Fix sugegstion logic. I ran pytest tests/test_game_logic.py against logic_utils.check_guess after Claude refactored the function out of app.py and applied the higher/lower fix. Two of the tests specifically assert the hint text direction (for example, guess 60 vs secret 50 must contain "LOWER" and not "HIGHER"), including a version where the secret is passed as a string to cover the attempts % 2 == 0 branch in app.py that compares against str(secret). All 7 tests passed, which gave me confidence the fix was correct in both code paths, not just the common one. Separately, I manually tested the running app by typing a guess (69) and pressing Enter, and found the game didn't respond until I clicked "Submit Guess" a second time. This manual test surfaced a bug pytest wouldn't have caught, since it was a Streamlit widget/form interaction issue rather than a logic error.

  Scernaio 2 - New Game reset bug
  My input: I noticed clicking "New Game" didn't clear the previous win/loss message, the guess history, or the last guess I'd typed into the input box, so I asked Claude to look into it and fix it.

  Claude's work: Claude traced it to three issues in app.py. The New Game handler never reset status back to "playing", so the old win/loss message kept blocking the page through an st.stop() call. It also never cleared history. And the guess text box kept its old value because Streamlit ties a widget's value to its key across reruns. Claude fixed all three: reset status and history on New Game, and added a game_id counter baked into the guess input's key so each New Game click gets a genuinely fresh, empty box. It also wrote a new test file, tests/test_new_game_reset.py, using Streamlit's AppTest framework to simulate submitting a guess and clicking New Game, then checking that status, history, and the input all reset. It even reverted the fix temporarily to confirm those tests actually failed on the old code, then passed again once restored.

  What I did: I ran the app myself, played a round to a win, clicked New Game, and confirmed in the browser that the message cleared, the history was empty, and the input box was blank. I also ran the full pytest suite myself and saw all 10 tests pass.

- Did AI help you design or understand any tests? How?
  Yes. For the hint-direction bug, Claude explained that check_guess has two branches, a normal numeric comparison and a TypeError fallback that triggers when the secret is compared as a string (which happens every other attempt in app.py), and that both branches needed the same fix. I wouldn't have thought to test the string-secret path on my own. For the New Game bug, Claude introduced me to Streamlit's AppTest framework, which simulates clicking buttons and filling in widgets in a real app run instead of just calling a function directly, since the reset logic lives in session state and button clicks rather than a plain function I could call in a test. It also showed me the trick of reverting the fix temporarily and rerunning the tests to prove they'd actually fail on the old buggy code, which is how I now understand a test is only useful if it can fail.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
