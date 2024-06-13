import os
import sys
# Add the project root to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src.chat import chatter
from src.chat import entity_extractor
from src.chat import json_extractor
from src.chat import entity_checker
from src.recommender import recomendation_selector
from src.recommender import recomender, chatCompletionChecker, nameExtractor


def stchat():
    st.subheader("Spa Cylone", divider="rainbow", anchor=False)
    st.sidebar.title("Output")
    
        # Initialize chat history if not already done
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chatter" not in st.session_state:
        st.session_state.chatter = chatter
    if "entity_extractor" not in st.session_state:
        st.session_state.entity_extractor = entity_extractor

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        avatar = "🤖" if message["role"] == "assistant" else "👨‍💻"
        with st.chat_message(message["role"], avatar=avatar):
            st.write(message["content"])
    
    prompt = st.chat_input("Enter your prompt here...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👨‍💻"):
                st.markdown(prompt)
        response = st.session_state.chatter(user_message=prompt)

        # Add the responses to the chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant", avatar="🤖"):
            st.write(response)

        st.sidebar.markdown('## entity extractor')
        a = st.session_state.entity_extractor(prompt)
        st.sidebar.write(a)
        st.sidebar.markdown('## json extractor')
        b = json_extractor(a)
        st.sidebar.write(b)
        st.sidebar.markdown('## entity checker')
        c = entity_checker(b)
        st.sidebar.write(c)
        st.sidebar.markdown('## recomendation selector')
        d = recomendation_selector(b, c)
        completion = chatCompletionChecker(response)
        st.sidebar.write(d)
        if d != False and completion == True:
            st.sidebar.markdown('## recomender')
            e_id,e_price = recomender(d)
            e_name = nameExtractor(e_id)
            e_list = dict(zip(e_name, e_price))
            st.session_state.messages.append({"role": "assistant", "content": e_list})
            with st.chat_message("assistant", avatar="🤖"):
                st.write(e_list)
            
stchat()
