import streamlit as st
from core import assess_skills, select_goal, generate_roadmap, predict_career
from helpers import parse_resume, fetch_youtube_resources, store_quiz_results  # Corrected import for store_quiz_results
from project_suggester import suggest_projects
from quiz_engine import load_questions, run_quiz, fetch_questions_from_api
from pymongo import MongoClient
import hashlib

# Initialize user_skills as an empty list
user_skills = []

st.set_page_config(page_title="AspirePath", layout="wide")

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["aspirepath"]
users_collection = db["users"]

# Update the background to a more attractive gradient
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #ff9a9e, #fad0c4, #fbc2eb, #a18cd1);
        background-size: 300% 300%;
        animation: gradientBG 10s ease infinite;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Log In / Sign Up", "Home", "Skill Quiz & Resume Upload", "Career Roadmap", "Peer Comparison", "Progress Tracker", "Progress Dashboard"])

# Log In / Sign Up Section
if page == "Log In / Sign Up":
    st.header("🔐 Log In / Sign Up")

    # Tabs for Log In and Sign Up
    tab1, tab2 = st.tabs(["Log In", "Sign Up"])

    with tab1:
        st.subheader("Log In")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Log In"):
            if login_email and login_password:
                hashed_password = hashlib.sha256(login_password.encode()).hexdigest()
                user = users_collection.find_one({"email": login_email, "password": hashed_password})
                if user:
                    st.success(f"Welcome back, {user['name']}!")
                else:
                    st.error("Invalid email or password.")
            else:
                st.warning("Please enter both email and password.")

    with tab2:
        st.subheader("Sign Up")
        signup_name = st.text_input("Name", key="signup_name")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Sign Up"):
            if signup_name and signup_email and signup_password:
                if users_collection.find_one({"email": signup_email}):
                    st.error("An account with this email already exists.")
                else:
                    hashed_password = hashlib.sha256(signup_password.encode()).hexdigest()
                    users_collection.insert_one({"name": signup_name, "email": signup_email, "password": hashed_password})
                    st.success("Account created successfully! You can now log in.")
            else:
                st.warning("Please fill out all fields.")

# Home Section
if page == "Home":
    st.title("🚀 Welcome to AspirePath")

    st.markdown(
        """
        ### 🌟 Why Choose AspirePath?
        - **Personalized Career Guidance**: Tailored roadmaps to achieve your dream career.
        - **Skill Assessment**: Identify your strengths and areas for improvement.
        - **Learning Resources**: Access curated tutorials, courses, and project ideas.
        - **Peer Comparison**: Benchmark your skills against others.

        ### 📖 How to Get Started?
        1. Navigate to **Skill Quiz & Resume Upload** to assess your skills.
        2. Explore **Career Roadmap** for a step-by-step guide to your goals.
        3. Compare your skills with peers in **Peer Comparison**.

        ### 💡 Pro Tip:
        Regularly update your skills and revisit AspirePath to stay on track with your career goals!
        """
    )

