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
    st.session_state['prompt_text'] = [{"role": "system", "content": "You are a helpful assistant."}]

def answer_GPT3(question):
    st.session_state['prompt_text'] += {"role": "user", "content": question}
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state['prompt_text'],
        temperature=0.9,
    )
    response_json = response.choices[0]['message']
    st.session_state['prompt_text'] += {"role": "assistant", "content": response_json['content']}
    return response_json['content']

def input_and_clear():
    st.session_state['user_input'] = st.session_state['input']
    st.session_state['input'] = ""

# layout
st.header("streamlit-chat & GPT-3 - Chatbot Demo")
st.text_input("**input message :**", key="input", on_change=input_and_clear)

if st.session_state['user_input']:
    output = answer_GPT3(st.session_state['user_input'])
    st.session_state.past.append(st.session_state['user_input'])
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], seed=86, key=str(i))
        message(st.session_state['past'][i], is_user=True, 
                avatar_style='big-ears-neutral', seed=635, key=str(i) + '_user')
