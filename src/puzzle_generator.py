# We need the 'random' module to pick random numbers
import random

def generate_puzzle(difficulty_level):
    """
    Generates a math puzzle based on the difficulty level.
    
    Args:
        difficulty_level (str): "Easy", "Medium", or "Hard"

    Returns:
        tuple: A (question, answer) tuple.
               e.g., ("5 + 3 = ?", 8)
    """
    
    if difficulty_level == "Easy":
        # Easy: Addition of two small numbers (1 to 9)
        num1 = random.randint(1, 9)
        num2 = random.randint(1, 9)
        question = f"What is {num1} + {num2}?"
        answer = num1 + num2
        
    elif difficulty_level == "Medium":
        # Medium: Addition or Subtraction with larger numbers (10 to 50)
        num1 = random.randint(10, 50)
        num2 = random.randint(10, 50)
        
        # Make sure the answer to subtraction isn't a negative number
        # This is good practice for a kids' game
        if num1 < num2:
            num1, num2 = num2, num1  # Swap the numbers
        
        question = f"What is {num1} - {num2}?"
        answer = num1 - num2
        
    elif difficulty_level == "Hard":
        # Hard: Multiplication (2 to 12)
        num1 = random.randint(2, 12)
        num2 = random.randint(2, 12)
        question = f"What is {num1} x {num2}?"
        answer = num1 * num2
        
    return question, answer

# -----------------------------------------------------------------
# This special block of code only runs when you execute this file 
# directly. It's a great way to test your file in isolation.
# We will remove this test code later on.
# -----------------------------------------------------------------
if __name__ == "__main__":
    print("--- Testing Puzzle Generator ---")
    
    # Test Easy
    easy_q, easy_a = generate_puzzle("Easy")
    print(f"Easy Puzzle:   {easy_q} | Answer: {easy_a}")
    
    # Test Medium
    med_q, med_a = generate_puzzle("Medium")
    print(f"Medium Puzzle: {med_q} | Answer: {med_a}")
    
    # Test Hard
    hard_q, hard_a = generate_puzzle("Hard")
    print(f"Hard Puzzle:  {hard_q} | Answer: {hard_a}")