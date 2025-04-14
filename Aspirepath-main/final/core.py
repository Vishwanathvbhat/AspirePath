from config import SKILL_TEMPLATES
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize MongoDB client and collection
client = MongoClient("mongodb://localhost:27017/")
db = client["skills_database"]
skills_collection = db["skills"]

# Predefined career goals and their associated skills
CAREER_SKILLS = {
    "Data Analyst": "Excel, SQL, Python, Tableau, Statistics, Power BI",
    "Web Developer": "HTML, CSS, JavaScript, React, Node.js, MongoDB",
    "ML Engineer": "Python, Numpy, Pandas, Scikit-learn, Deep Learning",
    "Cybersecurity Analyst": "Network Security, Cryptography, Firewalls, Linux, Ethical Hacking",
    "AI Engineer": "Python, TensorFlow, PyTorch, Machine Learning, Neural Networks",
    "Software Developer": "C++, Java, Python, Data Structures, Algorithms",
    "Game Developer": "C++, Unity, Unreal Engine, Game Physics, 3D Modeling"
}

def assess_skills(text):
    found = []
    for skills in SKILL_TEMPLATES.values():
        found += [skill for skill in skills if skill.lower() in text.lower()]
    # Store the extracted skills in the database
    skills_collection.insert_one({"text": text, "skills": found})
    return list(set(found))

def select_goal():
    return list(SKILL_TEMPLATES.keys())

def generate_roadmap(user_skills, goal):
    required = SKILL_TEMPLATES.get(goal, [])
    missing = list(set(required) - set(user_skills))
    roadmap = [f"Learn {skill}" for skill in missing]
    return roadmap, required

def predict_career(user_skills):
    """
    Predicts the most suitable career goal based on user skills using cosine similarity.

    Args:
        user_skills (list): List of skills provided by the user.

    Returns:
        str: Predicted career goal.
    """
    user_skills_str = ", ".join(user_skills)
    vectorizer = TfidfVectorizer()
    all_skills = list(CAREER_SKILLS.values()) + [user_skills_str]
    tfidf_matrix = vectorizer.fit_transform(all_skills)

    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    if max(similarities[0]) < 0.1:  # Threshold for unmatched skills
        return "Generalist"  # Fallback career goal for unmatched skills
    predicted_index = similarities.argmax()
    return list(CAREER_SKILLS.keys())[predicted_index]
