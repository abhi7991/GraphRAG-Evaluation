# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 13:13:14 2024

@author: abhis
"""


import streamlit as st
import requests
from dotenv import load_dotenv
import os
from datetime import datetime,timedelta
import pandas as pd
from modules import utils
import numpy as np
from openai import OpenAI
# import seaborn as sns
# import matplotlib.pyplot as plt
# import numpy as np

load_dotenv()

def home_page():
    # Set background image
    st.markdown("# MovieMatch")
        
        
def chat_interface_page():
    # Set background image
    # st.markdown(f'<style>body{{background-image: url({page_bg}); background-size: cover;}}</style>', unsafe_allow_html=True)
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    st.markdown("# MovieMatch")
    st.subheader('Your friendly guide to all your queries!🌟')
    st.text('Ask us anything about movies and get tailored recommendations based on your viewing mood!')

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Hey so what do you want to watch?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
            
        response = utils.chat_bot(prompt)   
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.experimental_rerun()     

pages = {
        "Home": home_page,
        "Question? Chat it out": chat_interface_page
    }

# Define the Streamlit app
def main():
    st.set_page_config(
        page_title="MovieMatch",page_icon=":popcorn:" ,layout="wide"
    )

    page = pages['Question? Chat it out']
    page()


if __name__ == "__main__":
    main()                