# original: https://github.com/AI-Yash/st-chat/blob/main/examples/chatbot.py
import streamlit as st
from streamlit_chat import message
import openai
from PIL import Image

openai.api_key = st.secrets['api_key']

st.set_page_config(
    page_title = "GPT-3 chatbot",
    page_icon = Image.open("favicon.png")
)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""
    
if 'prompt_text' not in st.session_state:
    st.session_state['prompt_text'] = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\n"

def answer_ChatGPT(question):
    st.session_state['prompt_text'] += f"Human: {question}\nAI:"
    response = openai.Completion.create(
        model="text-davinci-003",
#         model="gpt-3.5-turbo-0301",
        prompt=question,
        temperature=0.9,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    response_text = response.choices[0].text
    st.session_state['prompt_text'] += f" {response_text}\n"
    return response_text

def input_and_clear():
    st.session_state['user_input'] = st.session_state['input']
    st.session_state['input'] = ""

# layout
st.header("streamlit-chat & GPT-3 - Chatbot Demo")
st.text_input("**input message :**", key="input", on_change=input_and_clear)

if st.session_state['user_input']:
    output = answer_ChatGPT(st.session_state['user_input'])
    st.session_state.past.append(st.session_state['user_input'])
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], seed=86, key=str(i))
        message(st.session_state['past'][i], is_user=True, 
                avatar_style='big-ears-neutral', seed=635, key=str(i) + '_user')
