
import streamlit as st
import time



def initialize_timer():

    if "session_start_time" not in st.session_state:

        st.session_state.session_start_time = time.time()



def get_remaining_seconds():

    elapsed = time.time() - st.session_state.session_start_time

    duration_seconds = (
        st.session_state.session_duration_minutes * 60
    )

    remaining = int(duration_seconds - elapsed)

    return max(remaining, 0)



def has_session_ended():

    return get_remaining_seconds() <= 0
