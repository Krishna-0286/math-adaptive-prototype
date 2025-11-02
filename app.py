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
    
    # 2. Log the attempt 
    st.session_state.tracker.log_attempt(
        st.session_state.current_difficulty, 
        was_correct
    )
    
    # 3. Update puzzle count
    st.session_state.puzzle_count += 1
    
    # 4. Get next difficulty 
    last_attempt = st.session_state.tracker.performance_log[-1]
    next_diff = get_next_difficulty(
        st.session_state.current_difficulty, 
        last_attempt
    )
    st.session_state.current_difficulty = next_diff
    
    # 5. Generate the next puzzle 
    if st.session_state.puzzle_count < TOTAL_PUZZLES:
        generate_new_puzzle()
    


 
st.set_page_config(page_title="Math Adventures", page_icon="🚀")


TOTAL_PUZZLES = 5

 

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

#2. The Main App 

st.title("🚀 Math Adventures")

#  1: The Start Screen 
if not st.session_state.game_started:
    st.subheader("Welcome! Let's get started.")
    
    # Get user's name
    user_name = st.text_input("Enter your name:", "Player")
    
    
    start_difficulty = st.selectbox(
        "Choose your starting difficulty:",
        DIFFICULTY_LEVELS
    )
    
    # Start Game button
    if st.button("Start Game!"):
    
        st.session_state.game_started = True
        st.session_state.current_difficulty = start_difficulty
        st.session_state.puzzle_count = 0
        st.session_state.tracker = PerformanceTracker() #
        st.session_state.user_name = user_name
        
        
        generate_new_puzzle()
        st.rerun() 

#2: The Game is Running ---
else:
    
    
    if st.session_state.puzzle_count >= TOTAL_PUZZLES:
        st.header(f"Session Over, {st.session_state.user_name}!")
        
        
        st.code(st.session_state.tracker.get_summary())
        
        
        st.subheader(f"Recommended starting level for next time: {st.session_state.current_difficulty}")
        
        
        if st.button("Play Again?"):
            
            st.session_state.clear()
            st.rerun()
     
    else:
        st.header(f"Puzzle {st.session_state.puzzle_count + 1} of {TOTAL_PUZZLES}")
        st.caption(f"Difficulty: {st.session_state.current_difficulty}")
        
    
        st.subheader(st.session_state.current_question)
        
        
        with st.form(key="puzzle_form"):
            
            
            user_answer = st.number_input(
                "Your answer:", 
                step=1,         
                format="%d"    
            )
            
        
            submitted = st.form_submit_button("Submit Answer")
            
            if submitted:
                
                submit_answer(user_answer)
                st.rerun()