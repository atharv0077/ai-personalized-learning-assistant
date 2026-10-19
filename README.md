# AI-Powered Personalized Learning Assistant

## Aim
Build a learning assistant that explains a student-selected topic, asks five MCQs, evaluates answers, gives feedback, and creates a personalized revision plan.

## Features
- Subject/topic input and learning-level selection
- Topic explanation with an example
- Five multiple-choice questions
- Automatic score and percentage calculation
- Feedback for each answer
- Revision plan based on performance
- Demo mode works without an API key
- Optional Generative AI mode using the OpenAI API

## Technologies
Python, Streamlit, OpenAI API (optional), JSON

## Requirements
- Python 3.10 or newer recommended
- Internet connection only if using Generative AI mode

## How to run in VS Code
1. Extract the ZIP and open the project folder in VS Code.
2. Open the terminal in that folder.
3. Create and activate a virtual environment (optional but recommended):
   - Windows: `py -m venv .venv`
   - PowerShell: `.\.venv\Scripts\Activate.ps1`
4. Install packages:
   `pip install -r requirements.txt`
5. Start the application:
   `streamlit run app.py`
6. Open the local URL shown in the terminal (usually `http://localhost:8501`).

## Enable Generative AI (optional)
Set your API key as an environment variable before launching Streamlit. Do not put the key directly in the source code or upload it to GitHub.

PowerShell:
`$env:OPENAI_API_KEY="your-api-key"`
`streamlit run app.py`

Then enable **Use Generative AI** in the sidebar and click **Generate learning session**. API usage may incur charges. If no key is configured, use demo mode.

## Test cases
1. Topic = Machine Learning, demo mode: built-in explanation and five MCQs appear.
2. Answer all five questions correctly: score should be 5/5 and strong-performance revision guidance appears.
3. Answer two questions correctly: score should be 2/5 and a foundational revision plan appears.
4. Leave a question unanswered: it is counted as incorrect and feedback identifies the correct answer.
5. Enter a custom topic in demo mode: a general study guide appears. For topic-specific AI-generated content, enable Generative AI and configure the API key.

## Observation
The application takes a topic as input, presents learning material, evaluates five answers, calculates the score, explains incorrect answers, and recommends revision activities based on performance.

## Limitations
- Demo mode provides built-in content for Machine Learning, DBMS, and Python; other topics receive a general study guide and generic practice questions.
- AI output may contain errors and should be checked.
- Generative AI mode requires an OpenAI API key and internet access.

## Conclusion
The project demonstrates how a Generative AI tool can support personalized learning by combining explanations, quizzes, answer evaluation, feedback, and a performance-based revision plan.
