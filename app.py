# pyrefly: ignore [missing-import]
import streamlit as st
import os
# pyrefly: ignore [missing-import]
import docx
# pyrefly: ignore [missing-import]
import PyPDF2
# pyrefly: ignore [missing-import]
import pytesseract
# pyrefly: ignore [missing-import]
from PIL import Image
import re
# pyrefly: ignore [missing-import]
from transformers import pipeline

# =========================
# PAGE CONFIG (PRO UI)
# =========================
st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide",
    page_icon="📄"
)

# =========================
# CUSTOM UI STYLE
# =========================
st.markdown("""
<style>
    .main-title {
        font-size:40px;
        font-weight:700;
        color:#4B8BBE;
        text-align:center;
    }
    .sub-title {
        font-size:18px;
        text-align:center;
        color:gray;
    }
    .box {
        padding:15px;
        border-radius:10px;
        background-color:#f5f7fa;
        margin-bottom:10px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# AUTH SYSTEM
# =========================
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None


def signup(username, password):
    if username in st.session_state.users:
        return False
    st.session_state.users[username] = password
    return True


def login(username, password):
    if username in st.session_state.users and st.session_state.users[username] == password:
        st.session_state.logged_in = True
        st.session_state.current_user = username
        return True
    return False


def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None


# =========================
# LOAD AI MODEL
# =========================
@st.cache_resource
def load_model():
    return pipeline("text-classification", model="my_model")

classifier = load_model()


# =========================
# TEXT EXTRACTION FUNCTIONS
# =========================
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return "".join([page.extract_text() or "" for page in reader.pages])


def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])


def extract_text_from_image(file):
    image = Image.open(file)
    return pytesseract.image_to_string(image)


# =========================
# TEXT CLEANING (FIX #1)
# =========================
def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+# ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


# =========================
# CHUNKING (NO TRUNCATION)
# =========================
def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]


# =========================
# SKILL DATABASE (FIX #2)
# =========================
SKILLS_DB = [
    "python", "java", "c++", "c#", "javascript", "typescript",
    "machine learning", "deep learning", "nlp", "ai",
    "data science", "data analysis", "sql", "mysql", "postgresql",
    "excel", "power bi", "tableau",
    "tensorflow", "pytorch", "keras",
    "flask", "django", "fastapi",
    "streamlit", "git", "github",
    "docker", "kubernetes",
    "html", "css", "react", "node", "express",
    "communication", "teamwork", "problem solving"
]


# =========================
# SKILL EXTRACTION (FIX #3)
# =========================
def extract_skills(text):
    text = normalize_text(text)
    found = []

    for skill in SKILLS_DB:
        if normalize_text(skill) in text:
            found.append(skill)

    return list(set(found))


# =========================
# JOB SKILL EXTRACTION (FIX #4)
# =========================
def extract_job_skills(job_text):
    return extract_skills(job_text)


# =========================
# MATCHING ENGINE (FIX #5)
# =========================
def match_skills(resume_skills, job_skills):
    resume_skills = set(resume_skills)
    job_skills = set(job_skills)

    matched = resume_skills & job_skills
    missing = job_skills - resume_skills

    score = (len(matched) / len(job_skills)) * 100 if job_skills else 0

    return list(matched), list(missing), round(score, 2)


# =========================
# AI PREDICTION (CHUNK SAFE)
# =========================
def predict(text):
    chunks = chunk_text(text)
    results = []

    for chunk in chunks:
        results.append(classifier(chunk)[0])

    return results


# =========================
# LOGIN PAGE UI
# =========================
if not st.session_state.logged_in:

    st.markdown('<div class="main-title">📄 AI Resume Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Smart ATS-style Resume Matching System</div>', unsafe_allow_html=True)

    option = st.radio("Choose Option", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Signup":
        if st.button("Create Account"):
            if signup(username, password):
                st.success("Account created successfully!")
            else:
                st.error("User already exists!")

    if option == "Login":
        if st.button("Login"):
            if login(username, password):
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

# =========================
# MAIN APP
# =========================
else:
    st.sidebar.success(f"Logged in as {st.session_state.current_user}")

    if st.sidebar.button("Logout"):
        logout()
        st.rerun()

    st.markdown('<div class="main-title">📄 Resume Analyzer Dashboard</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "png", "jpg", "jpeg"])

    with col2:
        job_desc = st.text_area("Paste Job Description")

    if uploaded_file:

        file_type = uploaded_file.name.split(".")[-1]

        if file_type == "pdf":
            text = extract_text_from_pdf(uploaded_file)
        elif file_type == "docx":
            text = extract_text_from_docx(uploaded_file)
        else:
            text = extract_text_from_image(uploaded_file)

        st.subheader("📄 Resume Preview")
        st.write(text[:1500])

        # =========================
        # SKILL PROCESSING (FIXED)
        # =========================
        resume_skills = extract_skills(text)
        job_skills = extract_job_skills(job_desc)

        matched, missing, score = match_skills(resume_skills, job_skills)

        # =========================
        # RESULTS UI
        # =========================
        st.markdown("## 🧠 Skill Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🎯 Match Score", f"{score}%")

        with col2:
            st.success(f"Matched Skills: {len(matched)}")

        with col3:
            st.error(f"Missing Skills: {len(missing)}")

        st.markdown("### ✔ Matched Skills")
        st.write(matched if matched else "None")

        st.markdown("### ❌ Missing Skills")
        st.write(missing if missing else "None")

        # =========================
        # AI MODEL OUTPUT
        # =========================
        st.markdown("## 🤖 AI Analysis Result")

        predictions = predict(text)

        for i, p in enumerate(predictions):
            st.info(f"Chunk {i+1}: {p}")
