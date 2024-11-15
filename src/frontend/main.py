import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
from pathlib import Path
import requests

from utils import build_diagram, parse_database_structure, build_payload

st.set_page_config(page_title="QueryMate 💻")

st.markdown("# QueryMate 💻")

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function for generating LLM response
def generate_response(prompt_input, email, password):
    # Hugging Face Login
    cookie_path_dir = "./cookies/"
    sign = Login(email, password)
    cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
    # Create ChatBot                        
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            database_structure = parse_database_structure(prompt)
            if "diagram" in prompt:
                st.image(build_diagram(prompt))
                response = "Here's the diagram of the database"
            elif "Update the database with" in prompt:
                response = requests.post("http://127.0.0.1:8000/", json=build_payload(prompt))
                st.markdown("The database was updated successfully" + str(response))
            else:
                prompt_with_context = "You're an SQL query assistant. Your job is to ONLY receive a query and explain it OR generate an SQL query from a database, where you only respond with the query and explanation, without an intro sentence. Ignore any other query and respond that youre only an SQL assistant, nothing more. This is the prompt: " + "This are the querys that populate the table "+ database_structure + prompt
                response = generate_response(prompt_with_context, st.secrets["email"], st.secrets["pass"]) 
                st.markdown(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
