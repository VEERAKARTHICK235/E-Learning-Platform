import streamlit as st
import hashlib
import json
import os
import random

# Initialize app configuration
st.set_page_config(page_title="AI E-Learning", layout="centered")

# File paths for data storage
USER_DB_FILE = "users.json"
PROGRESS_DB_FILE = "progress.json"
QUIZ_LOG_FILE = "quiz_log.json"

# Initialize JSON files if they don't exist
for file in [USER_DB_FILE, PROGRESS_DB_FILE, QUIZ_LOG_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump({}, f)

# Data loading functions with error handling
def load_users():
    try:
        with open(USER_DB_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    try:
        with open(USER_DB_FILE, "w") as file:
            json.dump(users, file)
    except Exception as e:
        st.error(f"Error saving user data: {e}")

def load_progress():
    try:
        with open(PROGRESS_DB_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_progress(progress):
    try:
        with open(PROGRESS_DB_FILE, "w") as file:
            json.dump(progress, file)
    except Exception as e:
        st.error(f"Error saving progress data: {e}")

def load_quiz_log():
    try:
        with open(QUIZ_LOG_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_quiz_log(log):
    try:
        with open(QUIZ_LOG_FILE, "w") as file:
            json.dump(log, file)
    except Exception as e:
        st.error(f"Error saving quiz log: {e}")

# Load initial data
users = load_users()
progress = load_progress()
quiz_log = load_quiz_log()

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "quiz_count" not in st.session_state:
    st.session_state.quiz_count = 0

# Authentication UI
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
                st.rerun()
            else:
                st.error("\u274C Invalid username or password")

    with signup_tab:
        new_username = st.text_input("Create Username")
        new_password = st.text_input("Create Password", type="password")
        if st.button("🆕 Signup", key="signup_btn"):
            if new_username in users:
                st.warning("\u26A0\uFE0F Username already exists.")
            elif not new_username or not new_password:
                st.warning("Please enter both username and password")
            else:
                users[new_username] = hash_password(new_password)
                save_users(users)
                st.success("\U0001F389 Signup successful! You can log in now.")
else:
    # Main application after login
    st.sidebar.write(f"\U0001F44B Hello, {st.session_state.username}")
    if st.sidebar.button("🚪 Logout", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # Custom CSS styling
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

    # Application menu
    menu = ["Home", "Courses", "Video Lessons", "Assignments", "Quiz", "Review Answers", "Dashboard", "Profile"]
    choice = st.sidebar.selectbox("📚 Navigate", menu)

    # Course data
    courses = {
        "Python Basics": "Learn Python from scratch",
        "Data Science": "Explore data analysis techniques",
        "Machine Learning": "Understand ML algorithms",
        "AI for Beginners": "Introduction to AI",
        "Deep Learning": "Dive into deep neural networks",
        "Computer Vision": "Master image processing",
        "Natural Language Processing": "Work with text data",
        "Reinforcement Learning": "Learn agent-based learning",
        "The Ethics of AI & ML": "Understand ethical implications",
        "Generative AI": "Understanding the Gen AI"
    }

    user_progress = progress.get(st.session_state.username, {})

    # Menu options
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
            "AI for Beginners": "https://www.youtube.com/watch?v=JMUxmLyrhSk",
            "Deep Learning": "https://www.youtube.com/watch?v=DooxDIRAkPA",
            "Computer Vision": "https://www.youtube.com/watch?v=01sAkU_NvOY",
            "Natural Language Processing": "https://www.youtube.com/watch?v=dIUTsFT2MeQ",
            "Reinforcement Learning": "https://www.youtube.com/watch?v=ELE2_Mftqoc",
            "The Ethics of AI & ML": "https://www.youtube.com/watch?v=qpp1G0iEL_c",
            "Generative AI": "https://www.youtube.com/watch?v=hHnvo4f35GA"
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
                ("What is the output of print(2 * 3)?", ["5", "6", "8", "9"], "6", "Basic multiplication in Python."),
                ("Which keyword defines a function in Python?", ["func", "def", "function", "define"], "def", "Python uses 'def' to define functions."),
                ("What does list.append() do?", ["Adds an item to the end", "Removes an item", "Sorts the list", "Reverses the list"], "Adds an item to the end", "Append adds items to the end of a list."),
                ("Which of these is a valid variable name?", ["2var", "_var", "var!", "#var"], "_var", "Variable names can't start with numbers or symbols."),
                ("How do you start a comment in Python?", ["#", "//", "/*", "--"], "#", "Python uses '#' for single-line comments."),
                ("What data type is [1, 2, 3]?", ["List", "Tuple", "Dict", "Set"], "List", "Square brackets represent lists."),
                ("What does len() return?", ["Length", "Last element", "Line number", "None"], "Length", "len() returns the number of items."),
                ("What is the output of bool('False')?", ["False", "True"], "True", "Non-empty strings are truthy."),
                ("Which keyword is used to loop?", ["for", "while", "repeat", "loop"], "for", "Python uses 'for' and 'while' to loop."),
                ("What does 'break' do?", ["Exits loop", "Skips iteration", "Repeats loop"], "Exits loop", "'break' exits the loop early.")
            ],
            "Data Science": [
                ("Which library is used for data manipulation?", ["NumPy", "Pandas", "Flask"], "Pandas", "Pandas provides powerful dataframes."),
                ("What does .head() do?", ["Shows first rows", "Last rows", "Data types"], "Shows first rows", "Displays the first few rows."),
                ("What is NaN?", ["A number", "Missing value", "String"], "Missing value", "NaN means missing data."),
                ("Which file format is common in DS?", [".csv", ".exe", ".bin"], ".csv", "CSV files are widely used."),
                ("How do you import Pandas?", ["import pandas", "load pandas", "install pandas"], "import pandas", "Use import to bring in libraries."),
                ("What is df.shape?", ["Rows & columns", "File size", "Data types"], "Rows & columns", "Shows dimensions."),
                ("What does describe() return?", ["Stats summary", "Graph", "Null values"], "Stats summary", "Gives mean, std, etc."),
                ("Which is not a plot type?", ["bar", "line", "circle"], "circle", "Circle is not standard."),
                ("What is outlier?", ["Normal data", "Unusual value"], "Unusual value", "Outliers lie far from average."),
                ("Which method fills NaN?", ["fillna()", "replace()", "dropna()"], "fillna()", "fillna() replaces NaNs.")
            ],
            "Machine Learning": [
                ("What is supervised learning?", ["With labels", "Without guidance"], "With labels", "Uses labeled training data."),
                ("What is overfitting?", ["Fits training too well", "Fits test only"], "Fits training too well", "It memorizes instead of generalizes."),
                ("Which lib is for ML?", ["Scikit-learn", "Django", "Tkinter"], "Scikit-learn", "sklearn is ML library."),
                ("What is model accuracy?", ["Correct predictions %", "Data size"], "Correct predictions %", "Percentage of right answers."),
                ("Which algorithm is for classification?", ["KNN", "K-Means"], "KNN", "KNN is for classification."),
                ("Purpose of train_test_split?", ["Evaluate performance", "Plot graph"], "Evaluate performance", "Splits data into sets."),
                ("Which term means input features?", ["X", "Y", "Z"], "X", "'X' is used for features."),
                ("Y in ML usually stands for?", ["Target", "Feature", "Label"], "Target", "Y is your label/output."),
                ("Which is unsupervised?", ["K-Means", "Decision Tree"], "K-Means", "K-Means is for clustering."),
                ("What does 'fit()' do?", ["Trains model", "Evaluates"], "Trains model", "fit() is used to train.")
            ],
            "AI for Beginners": [
                ("What does AI stand for?", ["Artificial Intelligence", "Actual Interface"], "Artificial Intelligence", "AI = Artificial Intelligence."),
                ("What is goal of AI?", ["Mimic humans", "Replace humans"], "Mimic humans", "AI tries to mimic cognitive abilities."),
                ("Which is a type of AI?", ["Narrow AI", "Perfect AI"], "Narrow AI", "Narrow AI is task-specific."),
                ("What is Turing Test?", ["Test AI thinking", "Test memory"], "Test AI thinking", "Checks if AI mimics human."),
                ("AI uses which data type?", ["Structured", "Unstructured", "Both"], "Both", "AI uses all data types."),
                ("What is intelligent agent?", ["Entity that perceives & acts", "Robot only"], "Entity that perceives & acts", "Agent perceives environment."),
                ("What is NLP?", ["Text analysis", "Video editing"], "Text analysis", "Natural Language Processing."),
                ("Which is a goal of NLP?", ["Understand language", "Paint pictures"], "Understand language", "NLP helps machines understand text."),
                ("AI needs data for?", ["Learning", "Guessing"], "Learning", "Data is the fuel for AI."),
                ("Which is not AI?", ["Calculator", "Chatbot"], "Calculator", "Calculator is not intelligent.")
            ],
            "Deep Learning": [
                ("DL is a subset of?", ["Machine Learning", "Data Entry"], "Machine Learning", "DL is a type of ML."),
                ("Main element in DL?", ["Neural Network", "Database"], "Neural Network", "Neural nets mimic brain."),
                ("Which is activation function?", ["ReLU", "SELECT"], "ReLU", "ReLU adds non-linearity."),
                ("What is epoch?", ["One pass through data", "Data error"], "One pass through data", "Epoch = 1 full pass."),
                ("Which DL framework?", ["TensorFlow", "Excel"], "TensorFlow", "TensorFlow helps build DL models."),
                ("DL needs?", ["High data", "Low power"], "High data", "Deep nets need lots of data."),
                ("Backpropagation is for?", ["Training weights", "Cleaning data"], "Training weights", "It updates weights."),
                ("CNN is used for?", ["Images", "Audio"], "Images", "CNN = Convolutional Neural Network."),
                ("RNN is for?", ["Sequences", "Pictures"], "Sequences", "RNNs process sequence data."),
                ("DL differs from ML in?", ["Depth", "Nothing"], "Depth", "DL uses deeper networks.")
            ],
            "Computer Vision": [
                ("What is CV?", ["Understanding images", "Reading books"], "Understanding images", "Computer Vision = image understanding."),
                ("Which lib for CV?", ["OpenCV", "Flask"], "OpenCV", "OpenCV is used for image processing."),
                ("What is image?", ["Matrix", "Text"], "Matrix", "Images are matrix of pixels."),
                ("Which layer in CNN?", ["Conv", "Dense"], "Conv", "Convolution layers detect features."),
                ("Edge detection filters?", ["Sobel", "Bubble"], "Sobel", "Sobel detects edges."),
                ("Resolution is?", ["Clarity", "Speed"], "Clarity", "High resolution = clear image."),
                ("Object detection finds?", ["Objects", "Colors only"], "Objects", "Detects what is in frame."),
                ("What is segmentation?", ["Divide image", "Enhance colors"], "Divide image", "Splits image into parts."),
                ("Image classification is?", ["Assign label", "Crop image"], "Assign label", "Tells what is in image."),
                ("Face recognition is a?", ["CV Task", "Voice Task"], "CV Task", "CV handles faces.")
            ],
            "Natural Language Processing": [
                ("NLP stands for?", ["Natural Language Processing", "Neural Language Program"], "Natural Language Processing", "NLP = language understanding."),
                ("Tokenization means?", ["Splitting text", "Joining text"], "Splitting text", "Breaks text into words."),
                ("Stopwords are?", ["Common words", "Rare words"], "Common words", "Words like 'the', 'is'."),
                ("Stemming reduces?", ["Words to root", "Words to plural"], "Words to root", "Like 'running' to 'run'."),
                ("Bag of Words is?", ["Text rep", "Word game"], "Text rep", "BoW is a model for text."),
                ("TF-IDF means?", ["Term freq-inv doc freq", "File type"], "Term freq-inv doc freq", "Scores word importance."),
                ("NLP lib in Python?", ["NLTK", "NumPy"], "NLTK", "NLTK is for text."),
                ("NER finds?", ["Named entities", "Adjectives"], "Named entities", "Names, places, etc."),
                ("POS tagging is?", ["Grammar tag", "File tag"], "Grammar tag", "Part of Speech tagging."),
                ("Lemmatization uses?", ["Dictionary", "List"], "Dictionary", "Finds proper root word.")
            ],
            "Reinforcement Learning": [
                ("RL stands for?", ["Reinforcement Learning", "Relative Logic"], "Reinforcement Learning", "RL uses reward systems."),
                ("What is agent?", ["Learner", "Server"], "Learner", "Agent acts in environment."),
                ("Reward is?", ["Feedback", "Data"], "Feedback", "Tells how good action is."),
                ("Action is?", ["Decision", "Reward"], "Decision", "Agent's choice."),
                ("Policy maps?", ["States to actions", "States to rewards"], "States to actions", "It defines behavior."),
                ("Q-value is?", ["Action value", "Quality check"], "Action value", "Q = expected return."),
                ("Environment is?", ["External system", "Code"], "External system", "Where agent acts."),
                ("Goal of RL?", ["Maximize rewards", "Minimize actions"], "Maximize rewards", "Seeks best outcomes."),
                ("What is episode?", ["Interaction run", "Script"], "Interaction run", "From start to terminal."),
                ("Exploration is?", ["Trying new", "Repeating"], "Trying new", "Explore to discover better actions.")
            ],
            "The Ethics of AI & ML": [
                ("AI ethics studies?", ["Right use", "Code bugs"], "Right use", "It's about responsible AI."),
                ("Bias in AI is?", ["Unfairness", "Feature"], "Unfairness", "Bias harms fairness."),
                ("Which is ethical?", ["Fair AI", "Spy AI"], "Fair AI", "Fairness is key."),
                ("What is transparency?", ["Explain decisions", "Confuse users"], "Explain decisions", "Users must understand AI."),
                ("Which is concern?", ["Privacy", "Coding speed"], "Privacy", "Data privacy is major issue."),
                ("Accountability means?", ["Responsibility", "Speed"], "Responsibility", "Who answers for AI."),
                ("What is fairness?", ["No discrimination", "Fast code"], "No discrimination", "AI should treat all equally."),
                ("Explainability is?", ["Explain model", "Hide model"], "Explain model", "Users must know why AI acts."),
                ("Who regulates AI?", ["Govt", "Coders only"], "Govt", "Governments are involved."),
                ("AI should be?", ["Ethical", "Unrestricted"], "Ethical", "Ethics is a must.")
            ],
            "Generative AI": [
                ("What is Gen AI?", ["Creates content", "Deletes data"], "Creates content", "Gen AI generates new data."),
                ("Example of Gen AI?", ["ChatGPT", "Excel"], "ChatGPT", "ChatGPT is generative."),
                ("Gen AI uses?", ["Deep models", "Textbooks"], "Deep models", "Uses complex models."),
                ("GANs stand for?", ["Generative Adversarial Networks", "Graphics and Networks"], "Generative Adversarial Networks", "GANs are used in Gen AI."),
                ("Which is LLM?", ["Large Language Model", "Long List"], "Large Language Model", "ChatGPT is an LLM."),
                ("Diffusion models are for?", ["Image Gen", "Text edit"], "Image Gen", "Stable Diffusion uses it."),
                ("Which creates art?", ["DALL·E", "MySQL"], "DALL·E", "DALL·E generates images."),
                ("AI hallucination is?", ["Wrong output", "Dreaming"], "Wrong output", "It makes things up."),
                ("Which model for text?", ["GPT", "CNN"], "GPT", "Generative Pre-trained Transformer."),
                ("Gen AI risks?", ["Misinformation", "Better answers"], "Misinformation", "It may generate false content.")
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
        if not user_logs:
            st.info("No quiz attempts yet")
        else:
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
