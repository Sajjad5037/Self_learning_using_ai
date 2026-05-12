
import json
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_OPENAI_API_KEY"
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

    Evaluate the response.

    Return ONLY valid JSON.

    Example:

    {{
      "coach_response": "Great effort.",
      "effort_score": 7,
      "progress_increment": 10,
      "engagement_level": "strong"
    }}
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
