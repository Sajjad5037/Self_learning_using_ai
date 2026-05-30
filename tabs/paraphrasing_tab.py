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
    reset_session_state,
    reset_and_rerun
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
        # Compute a safe progress increment. Prefer model-provided
        # `progress_increment`, but fall back to a value derived from
        # `effort_score` when missing or invalid.
        progress_inc = evaluation.get("progress_increment")

        if not isinstance(progress_inc, int) or progress_inc <= 0:

            effort = evaluation.get("effort_score")

            try:
                effort_val = int(effort)
            except Exception:
                effort_val = 5

            # Map effort (0-10) to progress (5-20) as a fallback
            progress_inc = max(5, min(20, effort_val * 2))

            evaluation["progress_increment"] = progress_inc

        update_progress(progress_inc)

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

            st.button("Reset session and return to setup", on_click=reset_and_rerun)

            st.stop()

        # Save feedback and decide whether to auto-advance.
        st.session_state.current_feedback = evaluation
        feedback = evaluation

        if evaluation.get("should_try_again"):

            st.warning(
                "The AI coach has suggested a revision. Try again using the guidance shown above."
            )

        else:

            st.success(
                "Great paraphrase! Loading next sentence..."
            )

            # Auto-advance to the next sentence so the student can continue.
            next_sentence = generate_paraphrasing_sentence(
                child_age=st.session_state.child_age
            )

            st.session_state.current_sentence = next_sentence
            st.session_state.current_feedback = {}
            st.session_state.student_paraphrasing_response = ""

            # Refresh the app to show the new sentence and updated progress
            st.rerun()

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

        st.button("Reset session and return to setup", on_click=reset_and_rerun)

        st.stop()
