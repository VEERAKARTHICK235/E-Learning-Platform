import streamlit as st
import hashlib
import json
import os
import random

st.set_page_config(page_title="AI E-Learning", layout="centered")

USER_DB_FILE = "users.json"
PROGRESS_DB_FILE = "progress.json"
QUIZ_LOG_FILE = "quiz_log.json"

def load_users():
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "r") as file:
            return json.load(file)
    return {}

def save_users(users):
    with open(USER_DB_FILE, "w") as file:
        json.dump(users, file)

def load_progress():
    if os.path.exists(PROGRESS_DB_FILE):
        with open(PROGRESS_DB_FILE, "r") as file:
            return json.load(file)
    return {}

def save_progress(progress):
    with open(PROGRESS_DB_FILE, "w") as file:
        json.dump(progress, file)

def load_quiz_log():
    if os.path.exists(QUIZ_LOG_FILE):
        with open(QUIZ_LOG_FILE, "r") as file:
            return json.load(file)
    return {}

def save_quiz_log(log):
    with open(QUIZ_LOG_FILE, "w") as file:
        json.dump(log, file)

users = load_users()
progress = load_progress()
quiz_log = load_quiz_log()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "quiz_count" not in st.session_state:
    st.session_state.quiz_count = 0

if not st.session_state.logged_in:
    st.title("\U0001F512 Welcome to AI Learning Portal")
    login_tab, signup_tab = st.tabs(["Login", "Signup"])

    with login_tab:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("🔐 Login", key="login_btn"):
            if username in users and users[username] == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.quiz_count = len(quiz_log.get(username, []))
                st.success("\u2705 Logged in!")
                st.experimental_rerun()
            else:
                st.error("\u274C Invalid username or password")

    with signup_tab:
        new_username = st.text_input("Create Username")
        new_password = st.text_input("Create Password", type="password")
        if st.button("🆕 Signup", key="signup_btn"):
            if new_username in users:
                st.warning("\u26A0\uFE0F Username already exists.")
            else:
                users[new_username] = hash_password(new_password)
                save_users(users)
                st.success("\U0001F389 Signup successful! You can log in now.")
