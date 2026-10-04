# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

## 📸 Demo Walkthrough

Secret number is 53 (Normal difficulty, range 1 to 100).

1. User enters a guess of 40. The game returns "Too Low" with the hint "Go HIGHER!", and the score drops to -5.
2. User enters a guess of 70. The game returns "Too High" with the hint "Go LOWER!", and the score drops to -10.
3. User enters a guess of 53. The game returns "Correct!", the app shows "You won! The secret was 53. Final score: 30".
4. User clicks "New Game". A new secret is picked (respecting the selected difficulty's range), the guess history clears, the guess box is blanked, and the win message disappears so the game is immediately playable again. (Note: score is not reset by "New Game" and carries over between games.)

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->
![alt text](image.png)

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:


(.venv) PS C:\Users\sinha\Desktop\AI110\ai110-module1show-gameglitchinvestigator-starter> python -m pytest
==================================================== test session starts ====================================================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\sinha\Desktop\AI110\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.15.1
collected 10 items                                                                                                           

tests\test_game_logic.py .......                                                                                       [ 70%]
tests\test_new_game_reset.py ...                                                                                       [100%]

==================================================== 10 passed in 3.13s =====================================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
