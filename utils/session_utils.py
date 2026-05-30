
import streamlit as st



def initialize_session_state():

    defaults = {
        "child_name": "",
        "child_age": 13,
        "guardian_email": "",
        "session_duration_minutes": 20,
        "progress": 0,
        "chat_history": [],
        "current_sentence": "",
        "current_feedback": {},
        "student_paraphrasing_response": "",
        "final_report": "",
        "report_sent": False,
        "session_started": False
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


def reset_session_state():
    """Reset session-specific state while keeping guardian and child info."""

    reset_values = {
        "progress": 0,
        "chat_history": [],
        "current_sentence": "",
        "current_feedback": {},
        "student_paraphrasing_response": "",
        "final_report": "",
        "report_sent": False,
        "session_started": False
    }

    for key, value in reset_values.items():

        st.session_state[key] = value

    if "session_start_time" in st.session_state:
        del st.session_state["session_start_time"]
