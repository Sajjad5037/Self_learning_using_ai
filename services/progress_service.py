
import streamlit as st



def update_progress(progress_increment):

    st.session_state.progress += progress_increment

    if st.session_state.progress > 100:
        st.session_state.progress = 100
