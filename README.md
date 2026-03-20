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

### Game Purpose
The idea behind this app is pretty simple — it's a number guessing game built with Streamlit. You pick a difficulty, and the game picks a secret number. You keep guessing and the app tells you to go higher or lower until you get it right or run out of attempts. There's also a score that goes up when you win and down when you guess wrong.

### Bugs I Found

1. **The secret number kept changing** — Every time I clicked Submit, the secret number in the Debug panel was different. The game was literally unwinnable because the target moved on every click. Turns out `random.randint()` was running on every Streamlit rerun without being saved to session state.
2. **Had to click Submit twice** — I'd type a number, click Submit, and nothing would happen. I had to click again for it to actually register. The text input and button weren't inside a `st.form`, so they didn't fire together.
3. **New Game did nothing** — After losing, I'd click "New Game" and it would just sit there showing "Game over." It wasn't resetting the game status or clearing the history, so the app thought the game was still over.
4. **Scoring was off** — My first guess was being treated as attempt 2 because `attempts` started at 1 instead of 0. Also, the "Too High" penalty was weird — it gave you +5 on even attempts and -5 on odd ones, which made no sense.
5. **Hints pointed the wrong way** — When your guess was too high, the app said "Go HIGHER!" which is the opposite of what it should say. The hint messages were swapped.

### Fixes I Applied

- [x] Added a `st.session_state` guard around the secret number so it only gets generated once per game.
- [x] Put the text input and submit button inside a `st.form()` so everything submits in one click.
- [x] Fixed the New Game button to properly reset `attempts`, `status`, and `history`, and added `st.rerun()` so it refreshes right away.
- [x] Changed `attempts` to start at `0` instead of `1` to fix the off-by-one scoring problem.
- [x] Moved all the game logic into `logic_utils.py` with clean, consistent scoring — flat -5 for wrong guesses, no more weird even/odd behavior.
- [x] Created a `HINT_MESSAGES` dictionary with the correct directions — "Too High" now says "Go LOWER!" like it should.

## 📸 Demo


## 🚀 Stretch Features

