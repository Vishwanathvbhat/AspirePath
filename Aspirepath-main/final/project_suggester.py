def suggest_projects(skills):
    projects = []

    skill_projects = {
        "Python": [
            "Build a personal expense tracker",
            "Automate PDF or Excel reports",
            "Create a command-line to-do app"
        ],
        "JavaScript": [
            "Build a weather app using APIs",
            "Make a quiz app with timers",
            "Create a dynamic portfolio site"
        ],
        "React": [
            "Create a task manager with drag & drop",
            "Build a movie browser with OMDB API"
        ],
        "SQL": [
            "Design a student-course enrollment database",
            "Build an analytics dashboard using sample sales data"
        ],
        "Excel": [
            "Create a budgeting sheet with charts & automation",
            "Build a sales performance tracker"
        ],
        "Machine Learning": [
            "Predict house prices using regression",
            "Build a spam email classifier",
            "Image classification with CNN"
        ],
        "HTML": [
            "Build a responsive landing page",
            "Create a blog layout with HTML & CSS"
        ],
        "CSS": [
            "Recreate famous brand websites’ UIs",
            "Make a responsive grid-based photo gallery"
        ],
        "Power BI": [
            "Create interactive dashboards from Excel data",
            "Build a sales analytics report"
        ],
        "Cybersecurity": [
            "Set up a virtual lab for penetration testing",
            "Simulate a phishing attack scenario"
        ]
    }

    for skill in skills:
        matched = skill_projects.get(skill.strip(), [])
        if matched:
            projects.extend(matched)

    # Limit total projects to avoid overwhelming the user
    return projects[:7]
