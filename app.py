import streamlit as st
from tabs.paraphrasing_tab import render_paraphrasing_tab
from tabs.creative_tab import render_creative_tab
from tabs.reading_tab import render_reading_tab
from utils.session_utils import initialize_session_state

st.set_page_config(
    page_title="AI Learning Coach",
    page_icon="📘",
    layout="wide"
)

initialize_session_state()

st.title("📘 AI Learning Coach")
st.caption("AI-assisted learning sessions for children")

with st.sidebar:

    st.header("Guardian Setup")

    st.session_state.child_name = st.text_input(
        "Child Name",
        value=st.session_state.child_name
    )

    st.session_state.child_age = st.number_input(
        "Child Age",
        min_value=5,
        max_value=18,
        value=st.session_state.child_age
    )

    st.session_state.guardian_email = st.text_input(
        "Guardian Email",
        value=st.session_state.guardian_email
    )

    st.session_state.session_duration_minutes = st.selectbox(
        "Session Duration",
        [2,10, 15, 20, 30],
        index=2
    )
    if st.button("Start Session"):

        if not st.session_state.child_name:
    
            st.warning(
                "Please enter child name."
            )
    
        elif not st.session_state.guardian_email:
    
            st.warning(
                "Please enter guardian email."
            )
    
        else:
    
            st.session_state.session_started = True
    
            st.session_state.progress = 0
    
            st.session_state.chat_history = []
    
            st.session_state.current_sentence = ""
    
            if "session_start_time" in st.session_state:
                del st.session_state["session_start_time"]
    
            st.rerun()

    st.divider()

    st.subheader("Session Progress")

    st.progress(
        st.session_state.progress / 100
    )

    st.write(f"Progress: {st.session_state.progress}%")

tab1, tab2, tab3 = st.tabs([
    "Sentence Paraphrasing",
    "Creative Writing",
    "Reading Comprehension"
])

with tab1:
    render_paraphrasing_tab()

with tab2:
    render_creative_tab()

with tab3:
    render_reading_tab()
