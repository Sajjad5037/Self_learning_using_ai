
# app.py

```python
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
        [10, 15, 20, 30],
        index=2
    )

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
```

---

# tabs/paraphrasing_tab.py

```python
import streamlit as st
from services.ai_service import (
    generate_paraphrasing_sentence,
    evaluate_paraphrasing_response
)
from services.progress_service import update_progress
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

    st.header("🔄 Sentence Paraphrasing")

    initialize_timer()

    remaining_seconds = get_remaining_seconds()

    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    st.info(f"Session Time Remaining: {minutes}:{seconds:02d}")

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
            st.warning("Please enter a response.")
            return

        evaluation = evaluate_paraphrasing_response(
            original_sentence=st.session_state.current_sentence,
            student_response=student_response,
            child_age=st.session_state.child_age
        )

        st.session_state.chat_history.append({
            "original_sentence": st.session_state.current_sentence,
            "student_response": student_response,
            "evaluation": evaluation
        })

        update_progress(
            evaluation["progress_increment"]
        )

        st.success(evaluation["coach_response"])

        st.write(f"Effort Score: {evaluation['effort_score']}/10")

        next_sentence = generate_paraphrasing_sentence(
            child_age=st.session_state.child_age
        )

        st.session_state.current_sentence = next_sentence

        st.rerun()

    if has_session_ended():

        st.warning("Session completed.")

        report = generate_final_report()

        send_report_email(report)

        st.success("Guardian report sent successfully.")

        st.text_area(
            "Generated Report",
            report,
            height=400
        )
```

---

# tabs/creative_tab.py

```python
import streamlit as st


def render_creative_tab():

    st.header("✨ Creative Writing")

    st.info(
        "This module will be implemented later."
    )
```

---

# tabs/reading_tab.py

```python
import streamlit as st


def render_reading_tab():

    st.header("📖 Reading Comprehension")

    st.info(
        "This module will be implemented later."
    )
```

---

# prompts/paraphrasing_system_prompt.txt

```text
You are an encouraging English paraphrasing coach for children.

Your job is to help the child:
- improve English expression
- improve vocabulary
- improve sentence restructuring
- improve communication confidence

Rules:
- Be warm and supportive
- Encourage effort
- Ask guiding questions
- Reward meaningful participation
- Never shame mistakes
- Never behave harshly
- Use age-appropriate explanations
- Do NOT fully rewrite everything immediately

The child should remain the active learner.
```

---

# prompts/evaluation_prompt.txt

```text
You are evaluating a child paraphrasing exercise.

Evaluate:
- effort
- engagement
- meaning preservation
- vocabulary experimentation
- sentence clarity

Return JSON only.

Required JSON format:

{
  "coach_response": "...",
  "effort_score": 0,
  "progress_increment": 0,
  "engagement_level": "..."
}
```

---

# prompts/report_prompt.txt

```text
Generate a guardian report for a child learning session.

The report should:
- feel professional
- feel educational
- feel supportive
- avoid harsh judgment
- summarize engagement quality
- summarize effort level
- summarize paraphrasing growth
- summarize communication development

Include:
- session overview
- engagement summary
- effort level
- paraphrasing examples
- encouraging closing summary
```

---

# services/ai_service.py

```python
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
        model="gpt-4.1-mini",
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
```

---

# services/email_service.py

```python
import smtplib
from email.mime.text import MIMEText


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "YOUR_EMAIL@gmail.com"
EMAIL_PASSWORD = "YOUR_APP_PASSWORD"



def send_email(receiver_email, subject, body):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver_email

    server = smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT
    )

    server.starttls()

    server.login(
        EMAIL_ADDRESS,
        EMAIL_PASSWORD
    )

    server.sendmail(
        EMAIL_ADDRESS,
        receiver_email,
        msg.as_string()
    )

    server.quit()
```

---

# services/report_service.py

```python
import streamlit as st
from services.email_service import send_email
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_OPENAI_API_KEY"
)


LEVELS = {
    range(0, 21): "Beginner Explorer",
    range(21, 41): "Sentence Builder",
    range(41, 61): "Expression Explorer",
    range(61, 81): "Vocabulary Adventurer",
    range(81, 101): "Communication Master"
}



def get_learning_level(progress):

    for score_range, level in LEVELS.items():

        if progress in score_range:
            return level

    return "Beginner Explorer"



def generate_final_report():

    progress = st.session_state.progress

    learning_level = get_learning_level(progress)

    prompt = f"""
    Generate a guardian report.

    Child Name:
    {st.session_state.child_name}

    Child Age:
    {st.session_state.child_age}

    Progress Score:
    {progress}

    Learning Level:
    {learning_level}

    Chat History:
    {st.session_state.chat_history}

    The report should feel:
    - supportive
    - professional
    - educational
    - encouraging
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

    return response.choices[0].message.content



def send_report_email(report):

    send_email(
        receiver_email=st.session_state.guardian_email,
        subject="AI Learning Session Report",
        body=report
    )
```

---

# services/progress_service.py

```python
import streamlit as st



def update_progress(progress_increment):

    st.session_state.progress += progress_increment

    if st.session_state.progress > 100:
        st.session_state.progress = 100
```

---

# utils/timer_utils.py

```python
import streamlit as st
import time



def initialize_timer():

    if "session_start_time" not in st.session_state:

        st.session_state.session_start_time = time.time()



def get_remaining_seconds():

    elapsed = time.time() - st.session_state.session_start_time

    duration_seconds = (
        st.session_state.session_duration_minutes * 60
    )

    remaining = int(duration_seconds - elapsed)

    return max(remaining, 0)



def has_session_ended():

    return get_remaining_seconds() <= 0
```

---

# utils/session_utils.py

```python
import streamlit as st



def initialize_session_state():

    defaults = {
        "child_name": "",
        "child_age": 13,
        "guardian_email": "",
        "session_duration_minutes": 20,
        "progress": 0,
        "chat_history": [],
        "current_sentence": ""
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value
```

---

# requirements.txt

```text
streamlit
openai
```
