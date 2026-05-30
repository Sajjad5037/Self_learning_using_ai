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
from utils.session_utils import (
    reset_session_state
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
    

    st.header("🔄 Sentence Paraphrasing")

    st.info(
        "This session will coach the student through paraphrasing with helpful feedback and improvement tips."
    )

    initialize_timer()

    remaining_seconds = get_remaining_seconds()

    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    
    st.info(
        f"Session Time Remaining: {minutes}:{seconds:02d}"
    )
    
    if not has_session_ended():
    
        st_autorefresh(
            interval=60000,
            key="timer_refresh"
        )

    if not st.session_state.current_sentence:

        sentence = generate_paraphrasing_sentence(
            child_age=st.session_state.child_age
        )

        st.session_state.current_sentence = sentence
        st.session_state.current_feedback = {}
        st.session_state.student_paraphrasing_response = ""

    st.subheader("Paraphrase This Sentence")

    st.write(st.session_state.current_sentence)

    with st.form("paraphrasing_form"):

        student_response = st.text_area(
            "Write your paraphrased sentence",
            key="student_paraphrasing_response"
        )
    
        submitted = st.form_submit_button(
            "Submit Response"
        )
    
    feedback = st.session_state.current_feedback or {}

    if submitted:

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

        # If progress reaches 100%, end the session early and generate report
        if st.session_state.progress >= 100:

            if not st.session_state.report_sent:

                report = generate_final_report()

                st.session_state.final_report = report

                # Future email sending
                # send_report_email(report)

                st.session_state.report_sent = True

            st.balloons()

            st.success(
                "Progress reached 100%. Session completed. Great job!"
            )

            st.text_area(
                "Generated Report",
                st.session_state.final_report,
                height=400
            )

            if st.button("Reset session and return to setup"):

                reset_session_state()

                st.rerun()

            st.stop()

        st.session_state.current_feedback = evaluation
        feedback = evaluation

        if evaluation.get("should_try_again"):

            st.warning(
                "The AI coach has suggested a revision. Try again using the guidance shown above."
            )

        else:

            st.success(
                "Great paraphrase! Press Continue to next sentence when you are ready."
            )

    if feedback:

        st.markdown("### 🧠 AI Coach Feedback")

        st.info(
            feedback.get("coach_response", "Here is your feedback.")
        )

        st.write(
            f"Effort Score: {feedback.get('effort_score', 0)}/10"
        )

        st.write(
            f"Engagement Level: {feedback.get('engagement_level', 'unknown')}"
        )

        if feedback.get("improvement_tip"):

            st.write(
                "**Tip:** "
                f"{feedback['improvement_tip']}"
            )

        if feedback.get("suggested_paraphrase"):

            with st.expander("View a stronger paraphrase suggestion"):

                st.write(
                    feedback["suggested_paraphrase"]
                )

        if feedback.get("should_try_again"):

            st.warning(
                "Try again using the tip above to make your paraphrase clearer and more accurate."
            )

        else:

            if st.button(
                "Continue to next sentence",
                key="continue_sentence"
            ):

                next_sentence = generate_paraphrasing_sentence(
                    child_age=st.session_state.child_age
                )

                st.session_state.current_sentence = next_sentence
                st.session_state.current_feedback = {}
                st.session_state.student_paraphrasing_response = ""
                st.rerun()

    if has_session_ended():

        st.warning(
            "Session completed."
        )
    
        if not st.session_state.report_sent:
    
            report = generate_final_report()
    
            st.session_state.final_report = report
    
            # Future email sending
            # send_report_email(report)
    
            st.session_state.report_sent = True
    
        st.balloons()

        st.success(
            "Session report generated successfully. Great work!"
        )

        st.text_area(
            "Generated Report",
            st.session_state.final_report,
            height=400
        )

        if st.button("Reset session and return to setup"):

            reset_session_state()

            st.rerun()

        st.stop()
