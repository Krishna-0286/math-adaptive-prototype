import streamlit as st
from src.puzzle_generator import generate_puzzle
from src.tracker import PerformanceTracker
from src.adaptive_engine import get_next_difficulty, DIFFICULTY_LEVELS

# --- Helper Functions ---

def generate_new_puzzle():
    """Gets a new puzzle and saves it to the session state."""
    q, a = generate_puzzle(st.session_state.current_difficulty)
    
    st.session_state.current_question = q
    st.session_state.current_answer = a
    
    # Start the timer for this puzzle
    st.session_state.tracker.start_puzzle()

def submit_answer(user_answer):
    """
    Called when the user submits an answer.
    It checks, logs, adapts, and generates the next puzzle.
    """
    # 1. Check correctness
    correct_answer = st.session_state.current_answer
    was_correct = (user_answer == correct_answer)

    if was_correct:
        st.success("Correct! Good job.")
    else:
        st.error(f"Not quite. The correct answer was {correct_answer}.")
    
    # 2. Log the attempt (this also stops the timer)
    st.session_state.tracker.log_attempt(
        st.session_state.current_difficulty, 
        was_correct
    )
    
    # 3. Update puzzle count
    st.session_state.puzzle_count += 1
    
    # 4. Get next difficulty (The ADAPTIVE part)
    last_attempt = st.session_state.tracker.performance_log[-1]
    next_diff = get_next_difficulty(
        st.session_state.current_difficulty, 
        last_attempt
    )
    st.session_state.current_difficulty = next_diff
    
    # 5. Generate the next puzzle (if game isn't over)
    if st.session_state.puzzle_count < TOTAL_PUZZLES:
        generate_new_puzzle()
    
# --- 1. Page Configuration & Initialization ---

# Set the page title
st.set_page_config(page_title="Math Adventures", page_icon="🚀")

# Define how many puzzles per session
TOTAL_PUZZLES = 5

# Initialize all our "session state" variables
# This is how Streamlit "remembers" things between button clicks

if 'game_started' not in st.session_state:
    st.session_state.game_started = False

if 'tracker' not in st.session_state:
    st.session_state.tracker = PerformanceTracker()

if 'current_difficulty' not in st.session_state:
    st.session_state.current_difficulty = "Easy"

if 'puzzle_count' not in st.session_state:
    st.session_state.puzzle_count = 0

if 'current_question' not in st.session_state:
    st.session_state.current_question = ""
    st.session_state.current_answer = 0

# --- 2. The Main App UI ---

st.title("🚀 Math Adventures")

# --- UI Flow 1: The Start Screen ---
if not st.session_state.game_started:
    st.subheader("Welcome! Let's get started.")
    
    # Get user's name
    user_name = st.text_input("Enter your name:", "Player")
    
    # Let user choose initial difficulty
    start_difficulty = st.selectbox(
        "Choose your starting difficulty:",
        DIFFICULTY_LEVELS
    )
    
    # Start Game button
    if st.button("Start Game!"):
        # Set all the session state variables to start the game
        st.session_state.game_started = True
        st.session_state.current_difficulty = start_difficulty
        st.session_state.puzzle_count = 0
        st.session_state.tracker = PerformanceTracker() # Reset tracker
        st.session_state.user_name = user_name
        
        # Generate the very first puzzle
        generate_new_puzzle()
        st.rerun() # Rerun the script to show the puzzle UI

# --- UI Flow 2: The Game is Running ---
else:
    
    # --- UI Flow 2a: The Game is Over ---
    if st.session_state.puzzle_count >= TOTAL_PUZZLES:
        st.header(f"Session Over, {st.session_state.user_name}!")
        
        # Show the final summary
        st.code(st.session_state.tracker.get_summary())
        
        # Recommend a starting level for next time
        st.subheader(f"Recommended starting level for next time: {st.session_state.current_difficulty}")
        
        # Play Again button
        if st.button("Play Again?"):
            # Clear all session state to reset the game
            st.session_state.clear()
            st.rerun()

    # --- UI Flow 2b: The Game is In-Progress ---
    else:
        st.header(f"Puzzle {st.session_state.puzzle_count + 1} of {TOTAL_PUZZLES}")
        st.caption(f"Difficulty: {st.session_state.current_difficulty}")
        
        # Display the current puzzle
        st.subheader(st.session_state.current_question)
        
        # Use a "form" so the page only reruns when the button is clicked
        with st.form(key="puzzle_form"):
            
            # Use number_input for the answer
            user_answer = st.number_input(
                "Your answer:", 
                step=1,         # Only allow whole numbers
                format="%d"     # Don't show decimals
            )
            
            # The submit button for the form
            submitted = st.form_submit_button("Submit Answer")
            
            if submitted:
                # This is the main logic!
                submit_answer(user_answer)
                st.rerun()