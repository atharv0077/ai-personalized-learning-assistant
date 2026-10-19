import os
import json
import random
import streamlit as st

# Optional: set OPENAI_API_KEY in your environment to enable AI-generated content.
# The app also has a built-in demo mode, so it can run without an API key.

st.set_page_config(page_title="AI Personalized Learning Assistant", page_icon="🎓", layout="wide")

st.title("🎓 AI-Powered Personalized Learning Assistant")
st.caption("Learn a topic, test your understanding, and get a personalized revision plan.")

DEMO_CONTENT = {
    "Machine Learning": {
        "explanation": """Machine Learning (ML) is a branch of Artificial Intelligence that enables computers to learn patterns from data and make predictions without being explicitly programmed for every situation.

**Example:** An email service can learn from previously labelled emails to identify spam.

**Common types:**
- **Supervised learning:** Learns from labelled examples, such as predicting house prices.
- **Unsupervised learning:** Finds patterns in unlabelled data, such as grouping customers.
- **Reinforcement learning:** Learns by receiving rewards or penalties for actions.""",
        "questions": [
            {"question": "What is the main goal of Machine Learning?", "options": ["To learn patterns from data", "To replace all databases", "To design web pages only", "To increase file size"], "answer": 0, "explanation": "Machine Learning identifies patterns in data to make predictions or decisions."},
            {"question": "Which type uses labelled training examples?", "options": ["Unsupervised learning", "Supervised learning", "Reinforcement learning", "Random learning"], "answer": 1, "explanation": "Supervised learning learns from examples that have known labels or target values."},
            {"question": "Grouping customers by similar behaviour is commonly an example of:", "options": ["Clustering", "Compilation", "Encryption", "Sorting files"], "answer": 0, "explanation": "Clustering groups similar data points and is commonly used in unsupervised learning."},
            {"question": "Which is an example of Machine Learning?", "options": ["A calculator adding 2 + 2 using fixed rules", "A spam filter learning from examples", "A monitor displaying pixels", "A keyboard entering text"], "answer": 1, "explanation": "A spam filter can learn patterns from labelled examples of spam and legitimate email."},
            {"question": "In reinforcement learning, an agent learns mainly through:", "options": ["Rewards and penalties", "Only labelled images", "Manual typing of every answer", "Database tables"], "answer": 0, "explanation": "Reinforcement learning uses feedback such as rewards or penalties for actions."}
        ]
    },
    "Database Management System": {
        "explanation": """A Database Management System (DBMS) is software used to create, store, organize, retrieve, and manage data in a database.

**Example:** A college database can store student details, courses, marks, and attendance.

**Key terms:**
- **Table:** Organizes data into rows and columns.
- **Primary key:** Uniquely identifies each row.
- **Foreign key:** Connects records between related tables.
- **SQL:** A language used to query and manage relational databases.""",
        "questions": [
            {"question": "What is the main purpose of a DBMS?", "options": ["Manage data", "Edit videos", "Create computer hardware", "Increase screen brightness"], "answer": 0, "explanation": "A DBMS provides tools to store, organize, retrieve, and manage data."},
            {"question": "Which key uniquely identifies a row in a table?", "options": ["Foreign key", "Primary key", "Duplicate key", "Optional key"], "answer": 1, "explanation": "A primary key uniquely identifies each row in a table."},
            {"question": "Which language is commonly used with relational databases?", "options": ["SQL", "HTML only", "CSS", "PNG"], "answer": 0, "explanation": "SQL is used to query and manage data in relational databases."},
            {"question": "A table is mainly organized into:", "options": ["Rows and columns", "Slides and animations", "Folders only", "Audio tracks"], "answer": 0, "explanation": "Relational tables arrange data in rows (records) and columns (fields)."},
            {"question": "A foreign key is used mainly to:", "options": ["Relate tables", "Change font size", "Compress images", "Turn off a computer"], "answer": 0, "explanation": "A foreign key references a key in another table to establish a relationship."}
        ]
    },
    "Python Programming": {
        "explanation": """Python is a high-level, general-purpose programming language known for readable syntax. It is used in automation, web development, data analysis, and artificial intelligence.

**Example:**
```python
name = "Asha"
print("Hello", name)
```
This program stores a name in a variable and prints a greeting.

**Key concepts:** Variables store values, conditions make decisions, loops repeat instructions, and functions group reusable code.""",
        "questions": [
            {"question": "Which function displays output in Python?", "options": ["show()", "print()", "displayText()", "echoLine()"], "answer": 1, "explanation": "The built-in print() function displays output."},
            {"question": "Which symbol starts a single-line comment in Python?", "options": ["//", "#", "<!--", "**"], "answer": 1, "explanation": "Python uses # for a single-line comment."},
            {"question": "Which data type stores True or False?", "options": ["str", "list", "bool", "float"], "answer": 2, "explanation": "The bool type stores Boolean values True and False."},
            {"question": "Which keyword defines a function?", "options": ["function", "func", "def", "make"], "answer": 2, "explanation": "Python uses the def keyword to define a function."},
            {"question": "Which structure repeats a block of code?", "options": ["Loop", "Comment", "Variable", "Import"], "answer": 0, "explanation": "Loops such as for and while repeat a block of code."}
        ]
    }
}

