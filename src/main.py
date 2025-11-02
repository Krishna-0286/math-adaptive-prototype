# Import the code from our other files
from src.puzzle_generator import generate_puzzle
from src.tracker import PerformanceTracker
from src.adaptive_engine import get_next_difficulty

# --- 1. SETUP THE GAME ---

def main():
    """
    Main function to run the adaptive math game.
    """
    print("========================================")
    print("   Welcome to Math Adventures!")
    print("========================================")
    
    # Get user's name
    user_name = input("Enter your name to begin: ")
    print(f"\nHello, {user_name}! Let's get started.")

    # Let user choose initial difficulty
    print("Choose your starting difficulty:")
    print("  1: Easy")
    print("  2: Medium")
    print("  3: Hard")
    
    difficulty_map = {"1": "Easy", "2": "Medium", "3": "Hard"}
    
    # Loop until they give a valid choice (1, 2, or 3)
    while True:
        choice = input("Enter choice (1, 2, or 3): ")
        if choice in difficulty_map:
            current_difficulty = difficulty_map[choice]
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    # Create a new tracker object for this session
    tracker = PerformanceTracker()
    
    # Define how many puzzles to show in the session
    TOTAL_PUZZLES = 5
    print(f"\nGreat! We will do {TOTAL_PUZZLES} puzzles.")
    print("----------------------------------------")

    # --- 2. START THE MAIN GAME LOOP ---
    
    for i in range(TOTAL_PUZZLES):
        print(f"\n--- Puzzle {i + 1} of {TOTAL_PUZZLES} ---")
        
        # 1. Get a puzzle
        question, correct_answer = generate_puzzle(current_difficulty)
        
        # 2. Start timer and show puzzle
        print(f"Difficulty: {current_difficulty}")
        print(f"Question: {question}")
        
        tracker.start_puzzle() # Start the timer
        
        # 3. Get user's answer
        while True:
            try:
                # Get input and try to convert it to an integer
                user_answer = int(input("Your answer: "))
                break # Exit the loop if conversion is successful
            except ValueError:
                # This 'except' block catches the error if they type "ten"
                print("Invalid input. Please enter a number.")
        
        # 4. Check correctness and log it
        if user_answer == correct_answer:
            print("Correct! Good job.")
            was_correct = True
        else:
            print(f"Not quite. The correct answer was {correct_answer}.")
            was_correct = False
            
        tracker.log_attempt(current_difficulty, was_correct)
        
        # 5. Get the next difficulty level (The ADAPTIVE part!)
        # We only adapt if it's not the very last puzzle
        if i < TOTAL_PUZZLES - 1:
            # Get the log of the attempt we just finished
            last_attempt = tracker.performance_log[-1] 
            
            # Ask the "brain" what to do next
            current_difficulty = get_next_difficulty(current_difficulty, last_attempt)

    # --- 3. END OF SESSION ---
    
    print("\n========================================")
    print("         Session Over!")
    print("========================================")
    
    # Show the final summary from the tracker
    print(tracker.get_summary())
    
    # Recommend a starting level for next time
    print(f"Recommended starting level for next time: {current_difficulty}")


# This is the standard Python way to run the 'main' function
# when the script is executed.
if __name__ == "__main__":
    main()