from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty


# --- check_guess tests ---

def test_winning_guess():
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- parse_guess tests ---

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_float_string():
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3
    assert err is None

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_parse_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_parse_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


# --- update_score tests ---

def test_score_win_first_attempt():
    # attempt 1: 100 - 10*1 = 90
    score = update_score(0, "Win", 1)
    assert score == 90

def test_score_win_later_attempt():
    # attempt 5: 100 - 10*5 = 50
    score = update_score(0, "Win", 5)
    assert score == 50

def test_score_win_minimum_points():
    # attempt 10: 100 - 100 = 0, clamped to 10
    score = update_score(0, "Win", 10)
    assert score == 10

def test_score_too_high():
    score = update_score(50, "Too High", 1)
    assert score == 45

def test_score_too_low():
    score = update_score(50, "Too Low", 1)
    assert score == 45

def test_score_too_high_consistent():
    # "Too High" should always deduct 5, regardless of attempt number
    score_odd = update_score(50, "Too High", 1)
    score_even = update_score(50, "Too High", 2)
    assert score_odd == score_even == 45


# --- get_range_for_difficulty tests ---

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_hard_range():
    assert get_range_for_difficulty("Hard") == (1, 200)

def test_default_range():
    assert get_range_for_difficulty("Unknown") == (1, 100)


# --- game-flow simulation tests (targets the off-by-one attempts bug) ---

def test_first_guess_win_scores_90():
    """Simulate the app's game loop: attempts starts at 0, increments to 1
    before scoring.  The old bug started attempts at 1, so the first guess
    was scored as attempt 2 (yielding 80 instead of 90)."""
    attempts = 0                          # correct initial state
    attempts += 1                         # increment before processing guess
    outcome = check_guess(50, 50)         # winning guess
    score = update_score(0, outcome, attempts)
    assert attempts == 1
    assert score == 90                    # 100 - 10*1 = 90, NOT 80


def test_second_guess_win_scores_80():
    """After one wrong guess, a correct second guess should score 80."""
    attempts = 0
    # first guess — wrong
    attempts += 1
    outcome1 = check_guess(30, 50)
    score = update_score(0, outcome1, attempts)
    assert outcome1 == "Too Low"
    assert score == -5
    # second guess — correct
    attempts += 1
    outcome2 = check_guess(50, 50)
    score = update_score(score, outcome2, attempts)
    assert attempts == 2
    assert score == -5 + 80              # 100 - 10*2 = 80
