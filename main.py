## An app to help kids learn about various topics using the socratic method with an LLM.  The teacher
# will take the form of a  "Paw Patrol" character.  The first thing we will do is take in the user name
# and then the age, and then from there the user will choose a topic to learn about and initiate the chat.

## Initial Imports
import streamlit as st
from PIL import Image
from utils.chat_utils import ChatService

# Establish the initial session state
# Create a function to initialize the session state variables
def init_session_variables():
    # Initialize session state variables
    session_vars = [
        'home_page', 'user_name', 'user_age', 'topic', 'teacher', 'chat_history', 'chat_service'
    ]
    default_values = [
        'get_user_info', '', '', '', '', [], ChatService()
    ]

    # Loop through the session variables and set them if they are not already set
    for session_var, default_value in zip(session_vars, default_values):
        if session_var not in st.session_state:
            st.session_state[session_var] = default_value

init_session_variables
# Define a function to get the user information
def get_user_info():
    # Get the user name via a text input
    st.session_state.user_name = st.text_input("What is your name?")
    # Get the user age via a text input
    st.session_state.user_age = st.text_input("What is your age?")
    # Change the page state to get the topic and teacher selections
    st.session_state.home_page = 'get_topic_and_teacher'
    # Reset the script
    st.experimental_rerun()

# Define a function to get the topic and teacher selections
def get_topic_and_teacher():
    # Greet the user by name
    st.write(f"Hi {st.session_state.user_name}!")
    st.markdown("Which teacher would you like to choose today?")
    # Ask the user which teacher they would like to choose -- we will use two columns to display the teacher pics and buttons to choose them with
    col1, col2 = st.columns(2)
    # Define the teacher images 
    teacher_images = {
        "Chase" : Image.open("resources/chase1.jpg"),
        "Leo" : Image.open("resources/leo1.jpg"),
    }
    # Col1 will be Chase
    with col1:
        st.image(teacher_images["Chase"])
        if st.button("Chase"):
            st.session_state.teacher = "Chase"
       