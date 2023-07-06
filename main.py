## An app to help kids learn about various topics using the socratic method with an LLM.  The teacher
# will take the form of a  "Paw Patrol" character.  The first thing we will do is take in the user name
# and then the age, and then from there the user will choose a topic to learn about and initiate the chat.

## Initial Imports
import streamlit as st
from PIL import Image
from utils.chat_utils import ChatService
from streamlit_chat import message
import asyncio

# Establish the initial session state
# Create a function to initialize the session state variables
def init_session_variables():
    # Initialize session state variables
    session_vars = [
        'home_page', 'user_name', 'user_age', 'topic', 'teacher', 'chat_messages', 'chat_service', 'initial_question', 'i', 'difficulty_score', 'is_correct', 'total_score'
    ]
    default_values = [
        'get_user_info', '', '', '', '', [], ChatService(), '', 0, 0, False, 0
    ]

    # Loop through the session variables and set them if they are not already set
    for session_var, default_value in zip(session_vars, default_values):
        if session_var not in st.session_state:
            st.session_state[session_var] = default_value

# Define a function to get the user information
def get_user_info():
    # Display an image of the Paw Patrol characters
    st.image(Image.open("resources/paw_patrol1.jpg"))
    st.markdown("##### Welcome to paw patrol school!  Let's get started!")
    st.text("")
    # Get the user name via a text input
    st.session_state.user_name = st.selectbox("Who is learning today?", ["Archie", "LuAnna"])
    # Get the user age via a text input
    #st.session_state.user_age = st.text_input("What is your age?")
    # Create a button to submit the user info
    initial_info_button = st.button("Submit", type='primary', use_container_width=True)
    # If the user clicks the button, change the page state to get the topic and teacher selections
    if initial_info_button:
        if st.session_state.user_name == "Archie":
            st.session_state.user_age = 4
        else:
            st.session_state.user_age = 6
        st.session_state.home_page = 'get_topic_and_teacher'
        # Reset the script
        st.experimental_rerun()

# Define a function to get the topic and teacher selections
def get_topic_and_teacher():
    # Greet the user by name
    st.markdown(f"**Hi {st.session_state.user_name}!  What would you like to learn about today?**")
    # Get the topic selection from the user
    topic = st.text_input("Enter a topic:")
    # Get the teacher selection from the user
    st.markdown("**Which teacher would you like to choose today?**")
    st.text("")
    # Ask the user which teacher they would like to choose -- we will use two columns to display the teacher pics and buttons to choose them with
    col1, col2 = st.columns(2, gap="large")
    # Define the teacher images 
    teacher_images = {
        "Chase" : Image.open("resources/chase1.jpg"),
        "Leo" : Image.open("resources/leo1.jpg"),
    }
    # Col1 will be Chase
    with col1:
        st.image(teacher_images["Chase"])
        if st.button("Chase", type='primary', use_container_width=True):
            st.session_state.chat_service.teacher = "Chase"
            st.session_state.chat_service.topic = topic
            st.session_state.chat_service.age = st.session_state.user_age
            st.session_state.chat_service.kid_name = st.session_state.user_name
            st.session_state.chat_service.get_initial_message_from_teacher()
            st.session_state.home_page = 'chat_session'
            st.experimental_rerun()

    # Col2 will be Leo
    with col2:
        st.image(teacher_images["Leo"])
        if st.button("Leo", type='primary', use_container_width=True):
            st.session_state.chat_service.teacher = "Leo"
            st.session_state.chat_service.topic = topic
            st.session_state.chat_service.age = st.session_state.user_age
            st.session_state.chat_service.kid_name = st.session_state.user_name
            st.session_state.chat_service.get_initial_message_from_teacher()
            st.session_state.home_page = 'chat_session'
            st.experimental_rerun()

# Define a function to display the chat message
def display_chat_message(chat_message, index):
    if chat_message['role'] == 'user':
        message(chat_message['content'], avatar_style="initials", seed="U", is_user=True, key = f"chat_message_{index}")
    elif chat_message['role'] == 'ai':
        message(chat_message['content'], avatar_style="initials", seed="SC", key = f"chat_message_{index}")

# Define a function to handle the user's input
def handle_user_input():
    # Create a text input for the user to enter their response
    user_response = st.text_input("Enter your response:")
    # Create a button to submit the user response
    submit_response_button = st.button("Submit")
    # If the user clicks the button, get the response from the user and send it to the chat service
    if submit_response_button:
        with st.spinner(f'{st.session_state.chat_service.teacher} is thinking...'):
            st.session_state.chat_service.get_answer_from_teacher(user_response)
            st.experimental_rerun()

# Define a function to run the chat session
def chat_session():
    # Create two columns -- one to display the teacher's image and one to display the chat messages
    col1, col2 = st.columns([1, 2.5], gap='large')
    # Col1 will be the teacher's image -- we need to check if the teacher is Chase or Leo
    with col1:
        if st.session_state.chat_service.teacher == "Chase":
            st.image(Image.open("resources/chase1.jpg"))
        elif st.session_state.chat_service.teacher == "Leo":
            st.image(Image.open("resources/leo1.jpg"))
    # Col2 will be the chat messages
    with col2:
        # Only display the last message
        last_message = st.session_state.chat_messages[-1]
        last_index = len(st.session_state.chat_messages) - 1
        display_chat_message(last_message, last_index)
        handle_user_input()


    #if st.session_state.is_correct == True:
    #        st.markdown(f'##### Congratulations, {st.session_state.chat_service.kid_name}🎉!  You earned {st.session_state.difficulty_score} points for that\
    #            correct answer!  Your total score is {st.session_state.total_score} points. Keep up the good work!  🤩')

    



# Define the flow of the app
def main():
    init_session_variables()

    if st.session_state.home_page == 'get_user_info':
        get_user_info()
    elif st.session_state.home_page == 'get_topic_and_teacher':
        get_topic_and_teacher()
    elif st.session_state.home_page == 'chat_session':
        chat_session()

# Run the app
if __name__ == "__main__":
    main()
       