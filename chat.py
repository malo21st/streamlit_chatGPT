import streamlit as st
from streamlit_chat import message
import openai

st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)

openai.api_key = st.secrets['api_key']

st.header("Streamlit-chat & chatGPT - Demo")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""

def answer(question):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        temperature=0,
        max_tokens=200,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    return response["choices"][0]["text"].split("\n")[-1]

def input_and_clear():
    st.session_state['user_input'] = st.session_state['input']
    st.session_state['input'] = ""

st.text_input("Input message :", key="input", on_change=input_and_clear)

if st.session_state['user_input']:
    output = answer(st.session_state['user_input'])

    st.session_state.past.append(st.session_state['user_input'])
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
