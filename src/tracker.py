# We need the 'time' module to track start and end times
import time

class PerformanceTracker:
    """
    A class to track performance metrics for each puzzle.
    It logs correctness, response time, and difficulty.
    """
    
    def __init__(self):
        # This list will store all our results.
        # Each result will be a dictionary, e.g.:
        # {'correct': True, 'time_taken': 3.4, 'difficulty': 'Easy'}
        self.performance_log = []
        self.puzzle_start_time = None

    def start_puzzle(self):
        """Records the exact time a puzzle is shown."""
        # time.time() gives the current time in seconds
        self.puzzle_start_time = time.time()

    def log_attempt(self, difficulty, was_correct):
        """
        Logs the result of a single puzzle attempt.
        Calculates time_taken since start_puzzle() was called.
        """
        # Calculate how much time has passed
        end_time = time.time()
        time_taken = end_time - self.puzzle_start_time
        
        # Create a dictionary to hold this attempt's data
        attempt_data = {
            "difficulty": difficulty,
            "was_correct": was_correct,
            "time_taken": time_taken
        }
        
        # Add this attempt to our main log
        self.performance_log.append(attempt_data)
        print(f"-> Logged: Correct={was_correct}, Time={time_taken:.2f}s")

    def get_summary(self):
        """
        Calculates and returns a summary of the entire session.
        """
        if not self.performance_log:
            return "No attempts were logged."

        total_puzzles = len(self.performance_log)
        total_correct = 0
        total_time = 0
        
        # Loop through every attempt in our log
        for attempt in self.performance_log:
            if attempt["was_correct"]:
                total_correct += 1  # Add 1 if they were right
            total_time += attempt["time_taken"] # Add the time taken
            
        # Calculate averages
        accuracy = (total_correct / total_puzzles) * 100
        avg_time = total_time / total_puzzles
        
        summary_report = f"""
        --- Session Summary ---
        Total Puzzles: {total_puzzles}
        Correct Answers: {total_correct}
        Accuracy: {accuracy:.2f}%
        Average Time: {avg_time:.2f} seconds per puzzle
        ---------------------
        """
        return summary_report

# -----------------------------------------------------------------
# This is our test block again.
# -----------------------------------------------------------------
if __name__ == "__main__":
    print("--- Testing Performance Tracker ---")
    
    # 1. Create a new tracker object from our class blueprint
    tracker = PerformanceTracker()
    
    # 2. Test 1: A fast, correct "Easy" puzzle
    tracker.start_puzzle()
    time.sleep(1.5) # Pretend the user is "thinking" for 1.5 seconds
    tracker.log_attempt("Easy", True)
    
    # 3. Test 2: A slow, incorrect "Medium" puzzle
    tracker.start_puzzle()
    time.sleep(3.0) # Pretend the user is "thinking" for 3 seconds
    tracker.log_attempt("Medium", False)
    
    # 4. Test 3: A fast, correct "Hard" puzzle
    tracker.start_puzzle()
    time.sleep(2.1) # Pretend the user is "thinking" for 2.1 seconds
    tracker.log_attempt("Hard", True)
    
    # 5. Get the final summary
    summary = tracker.get_summary()
    print(summary)