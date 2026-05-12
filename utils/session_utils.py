
import streamlit as st



def initialize_session_state():

    defaults = {
        "child_name": "",
        "child_age": 13,
        "guardian_email": "",
        "session_duration_minutes": 20,
        "progress": 0,
        "chat_history": [],
        "current_sentence": ""
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value
