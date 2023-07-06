## Chat functions for the app
import requests
from langchain.memory import ChatMessageHistory
from langchain.schema import messages_to_dict
import openai
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


# Set the API key
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG")


# Define a ChatMessage class to handle formatting the messages
class ChatMessage:
    def __init__(self, role, content):
        self.role = role
        self.content = content


# Define a class to handle the chatbot using OpenAI and langchain
class ChatService:
    # Initialize the chatbot with the initial message depending on the context
    def __init__(self, teacher: str, topic: str, age: str, kid_name: str):
        # Initialize the chat history
        self.chat_history = ChatMessageHistory()
        # Initialize the chat history dictionary
        self.chat_history_dict = {}
        # Initialize the initial message
        self.initial_system_message = {}
        # Initialize the teacher selecteds
        self.teacher = teacher
        # Initialize the topic selected
        self.topic = topic
        # Initialize the age of the student
        self.age = age
        # Initialize the name of the student
        self.kid_name = kid_name
        # Initialize the initial messages
        self.initial_messages = []
        # Initialize the chat_messages
        self.chat_messages = []
      
    
    # Save the chat_history to a dictionary
    def save_chat_history_dict(self):
        self.chat_history_dict = messages_to_dict(self.chat_history.messages)
        return self.chat_history_dict
    
    def add_user_response(self, response: str):
        self.chat_history.add_user_message(response)
        # Return the latest message in the chat history
        chat_messages =  self.save_chat_history_dict()
        # Get the latest message
        latest_message = chat_messages[-1]
        # Convert the response to a Message object
        formatted_message = ChatMessage(role = "user", content = latest_message[0]['data']['content'])
        # Append the message to the chat history
        st.session_state.chat_service.chat_messages.append({"role": formatted_message.role, "content": formatted_message.content})
        # Return the chat history
        return st.session_state.chat_service.chat_messages
        

    def add_teacher_message(self, message: str):
        self.chat_history.add_ai_message(message)
        # Return the latest message in the chat history
        chat_messages =  self.save_chat_history_dict()
        # Get the latest message
        latest_message = chat_messages[-1]
        # Convert the response to a Message object
        formatted_message = ChatMessage(role = "ai", content = latest_message[0]['data']['content'])
        # Append the message to the chat history
        self.chat_messages.append({"role": formatted_message.role, "content": formatted_message.content})
        # Return the chat history
        return self.chat_messages
    
    def add_user_message(self, message):
        response = requests.post(f"{self.baseUrl}/add_user_message", params={"message": message})
        data = response.json()
        # Convert the response to a Message object
        message = ChatMessage(role = "user", content = data[0]['data']['content'])

        # Append the message to the chat history
        self.chat_messages.append({"role": message.role, "content": message.content})

        # Return the chat history
        return self.chat_messages
    
    
    # Define the function to get the initial message from the teacher.  This will be the first message to initiate
    # the socratic method conversation with the student based on the topic and age
    def get_initial_message_from_teacher(self):
        # Define the messages to pass to the OpenAI API
        messages = [
            {
                "role": "system",
                "content": f"You are a teacher that is helping a child learn about different topics based on the socratic method.\
                    You have taken on the personality of {self.teacher} from the kids show 'Paw Patrol'.  The child's name is {self.kid_name}.\
                    The topic you are teaching is {self.topic}.  The age of the child is {self.age}.  The format of the conversation is question / response,\
                    where you ask a question and the child gives a response.  Please give the first question to the child to start the conversation."
            },
        ]
           # Use the OpenAI API to generate a recipe
        try:
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=messages,
            max_tokens=750,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            temperature=1,
            top_p=0.9,
            n=1,
        )
            response = response.choices[0].message.content

        except (requests.exceptions.RequestException, openai.error.APIError):
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            max_tokens=750,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            temperature=1,
            top_p=0.9,
            n=1,
        )

            response = response.choices[0].message.content
    
        return response

        
    # Define a function to initialize the chatbot with an initial message
    def initialize_chat(self):
        initial_system_message = {"role": "system", 
                                "content": f"You are a helpful and kind teacher helping a child of age {self.age} learn about a topic\
                                {self.topic} via the Socratic method.  You are taking on the personality of the kids show 'Paw Patrol'\
                                character {self.teacher}.  The child's name is {self.kid_name}.  The chat will be question and answer,\
                                where you will ask a question and the child will respond."}
        # Add the initial message to the chat history
        self.chat_messages.append(initial_system_message)
        self.initial_system_message = initial_system_message

        # Get the initial message from the teacher
        initial_message_from_teacher = self.get_initial_message_from_teacher()
        # Add the initial message from the teacher to the chat history
        self.chat_messages.append({"role": "ai", "content": initial_message_from_teacher})
        self.chat_history.add_ai_message(initial_message_from_teacher)
        self.chat_history_dict = self.save_chat_history_dict()
        # Return the chat history
        return self.chat_history_dict
        
        

    # Define the function to get the answer from the teacher
    def get_answer_from_teacher(self, response: str):                
        messages = [
            {
                "role": "system",
                "content": f"You are a teacher that is helping a child learn about different topics based on the socratic method.\
                    You have taken on the personality of {self.teacher} from the kids show 'Paw Patrol'.  The child's name is {self.kid_name}.\
                    The topic you are teaching is {self.topic}.  The age of the child is {self.age}.  The format of the conversation is question / response,\
                    where you ask a question and the child gives a response.\
                    Your chat history so far is {self.chat_messages}.  Please ask the next question based on the child's response {response}."
            },
            {
                "role": "user",
                "content": f"{response}"
            },
        ]

        # Use the OpenAI API to generate a question based on the child's response
        try:
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=messages,
            max_tokens=750,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            temperature=1,
            top_p=0.9,
            n=1,
        )
            question = response.choices[0].message.content
            # Add the child's response to the chat history
            self.chat_history.add_user_message(response)

            # Add the question to the chat history
            self.chat_history.add_ai_message(question)
            self.chat_history_dict = self.save_chat_history_dict()



        except (requests.exceptions.RequestException, openai.error.APIError):
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            max_tokens=750,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            temperature=1,
            top_p=0.9,
            n=1,
        )

            question = response.choices[0].message.content
            # Add the child's response to the chat history
            self.chat_history.add_user_message(response)

            # Add the question to the chat history
            self.chat_history.add_ai_message(question)
            self.chat_history_dict = self.save_chat_history_dict()
    
        return self.chat_messages

    # Define a function to clear the chat history
    def clear_chat_history(self):
        self.chat_history.clear()
        self.chat_history_dict = {}
        self.chat_messages = []

        
# Define the session variables
session_vars = [
        'chat_session',
    ]
default_values = [
        ChatService(),
    ]

# Loop through the session variables and set them if they are not already set
for session_var, default_value in zip(session_vars, default_values):
    if session_var not in st.session_state:
        st.session_state[session_var] = default_value