def get_demo_content(topic):
    if topic in DEMO_CONTENT:
        return DEMO_CONTENT[topic]
    return {
        "explanation": f"""**{topic}** is the topic you selected. Start by defining its main idea, learning the important terms, and studying one practical example.

**Suggested approach:**
1. Write a one-sentence definition.
2. Identify three important concepts.
3. Find or create a real-world example.
4. Explain the topic in your own words.

*Demo mode is showing a general study guide. Add an OpenAI API key to generate a topic-specific explanation and quiz for any topic.*""",
        "questions": [
            {"question": f"What should you do first when learning {topic}?", "options": ["Understand its main idea", "Memorize unrelated facts", "Skip examples", "Avoid practice"], "answer": 0, "explanation": "Begin by understanding the core idea, then study terms and examples."},
            {"question": "Why are examples useful when learning a concept?", "options": ["They connect theory to practice", "They remove the need to understand", "They always replace definitions", "They make every topic identical"], "answer": 0, "explanation": "Examples show how a concept can be applied."},
            {"question": "Which is a useful revision strategy?", "options": ["Practice questions", "Never review mistakes", "Study without breaks forever", "Ignore difficult concepts"], "answer": 0, "explanation": "Practice questions help identify gaps in understanding."},
            {"question": "What should you do after answering a question incorrectly?", "options": ["Review the concept and explanation", "Ignore the mistake", "Stop studying permanently", "Change the topic randomly"], "answer": 0, "explanation": "Reviewing mistakes helps correct misunderstandings."},
            {"question": "How can you check your understanding?", "options": ["Explain the concept in your own words", "Only look at the title", "Avoid practice", "Copy text without reading"], "answer": 0, "explanation": "Explaining an idea in your own words is a useful self-check."}
        ]
    }

def generate_with_openai(topic, level):
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = f"""Create learning material for a student at {level} level about: {topic}.
Return ONLY valid JSON with this exact structure:
{{
 "explanation": "A clear, accurate explanation with one suitable example. Use plain text, no HTML.",
 "questions": [
  {{"question":"...", "options":["A","B","C","D"], "answer":0, "explanation":"..."}}
 ]
}}
Create exactly 5 multiple-choice questions. Each answer must be an integer from 0 to 3 and match the correct option. Avoid trick questions. Do not include markdown fences."""
    response = client.responses.create(model="gpt-4.1-mini", input=prompt)
    data = json.loads(response.output_text)
    if not isinstance(data.get("questions"), list) or len(data["questions"]) != 5:
        raise ValueError("AI did not return exactly five questions.")
    for q in data["questions"]:
        if len(q["options"]) != 4 or not 0 <= int(q["answer"]) <= 3:
            raise ValueError("AI returned an invalid question format.")
        q["answer"] = int(q["answer"])
    return data

with st.sidebar:
    st.header("Learning setup")
    topic = st.text_input("Subject or topic", value="Machine Learning", placeholder="e.g., Normalization in DBMS")
    level = st.selectbox("Your level", ["Beginner", "Intermediate", "Advanced"])
    use_ai = st.toggle("Use Generative AI (requires API key)", value=False)
    st.caption("Without AI enabled, the app runs in demo mode with built-in learning content.")
    generate = st.button("Generate learning session", type="primary", use_container_width=True)

