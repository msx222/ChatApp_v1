import streamlit as st
from streamlit_chat_prompt import prompt

response = prompt(name="test", key="test")
st.write(response)