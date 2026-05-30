
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


def reset_and_rerun():
    """Reset session and trigger a Streamlit rerun from a safe callback."""

    reset_session_state()

    # set a small sentinel to indicate reset completed
    st.session_state["session_just_reset"] = True

    # Note: Do NOT call st.experimental_rerun() here because some
    # Streamlit environments may not expose it and calling it from
    # within certain contexts can raise AttributeError. The button
    # `on_click` will cause Streamlit to rerun automatically after
    # the callback returns, so we simply return from this function.
