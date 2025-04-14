# AspirePath

AspirePath is a career guidance platform designed to help users identify their skills, set career goals, and track their progress. It provides personalized roadmaps, skill assessments, and learning resources to help users achieve their career aspirations.

## Features

- **Log In / Sign Up**: Secure user authentication integrated with MongoDB.
- **Skill Quiz & Resume Upload**: Extract skills from resumes or manually input them, and take quizzes to assess your skills.
- **Career Roadmap**: Get personalized career goals and step-by-step learning roadmaps.
- **Peer Comparison**: Compare your skills with others by uploading resumes.
- **Progress Tracker**: Log weekly achievements and receive suggestions for improvement.
- **Progress Dashboard**: Visualize your progress over time with interactive charts.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd final
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Project Structure

```
final/
├── app.py                 # Main application file
├── config.py              # Configuration for skill templates
├── core.py                # Core logic for skill assessment and career prediction
├── helpers.py             # Utility functions for resume parsing and data storage
├── project_suggester.py   # Suggests project ideas based on skills
├── quiz_engine.py         # Handles skill assessment quizzes
├── real_mcq_bank.json     # Local question bank for quizzes
├── requirements.txt       # Python dependencies
└── __pycache__/           # Compiled Python files
```

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: MongoDB

## How to Use

1. **Log In / Sign Up**:
   - Create an account or log in to access the platform.
2. **Skill Quiz & Resume Upload**:
   - Upload your resume or manually input your skills.
   - Take a quiz to assess your skills.
3. **Career Roadmap**:
   - Get a personalized career goal and a step-by-step roadmap.
4. **Peer Comparison**:
   - Compare your skills with others by uploading resumes.
5. **Progress Tracker**:
   - Log your weekly achievements and receive suggestions for improvement.
6. **Progress Dashboard**:
   - Visualize your progress over time with interactive charts.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any inquiries or support, please contact sarveshbalaji26@gmail.com.
## Team
- S Sarvesh Balaji
- S Nandan
- Vishwanath V
- Praveen Koujalagi
