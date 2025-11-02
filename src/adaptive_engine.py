# This list defines the order of our levels
DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]

# We define "fast" as answering in under 5 seconds.
# You can change this number to make the game easier or harder!
FAST_THRESHOLD = 5.0 

def get_next_difficulty(current_difficulty, last_attempt):
    """
    Decides the next difficulty level based on the last attempt.
    
    Args:
        current_difficulty (str): "Easy", "Medium", or "Hard"
        last_attempt (dict): A dictionary from the tracker, e.g.,
            {'correct': True, 'time_taken': 3.4, 'difficulty': 'Easy'}

    Returns:
        str: The next difficulty level ("Easy", "Medium", or "Hard")
    """
    
    # Get data from the last attempt
    was_correct = last_attempt["was_correct"]
    time_taken = last_attempt["time_taken"]
    
    # Find the current level's index (0 for Easy, 1 for Medium, 2 for Hard)
    current_index = DIFFICULTY_LEVELS.index(current_difficulty)
    
    # This is the Core Adaptive Logic!
    if was_correct and time_taken < FAST_THRESHOLD:
        # Rule 1: Correct and Fast -> Increase difficulty
        print("-> (Logic: Correct and fast. Increasing difficulty.)")
        if current_index < 2:  # Check we're not already at "Hard"
            next_index = current_index + 1
        else:
            next_index = current_index  # Stay at Hard
            
    elif not was_correct:
        # Rule 2: Incorrect -> Decrease difficulty
        print("-> (Logic: Incorrect. Decreasing difficulty.)")
        if current_index > 0:  # Check we're not already at "Easy"
            next_index = current_index - 1
        else:
            next_index = current_index  # Stay at Easy
            
    else:
        # Rule 3: Correct but Slow -> Stay at the same level
        print("-> (Logic: Correct but slow. Staying at same level.)")
        next_index = current_index
        
    # Return the string name of the next level
    return DIFFICULTY_LEVELS[next_index]

# -----------------------------------------------------------------
# This is our test block.
# -----------------------------------------------------------------
if __name__ == "__main__":
    print("--- Testing Adaptive Engine ---")

    # Scenario 1: Correct and Fast on "Easy"
    # Expect: Move to "Medium"
    print("\nScenario 1: Easy, Correct, Fast")
    last_attempt_1 = {"was_correct": True, "time_taken": 3.1}
    current_level_1 = "Easy"
    next_level_1 = get_next_difficulty(current_level_1, last_attempt_1)
    print(f"Result: Went from {current_level_1} -> {next_level_1} (Expected: Medium)")

    # Scenario 2: Incorrect on "Medium"
    # Expect: Move to "Easy"
    print("\nScenario 2: Medium, Incorrect, Slow")
    last_attempt_2 = {"was_correct": False, "time_taken": 8.5}
    current_level_2 = "Medium"
    next_level_2 = get_next_difficulty(current_level_2, last_attempt_2)
    print(f"Result: Went from {current_level_2} -> {next_level_2} (Expected: Easy)")

    # Scenario 3: Correct but Slow on "Medium"
    # Expect: Stay at "Medium"
    print("\nScenario 3: Medium, Correct, Slow")
    last_attempt_3 = {"was_correct": True, "time_taken": 9.2}
    current_level_3 = "Medium"
    next_level_3 = get_next_difficulty(current_level_3, last_attempt_3)
    print(f"Result: Went from {current_level_3} -> {next_level_3} (Expected: Medium)")
    
    # Scenario 4: Incorrect on "Easy" (Boundary Test)
    # Expect: Stay at "Easy" (can't go lower)
    print("\nScenario 4: Easy, Incorrect")
    last_attempt_4 = {"was_correct": False, "time_taken": 4.0}
    current_level_4 = "Easy"
    next_level_4 = get_next_difficulty(current_level_4, last_attempt_4)
    print(f"Result: Went from {current_level_4} -> {next_level_4} (Expected: Easy)")

    # Scenario 5: Correct and Fast on "Hard" (Boundary Test)
    # Expect: Stay at "Hard" (can't go higher)
    print("\nScenario 5: Hard, Correct, Fast")
    last_attempt_5 = {"was_correct": True, "time_taken": 3.0}
    current_level_5 = "Hard"
    next_level_5 = get_next_difficulty(current_level_5, last_attempt_5)
    print(f"Result: Went from {current_level_5} -> {next_level_5} (Expected: Hard)")