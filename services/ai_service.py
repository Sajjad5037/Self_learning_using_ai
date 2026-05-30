import streamlit as st
import json
from openai import OpenAI


client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


def generate_paraphrasing_sentence(child_age):

    prompt = f"""
    Generate one paraphrasing sentence
    suitable for a {child_age} year old.

    Return ONLY the sentence.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content



def evaluate_paraphrasing_response(
    original_sentence,
    student_response,
    child_age
):

    prompt = f"""
    Original sentence:
    {original_sentence}

    Student response:
    {student_response}

    Student age:
    {child_age}

    Evaluate the paraphrasing response and provide coaching.

    Return ONLY valid JSON with all fields.

    Example:

    {{
      "coach_response": "Great effort.",
      "effort_score": 7,
      "progress_increment": 10,
      "engagement_level": "strong",
      "improvement_tip": "Try using a different verb and keep the meaning intact.",
      "suggested_paraphrase": "...",
      "should_try_again": true
    }}

    If the response is strong enough, set "should_try_again" to false.
    If the response can improve, provide a clear tip and a stronger suggested paraphrase.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    return json.loads(content)
