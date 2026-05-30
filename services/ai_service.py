import streamlit as st
import json
import re
from json import JSONDecodeError
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

    # Try to parse the AI response as JSON. If parsing fails,
    # attempt to extract a JSON object from the text. If that
    # still fails, return a safe fallback so the app doesn't crash.
    try:
        return json.loads(content)
    except JSONDecodeError:

        # Try to extract the first JSON object-looking substring
        # This handles cases where the model includes preface or
        # explanation around the JSON.
        m = re.search(r"(\{.*\})", content, re.DOTALL)

        if m:
            json_text = m.group(1)
            try:
                return json.loads(json_text)
            except JSONDecodeError:
                pass

        # If we reach here, we couldn't parse JSON. Log a brief
        # warning to the Streamlit UI and return a conservative
        # fallback evaluation that asks the student to try again.
        try:
            import streamlit as st
            st.warning(
                "AI response parsing failed; showing fallback feedback."
            )
        except Exception:
            # If Streamlit isn't available in this context, ignore.
            pass

        fallback = {
            "coach_response": "I couldn't parse my evaluation properly — let's try again. Here's one tip: keep the original meaning and use simpler words.",
            "effort_score": 0,
            "progress_increment": 0,
            "engagement_level": "unknown",
            "improvement_tip": "Keep the meaning, try changing one phrase or verb at a time.",
            "suggested_paraphrase": "",
            "should_try_again": True,
            "raw_response": content
        }

        return fallback
