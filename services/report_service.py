import streamlit as st

from openai import OpenAI

from services.email_service import (
    send_email
)


client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


LEVELS = {

    range(0, 21):
    "Beginner Explorer",

    range(21, 41):
    "Sentence Builder",

    range(41, 61):
    "Expression Explorer",

    range(61, 81):
    "Vocabulary Adventurer",

    range(81, 101):
    "Communication Master"
}


def get_learning_level(progress):

    for score_range, level in LEVELS.items():

        if progress in score_range:

            return level

    return "Beginner Explorer"


def generate_final_report():

    progress = st.session_state.progress

    learning_level = get_learning_level(
        progress
    )

    chat_history = st.session_state.chat_history

    prompt = f"""
    Generate a professional guardian report
    for a child learning session.

    Child Name:
    {st.session_state.child_name}

    Child Age:
    {st.session_state.child_age}

    Session Type:
    Sentence Paraphrasing

    Progress Score:
    {progress}

    Learning Level:
    {learning_level}

    Chat History:
    {chat_history}

    Important Instructions:

    - Be supportive
    - Be educational
    - Be encouraging
    - Avoid harsh criticism
    - Mention engagement quality
    - Mention vocabulary development
    - Mention paraphrasing effort
    - Mention participation consistency

    The report should include:

    1. Session Overview
    2. Engagement Summary
    3. Learning Progress Level
    4. Vocabulary & Communication Growth
    5. Areas For Improvement
    6. Encouraging Closing Summary
    """

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[

            {
                "role": "system",
                "content":
                "You are a professional educational AI report generator."
            },

            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    report = response.choices[0].message.content

    return report


def send_report_email(report):

    guardian_email = (
        st.session_state.guardian_email
    )

    send_email(
        receiver_email=guardian_email,
        subject="AI Learning Session Report",
        body=report
    )