else:
    st.sidebar.write(f"\U0001F44B Hello, {st.session_state.username}")
    if st.sidebar.button("🚪 Logout", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

st.markdown("""
<style>
.main-title { color: #00ffcc; font-size: 36px; font-weight: bold; text-align: center; }
.sub-title { color: #66fcf1; text-align: center; font-size: 20px; margin-bottom: 40px; }
.course-card { background: rgba(255,255,255,0.05); padding: 20px; margin: 15px 0; border-radius: 12px; }
.btn { background-color: #00adb5; color: white; padding: 10px 20px; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>\U0001F680 E-Learning Platform</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Explore futuristic learning with AI-powered content</div>", unsafe_allow_html=True)

if st.session_state.logged_in:
    menu = ["Home", "Courses", "Video Lessons", "Assignments", "Quiz", "Review Answers", "Dashboard", "Profile"]
    choice = st.sidebar.selectbox("📚 Navigate", menu)

    courses = {
        "Python Basics": "Learn Python from scratch",
        "Data Science": "Explore data analysis techniques",
        "Machine Learning": "Understand ML algorithms",
        "AI for Beginners": "Introduction to AI",
        "Deep Learning": "Dive into deep neural networks",
        "Computer Vision": "Master image processing",
        "Natural Language Processing": "Work with text data",
        "Reinforcement Learning": "Learn agent-based learning",
        "AI Ethics": "Understand ethical implications",
        "Genarative AI": "Understanding the Gen AI"
    }

    user_progress = progress.get(st.session_state.username, {})

    if choice == "Home":
        st.markdown("### \U0001F30C Welcome to the E Learning Platform!")
        for course, desc in courses.items():
            percent = user_progress.get(course, 0)
            st.markdown(f"""
                <div class='course-card'>
                    <b>{course}</b><br>
                    {desc}<br>
                    Progress: {percent}%
                </div>
            """, unsafe_allow_html=True)

    elif choice == "Courses":
        st.subheader("\U0001F4DA Explore Our Courses")
        for course, desc in courses.items():
            with st.expander(course):
                st.write(desc)
                current_progress = user_progress.get(course, 0)
                new_progress = st.slider(f"Update Progress - {course}", 0, 100, current_progress, key=f"{course}_slider")
                if new_progress != current_progress:
                    user_progress[course] = new_progress
                    progress[st.session_state.username] = user_progress
                    save_progress(progress)
                    st.success(f"\u2705 Progress updated for {course}!")

    elif choice == "Video Lessons":
        st.subheader("\U0001F3A5 AI Video Lessons")

        video_links = {
            "Python Basics": "https://www.youtube.com/watch?v=rfscVS0vtbw",
            "Data Science": "https://www.youtube.com/watch?v=ua-CiDNNj30",
            "Machine Learning": "https://www.youtube.com/watch?v=GwIo3gDZCVQ",
            "AI for Beginners": "https://www.youtube.com/watch?v=Yq0QkCxoTHM",
            "Deep Learning": "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi",
            "Computer Vision": "https://www.youtube.com/watch?v=lgbKpn7q40M",
            "Natural Language Processing": "https://www.youtube.com/watch?v=dIUTsFT2MeQ",
            "Reinforcement Learning": "https://www.youtube.com/watch?v=2pWv7GOvuf0",
            "AI Ethics": "https://www.youtube.com/watch?v=UwsrzCVZAb8",
            "Genarative AI": "https://www.youtube.com/watch?v=hHnvo4f35GA"
        }

        for title, link in video_links.items():
            st.markdown(f"#### \U0001F539 {title}")
            if "playlist" in link:
                st.markdown(f"[\U0001F3AC Watch Playlist]({link})", unsafe_allow_html=True)
            else:
                st.video(link)
            current_progress = user_progress.get(title, 0)
            if current_progress < 10:
                user_progress[title] = 10
                progress[st.session_state.username] = user_progress
                save_progress(progress)
                st.info(f"\U0001F4C8 Progress updated to 10% for {title}")

    elif choice == "Assignments":
        st.subheader("\U0001F4DD Assignments")
        assignment = st.selectbox("Select a Course", list(courses.keys()))
        st.write(f"### Assignment for {assignment}")
        uploaded_file = st.file_uploader("📤 Upload your assignment", type=["pdf", "ipynb"])
        if uploaded_file:
            st.success("\u2705 Assignment submitted successfully!")
            current_progress = user_progress.get(assignment, 0)
            if current_progress < 70:
                user_progress[assignment] = max(current_progress, 70)
                progress[st.session_state.username] = user_progress
                save_progress(progress)
                st.info(f"\U0001F4C8 Progress updated to {user_progress[assignment]}% for {assignment}")

    elif choice == "Quiz":
        st.subheader("\U0001F9E0 Quick Quiz")
        questions = {
            "Python Basics": [
                ("What is the output of print(2 * 3)?", ["5", "6", "8", "9"], "6", "Basic multiplication in Python.")
            ],
            "Data Science": [
                ("Which library is commonly used for data manipulation?", ["NumPy", "Pandas", "Flask"], "Pandas", "Pandas provides powerful dataframes.")
            ]
        }
        subject = st.selectbox("Select Subject", list(questions.keys()))
        qlist = questions[subject]
        question, options, correct, explanation = random.choice(qlist)
        user_answer = st.radio(question, options)
        if st.button("✅ Submit Answer", key="submit_answer_btn"):
            user = st.session_state.username
            result = "Correct" if user_answer == correct else "Incorrect"
            st.session_state.quiz_count += 1
            quiz_log.setdefault(user, []).append({
                "subject": subject,
                "question": question,
                "your_answer": user_answer,
                "correct_answer": correct,
                "result": result,
                "explanation": explanation
            })
            save_quiz_log(quiz_log)
            current_progress = user_progress.get(subject, 0)
            if current_progress < 50:
                new_progress = min(current_progress + 10, 50)
                user_progress[subject] = new_progress
                progress[st.session_state.username] = user_progress
                save_progress(progress)
                st.info(f"\U0001F4C8 Progress updated to {new_progress}% for {subject}")
            if result == "Correct":
                st.success("\u2705 Correct!")
            else:
                st.error("\u274C Incorrect")
                st.info(f"\U0001F4D8 Explanation: {explanation}")

        if st.session_state.quiz_count >= 15:
            st.success("\U0001F389 You can now submit the final quiz")
            if st.button("🚀 Final Submit", key="final_submit_btn"):
                st.balloons()
                st.success("\U0001F393 Final submission done! Congrats!")
                current_progress = user_progress.get(subject, 0)
                if current_progress < 100:
                    user_progress[subject] = 100
                    progress[st.session_state.username] = user_progress
                    save_progress(progress)
                    st.info(f"\U0001F973 Final progress set to 100% for {subject}")
        else:
            st.warning(f"\U0001F4CA You have completed {st.session_state.quiz_count} quizzes. 15 required to submit.")

    elif choice == "Review Answers":
        st.subheader("\U0001F4CB Quiz Review")
        user_logs = quiz_log.get(st.session_state.username, [])
        filter_option = st.selectbox("Filter", ["All", "Correct", "Incorrect"])
        for entry in user_logs:
            if filter_option == "All" or entry["result"] == filter_option:
                st.markdown(f"""
                **Subject:** {entry['subject']}  
                **Q:** {entry['question']}  
                **Your Answer:** {entry['your_answer']}  
                **Correct Answer:** {entry['correct_answer']}  
                **Result:** {entry['result']}  
                **Explanation:** {entry['explanation']}  
                ---
                """)

    elif choice == "Dashboard":
        st.subheader("\U0001F4CA Course Progress Dashboard")
        for course in courses:
            percent = user_progress.get(course, 0)
            st.progress(percent / 100.0, text=course)

    elif choice == "Profile":
        st.subheader("\U0001F464 Profile")
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        if st.button("👤 Save Profile", key="save_profile_btn"):
            if name and email:
                st.success(f"✅ Profile saved for {name}!")
            else:
                st.warning("⚠️ Please fill in all fields.")
