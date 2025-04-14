import json
import random
import requests
import streamlit as st

def load_questions(skills, path="real_mcq_bank.json"):
    with open(path, "r") as f:
        all_qs = json.load(f)
    return [q for q in all_qs if q["skill"] in skills]

def fetch_questions_from_api(skills, api_url="https://example.com/api/questions", api_key="your_api_key"):
    """
    Fetches questions from a real-time API based on the provided skills.

    Args:
        skills (list): List of skills to generate questions for.
        api_url (str): The API endpoint for fetching questions.
        api_key (str): The API key for authentication.

    Returns:
        list: A list of questions in the format [{"id": ..., "question": ..., "options": [...], "answer": ...}].
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {"skills": skills}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        questions = response.json().get("questions", [])

        if not questions:
            print("Debug: API returned no questions. Falling back to local questions.")
            return load_questions(skills)  # Fallback to local questions

        # Shuffle the questions to ensure variety
        random.shuffle(questions)
        return questions
    except requests.exceptions.RequestException as e:
        print(f"Error fetching questions: {e}")
        print("Debug: Falling back to local questions.")
        return load_questions(skills)  # Fallback to local questions

def run_quiz(skills, num_qs=5):
    questions = load_questions(skills)
    random.shuffle(questions)
    selected = questions[:num_qs]

    st.session_state["quiz_answers"] = st.session_state.get("quiz_answers", {})

    form_key = f"quiz_form_{random.randint(1, 10000)}"  # Generate a unique key for the form
    with st.form(form_key):
        for q in selected:
            user_ans = st.radio(
                q["question"],
                q["options"],
                key=f"quiz_{q['id']}"
            )
            st.session_state["quiz_answers"][q["id"]] = user_ans

        submitted = st.form_submit_button("✅ Submit Quiz")

    score = 0
    wrong = []
    if submitted:
        for q in selected:
            user_ans = st.session_state["quiz_answers"].get(q["id"], "")
            if user_ans == q["answer"]:
                score += 1
            else:
                q["user_answer"] = user_ans
                wrong.append(q)

        return score, len(selected), wrong

    return None, len(selected), []