elif page == "Skill Quiz & Resume Upload":
    st.header("📄 Upload Resume & Take Skill Quiz")

    # Resume Upload Section
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

    if uploaded_file:
        resume_text = parse_resume(uploaded_file)
        user_skills = assess_skills(resume_text)
        st.success(f"Extracted Skills: {', '.join(user_skills)}")

    st.markdown("Or manually enter your current skills (comma separated):")
    manual_input = st.text_input("Example: Python, SQL, Power BI")
    if manual_input:
        user_skills = [skill.strip() for skill in manual_input.split(",")]
        st.success(f"Using manual skills: {', '.join(user_skills)}")

    # Skill Quiz Section
    if user_skills:
        st.subheader("📝 Skill Assessment Quiz")
        st.write("Debug: User skills detected:", user_skills)  # Debug log

        # Fetch questions dynamically from the API
        questions = fetch_questions_from_api(user_skills)

        if not questions:
            st.warning("No questions could be fetched from the API. Please try again later.")
        else:
            with st.form("quiz_form"):
                user_answers = {}

                for idx, question in enumerate(questions):
                    st.markdown(f"**Q{idx + 1}: {question['question']}**")
                    user_answers[question['id']] = st.radio(
                        "Select an answer:",
                        options=question['options'],
                        key=f"q{idx + 1}"
                    )

                submitted = st.form_submit_button("Submit Quiz")

            # Store quiz results after submission
            if submitted:
                score = sum(1 for q in questions if user_answers.get(q['id']) == q['answer'])
                total = len(questions)
                wrong_qs = [q for q in questions if user_answers.get(q['id']) != q['answer']]

                # Save quiz results to the database
                store_quiz_results(user_id="user123", quiz_results={
                    "score": score,
                    "total": total,
                    "wrong_answers": wrong_qs
                })

                st.success(f"✅ You scored {score} out of {total}")

                if wrong_qs:
                    st.subheader("🔍 Review Incorrect Answers")
                    for q in wrong_qs:
                        st.markdown(f"**Q:** {q['question']}")
                        st.markdown(f"❌ Your Answer: {user_answers.get(q['id'])}")
                        st.markdown(f"✅ Correct Answer: **{q['answer']}**")
    else:
        st.warning("No skills found. Please upload a resume or enter skills manually.")

elif page == "Career Roadmap":
    st.header("🎯 Choose Your Career Goal")

    # Input for user skills
    user_input_skills = st.text_input("Enter your skills (comma-separated, e.g., Python, SQL, Power BI):")

    if user_input_skills:
        user_skills = [skill.strip() for skill in user_input_skills.split(",")]
        predicted_career = predict_career(user_skills)

        st.subheader(f"🔮 Predicted Career Goal: {predicted_career}")

        st.subheader("📚 Personalized Learning Roadmap")
        roadmap, all_required = generate_roadmap(user_skills, predicted_career)

        # Debugging logs to trace data flow
        st.write("Debug: User input skills:", user_input_skills)
        st.write("Debug: Predicted career goal:", predicted_career)
        st.write("Debug: Generated roadmap:", roadmap)

        if not roadmap:
            st.warning("No roadmap could be generated. Please check your input skills or try a different set of skills.")
        else:
            for step in roadmap:
                st.markdown(f"✅ {step}")

        # Generate a step-by-step learning roadmap
        st.subheader("📘 Step-by-Step Learning Roadmap")
        if roadmap:
            for idx, step in enumerate(roadmap, start=1):
                st.markdown(f"{idx}. {step}")
        else:
            st.success("You already have all the required skills for this career goal!")

        st.subheader("🎥 Curated YouTube Tutorials")
        for skill in roadmap:
            query = skill.replace("Learn ", "")
            st.markdown(f"**{query}**:")
            for link in fetch_youtube_resources(query):
                st.markdown(f"- [Watch Tutorial]({link})")

        st.subheader("📘 Suggested Tutorials and Courses")

        # Example curated resources
        resources = [
            {"title": "Python for Everybody", "platform": "Coursera", "link": "https://www.coursera.org/specializations/python"},
            {"title": "Full-Stack Web Development", "platform": "Udemy", "link": "https://www.udemy.com/course/the-web-developer-bootcamp/"},
            {"title": "Machine Learning", "platform": "edX", "link": "https://www.edx.org/course/machine-learning"},
            {"title": "Data Science Professional Certificate", "platform": "IBM on Coursera", "link": "https://www.coursera.org/professional-certificates/ibm-data-science"},
            {"title": "Cybersecurity Fundamentals", "platform": "Pluralsight", "link": "https://www.pluralsight.com/courses/cyber-security-fundamentals"}
        ]

        for resource in resources:
            st.markdown(f"- **{resource['title']}** on {resource['platform']}: [Link]({resource['link']})")
    else:
        st.warning("Please enter your skills to generate a career roadmap.")

