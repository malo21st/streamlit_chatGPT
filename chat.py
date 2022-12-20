import streamlit as st
from streamlit_chat import message
import openai

st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)

openai.api_key = st.secrets['api_key']

st.header("Streamlit & chatGPT - Demo")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

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

def get_text():
    input_text = st.text_input("あなた: ", key="input")
    return input_text 

user_input = get_text()

if user_input:
    output = answer(user_input)

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    if 'input' in st.session_state:
        st.session_state["input"] = ""
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
