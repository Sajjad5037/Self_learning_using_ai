import streamlit as st
from streamlit_autorefresh import st_autorefresh

from services.ai_service import (
    generate_paraphrasing_sentence,
    evaluate_paraphrasing_response
)

from services.progress_service import (
    update_progress
)

from services.report_service import (
    generate_final_report,
    send_report_email
)

from utils.timer_utils import (
    initialize_timer,
    get_remaining_seconds,
    has_session_ended
)


def render_paraphrasing_tab():
    if not st.session_state.child_name:

        st.warning(
            "Please complete guardian setup first."
        )
    
        return
    
    if not st.session_state.guardian_email:
    
        st.warning(
            "Please enter guardian email."
        )
    
        return
    st_autorefresh(interval=1000, key="timer_refresh")

    st.header("🔄 Sentence Paraphrasing")

    initialize_timer()

    remaining_seconds = get_remaining_seconds()

    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    st.info(
        f"Session Time Remaining: {minutes}:{seconds:02d}"
    )

    if not st.session_state.current_sentence:

        sentence = generate_paraphrasing_sentence(
            child_age=st.session_state.child_age
        )

        st.session_state.current_sentence = sentence

    st.subheader("Paraphrase This Sentence")

    st.write(st.session_state.current_sentence)

    student_response = st.text_area(
        "Write your paraphrased sentence",
        key="student_paraphrasing_response"
    )

    if st.button("Submit Response"):

        if not student_response.strip():

            st.warning(
                "Please enter a response."
            )

            return

        evaluation = evaluate_paraphrasing_response(
            original_sentence=st.session_state.current_sentence,
            student_response=student_response,
            child_age=st.session_state.child_age
        )

        st.session_state.chat_history.append({

            "original_sentence":
            st.session_state.current_sentence,

            "student_response":
            student_response,

            "evaluation":
            evaluation
        })

        update_progress(
            evaluation["progress_increment"]
        )

        st.success(
            evaluation["coach_response"]
        )

        st.write(
            f"Effort Score: "
            f"{evaluation['effort_score']}/10"
        )

        st.write(
            f"Engagement Level: "
            f"{evaluation['engagement_level']}"
        )

        next_sentence = generate_paraphrasing_sentence(
            child_age=st.session_state.child_age
        )

        st.session_state.current_sentence = next_sentence

        st.rerun()

    if has_session_ended():

        st.warning(
            "Session completed."
        )

        report = generate_final_report()

        send_report_email(report)

        st.success(
            "Guardian report sent successfully."
        )

        st.text_area(
            "Generated Report",
            report,
            height=400
        )
