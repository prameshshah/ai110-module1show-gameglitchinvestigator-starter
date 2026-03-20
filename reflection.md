# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

**Bug 1 — Secret number kept changing on every submit.**
I expected the secret number to stay the same for the entire round so I could narrow down my guess. Instead, every time I clicked "Submit Guess," the Developer Debug Info showed a brand-new secret number. This happened because `random.randint()` ran at the top level of the script, and Streamlit reruns the entire script on every interaction, so without proper `st.session_state` guarding the secret was regenerated each time.

**Bug 2 — Submit Guess required a double-click to register.**
I expected to type a number and click "Submit Guess" once to see the result. Instead, the first click only committed the text input value (triggering a rerun without the button press), and I had to click a second time for the guess to actually process. This was caused by the text input and button being separate Streamlit widgets outside of a `st.form`, so they did not submit together in a single action.

**Bug 3 — "New Game" button did not reset the game.**
After winning or losing, I expected clicking "New Game" to fully restart the game. Instead, it still showed the "You already won" or "Game over" message and blocked play. The handler reset `attempts` and `secret` but never reset `status` back to `"playing"` or cleared the `history`, so the status check at the top of the game loop kept blocking the player.

**Bug 4 — Scoring was inconsistent and unfair.**
I expected correct guesses to award points based on how few attempts I used, and wrong guesses to deduct a flat penalty. Instead, the win bonus docked an extra 10 points (using `attempt_number + 1` instead of `attempt_number`), and "Too High" guesses inconsistently gave +5 on even attempts but -5 on odd attempts, while "Too Low" always deducted 5. This made the scoring feel random and unfair.

---

## 2. How did you use AI as a teammate?

I used **Claude Code (Agent mode in VS Code)** as my primary AI tool for this project. I gave it the full codebase context and described the symptoms I was seeing (double-click to submit, New Game not working), and it read through `app.py`, `logic_utils.py`, and the test file to diagnose the issues.

**Correct AI suggestion:** Claude Code identified that `st.session_state.attempts` was initialized to `1` instead of `0`, causing an off-by-one bug where the first guess was scored as attempt 2 and the "Attempts left" counter was wrong from the start. I verified this by checking the Developer Debug Info panel — after the fix, the attempts counter started at 0 and incremented to 1 on the first submit, and the score for a first-attempt win was 90 (not 80). I also wrote two pytest cases (`test_first_guess_win_scores_90` and `test_second_guess_win_scores_80`) that simulate the game loop and confirm the correct attempt numbering.

**Incorrect/misleading AI suggestion:** Claude Code initially suggested that the hint messages ("Higher/Lower") in `logic_utils.py` might be reversed, based on the project instructions saying "The hints are wrong. Fix them." After reading the actual `check_guess` function, it turned out the logic was correct — `guess > secret` returns "Too High" and the HINT_MESSAGES map shows "Go LOWER!", which is the right direction. I verified this by running the existing `test_guess_too_high` and `test_guess_too_low` tests, both of which passed without changes. The AI corrected itself after reading the code, but the initial assumption was misleading.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed by combining two approaches: **manual testing in the running app** and **automated pytest cases**. For manual testing, I used the Developer Debug Info panel to watch `attempts`, `secret`, and `score` update in real time after each submit. If the values matched my expectations (e.g., attempts going 0 → 1 on first guess, score = 90 for a first-attempt win), I considered the fix verified.

For automated testing, I ran `pytest tests/test_game_logic.py -v` after every change. The key test I added was `test_first_guess_win_scores_90`, which simulates the app's game loop: it starts `attempts` at 0, increments to 1, calls `check_guess` and `update_score`, and asserts the score is 90. This test would have **failed** with the old buggy code (attempts starting at 1 would yield attempt 2, scoring only 80). I also added `test_second_guess_win_scores_80` to verify multi-turn flow. All 20 tests passed after the fixes.

Claude Code helped design the game-flow simulation tests. I asked it to write pytest cases targeting the off-by-one bug, and it created tests that replicate the exact logic from `app.py` (initialize attempts, increment, check, score) rather than just testing `update_score` in isolation. This approach catches integration-level bugs that unit tests on individual functions would miss.

---

## 4. What did you learn about Streamlit and state?

The secret number kept changing because Streamlit reruns the **entire** Python script from top to bottom every time the user interacts with the page — clicking a button, typing in an input, or toggling a checkbox all trigger a full rerun. If `random.randint()` is called at the top level without any guard, it generates a brand-new number on every single rerun, so the player is chasing a moving target they can never catch.

If I were explaining Streamlit to a friend, I would say: "Think of your script like a recipe that gets cooked from scratch every time someone touches the page. Nothing survives between reruns unless you put it in a special locker called `st.session_state`. Regular variables get wiped clean each time, but anything stored in session state persists across reruns — like saving your game progress between levels."

The fix that gave the game a stable secret number was wrapping the `random.randint()` call in an `if "secret" not in st.session_state:` guard (line 36-37 in `app.py`). This means the secret is only generated once — the very first time the app runs — and then lives safely in `st.session_state.secret` through all subsequent reruns. A new secret is only created when the player explicitly clicks "New Game", which deliberately overwrites `st.session_state.secret` with a fresh random value.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
