import os
from PyPDF2 import PdfReader
from docx import Document
from pymongo import MongoClient

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client["aspirepath"]

# Collections
resumes_collection = db["resumes"]
skills_collection = db["skills"]
quiz_results_collection = db["quiz_results"]
roadmaps_collection = db["roadmaps"]

def parse_resume(file):
    text = ""
    file_type = file.name.split(".")[-1]

    if file_type == "pdf":
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    elif file_type == "docx":
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text
    elif file_type == "txt":
        text = file.read().decode("utf-8")
    else:
        text = "Unsupported file format"

    # Store the parsed resume in the database
    resumes_collection.insert_one({"file_name": file.name, "content": text})
    return text

def fetch_youtube_resources(goal, skills=[], max_results=5):
    """
    Generates smart YouTube search links based on user goal and skills.
    """
    base_query = goal + " tutorial full course"
    if skills:
        base_query = f"{skills[0]} {skills[1] if len(skills) > 1 else ''} for {goal} full course tutorial"

    return [
        f"https://www.youtube.com/results?search_query={base_query.strip().replace(' ', '+')}&page={i+1}"
        for i in range(1,2)
    ]

def store_quiz_results(user_id, quiz_results):
    """
    Stores the quiz results in the MongoDB `quiz_results` collection.

    Args:
        user_id (str): The ID of the user taking the quiz.
        quiz_results (dict): A dictionary containing quiz details (e.g., score, total questions, wrong answers).

    Returns:
        None
    """
    quiz_results_collection.insert_one({"user_id": user_id, **quiz_results})

def store_roadmap(user_id, career_goal, roadmap):
    """
    Stores the generated roadmap in the MongoDB `roadmaps` collection.

    Args:
        user_id (str): The ID of the user.
        career_goal (str): The career goal specified by the user.
        roadmap (list): A list of steps in the roadmap.

    Returns:
        None
    """
    roadmaps_collection.insert_one({"user_id": user_id, "career_goal": career_goal, "roadmap": roadmap})