elif page == "Peer Comparison":
    st.header("🤝 Peer Skill Comparison Based on Resumes")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Person 1")
        person1_resume = st.file_uploader("Upload Resume (PDF or DOCX):", type=["pdf", "docx"], key="person1_resume")
        person1_skills = []
        if person1_resume:
            person1_text = parse_resume(person1_resume)
            person1_skills = assess_skills(person1_text)
            st.success(f"Extracted Skills: {', '.join(person1_skills)}")

    with col2:
        st.subheader("Person 2")
        person2_resume = st.file_uploader("Upload Resume (PDF or DOCX):", type=["pdf", "docx"], key="person2_resume")
        person2_skills = []
        if person2_resume:
            person2_text = parse_resume(person2_resume)
            person2_skills = assess_skills(person2_text)
            st.success(f"Extracted Skills: {', '.join(person2_skills)}")

    if person1_skills and person2_skills:
        st.subheader("🔍 Comparison Results")

        common_skills = set(person1_skills) & set(person2_skills)
        unique_to_person1 = set(person1_skills) - set(person2_skills)
        unique_to_person2 = set(person2_skills) - set(person1_skills)

        st.markdown("**Common Skills:**")
        st.write(common_skills if common_skills else "None")

        st.markdown("**Unique to Person 1:**")
        st.write(unique_to_person1 if unique_to_person1 else "None")

        st.markdown("**Unique to Person 2:**")
        st.write(unique_to_person2 if unique_to_person2 else "None")

# Progress Tracking Section
if page == "Progress Tracker":
    st.header("📈 Weekly Progress Tracker")

    # Input for weekly achievements
    st.subheader("🏆 Log Your Weekly Achievements")
    weekly_achievements = st.text_area("Enter your achievements for this week (e.g., completed Python course, built a project):")

    # Store weekly achievements in the database
    progress_collection = db["progress"]

    if st.button("Submit Achievements"):
        if weekly_achievements:
            # Example structure for storing data
            progress_data = {
                "user_id": "user123",  # Replace with dynamic user ID if available
                "date": pd.Timestamp.now(),
                "achievements": weekly_achievements,
                "skills_learned": len(weekly_achievements.split(',')),  # Example logic
                "projects_completed": weekly_achievements.lower().count("project")  # Example logic
            }
            progress_collection.insert_one(progress_data)
            st.success("Your achievements have been logged successfully!")
        else:
            st.warning("Please enter your achievements before submitting.")

    # Suggestions based on achievements
    st.subheader("💡 Suggestions for Next Week")
    if weekly_achievements:
        st.markdown("Based on your achievements, here are some suggestions:")
        st.markdown("- Continue learning advanced Python topics.")
        st.markdown("- Start a new project using the skills you've learned.")
        st.markdown("- Explore related fields like Data Analysis or Machine Learning.")
    else:
        st.info("Log your achievements to receive personalized suggestions.")

# Progress Dashboard Section
if page == "Progress Dashboard":
    st.header("📊 Progress Dashboard")

    # Example data for progress tracking
    import pandas as pd
    import altair as alt

    data = pd.DataFrame({
        'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'Skills Learned': [3, 5, 2, 4],
        'Projects Completed': [1, 2, 1, 3]
    })

    # Line chart for skills learned
    st.subheader("📈 Skills Learned Over Time")
    skills_chart = alt.Chart(data).mark_line(point=True).encode(
        x='Week',
        y='Skills Learned',
        tooltip=['Week', 'Skills Learned']
    ).properties(width=700, height=400)
    st.altair_chart(skills_chart)

    # Bar chart for projects completed
    st.subheader("📊 Projects Completed Over Time")
    projects_chart = alt.Chart(data).mark_bar().encode(
        x='Week',
        y='Projects Completed',
        tooltip=['Week', 'Projects Completed']
    ).properties(width=700, height=400)
    st.altair_chart(projects_chart)

    st.info("Update your weekly achievements in the Progress Tracker to see your progress here!")