if "content" not in st.session_state:
    st.session_state.content = get_demo_content("Machine Learning")
    st.session_state.topic = "Machine Learning"
    st.session_state.submitted = False

if generate:
    if not topic.strip():
        st.error("Please enter a subject or topic.")
    elif use_ai and not os.environ.get("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY was not found. Set it in your environment, or turn off Generative AI to use demo mode.")
    else:
        with st.spinner("Preparing your learning session..."):
            try:
                content = generate_with_openai(topic.strip(), level) if use_ai else get_demo_content(topic.strip())
                st.session_state.content = content
                st.session_state.topic = topic.strip()
                st.session_state.submitted = False
                for key in list(st.session_state.keys()):
                    if key.startswith("answer_"):
                        del st.session_state[key]
                st.success("Learning session ready!")
            except Exception as e:
                st.error(f"Could not generate AI content: {e}. Try demo mode or check your API key.")

st.subheader(f"📘 Topic: {st.session_state.topic}")
st.markdown(st.session_state.content["explanation"])

st.divider()
st.subheader("📝 Knowledge Check — 5 MCQs")
st.write("Choose one answer for each question, then submit to receive feedback.")

with st.form("quiz_form"):
    for i, q in enumerate(st.session_state.content["questions"]):
        st.markdown(f"**{i+1}. {q['question']}**")
        choice = st.radio(
            f"Choose an answer for question {i+1}",
            q["options"],
            index=None,
            key=f"answer_{i}",
            label_visibility="collapsed"
        )
    submitted = st.form_submit_button("Evaluate my answers", type="primary")

if submitted:
    st.session_state.submitted = True
    st.session_state.score = 0
    st.session_state.results = []
    for i, q in enumerate(st.session_state.content["questions"]):
        selected = st.session_state.get(f"answer_{i}")
        correct_option = q["options"][q["answer"]]
        is_correct = selected == correct_option
        st.session_state.score += int(is_correct)
        st.session_state.results.append({
            "question": q["question"],
            "selected": selected or "Not answered",
            "correct": correct_option,
            "is_correct": is_correct,
            "explanation": q["explanation"]
        })

if st.session_state.get("submitted"):
    score = st.session_state.score
    st.divider()
    st.subheader("📊 Your Results")
    col1, col2, col3 = st.columns(3)
    col1.metric("Score", f"{score}/5")
    col2.metric("Percentage", f"{score*20}%")
    col3.metric("Level", "Strong" if score >= 4 else ("Developing" if score >= 3 else "Needs revision"))

    weak_topics = []
    for i, result in enumerate(st.session_state.results):
        with st.expander(f"{'✅' if result['is_correct'] else '❌'} Question {i+1}: {'Correct' if result['is_correct'] else 'Review needed'}"):
            st.write("Your answer:", result["selected"])
            st.write("Correct answer:", result["correct"])
            st.write("Feedback:", result["explanation"])
        if not result["is_correct"]:
            weak_topics.append(result["question"])

    st.subheader("🗓️ Personalized Revision Plan")
    if score == 5:
        st.success("Excellent work! Your answers show a strong understanding of this quiz.")
        plan = [
            "Today: Explain the topic from memory in 3–5 sentences.",
            "Tomorrow: Solve 5 new questions or try a practical example.",
            "In 3 days: Revisit the topic briefly to strengthen retention."
        ]
    elif score >= 3:
        st.info("Good start. Review the questions you missed before moving to advanced material.")
        plan = [
            "Today (15 minutes): Review the concepts connected to incorrect answers.",
            "Tomorrow (15 minutes): Retry the quiz without looking at the answers.",
            "In 2 days: Write a short summary and solve one practical example."
        ]
    else:
        st.warning("Spend more time on the basics, then take the quiz again.")
        plan = [
            "Today (20 minutes): Re-read the explanation and note key terms.",
            "Tomorrow (20 minutes): Study one worked example and explain it in your own words.",
            "Next study session: Retry the quiz and focus on the incorrect answers."
        ]
    for item in plan:
        st.markdown(f"- {item}")
    if weak_topics:
        st.markdown("**Topics/questions to revise:**")
        for item in weak_topics:
            st.markdown(f"- {item}")

st.divider()
st.caption("Academic demo project. Verify AI-generated explanations and questions before relying on them.")
