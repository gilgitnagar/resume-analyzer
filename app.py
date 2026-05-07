# pyrefly: ignore [missing-import]
import streamlit as st
import os
import pandas as pd
# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
from model_utils import load_model

st.title("Resume Analyzer")

@st.cache_resource
def get_model():
    return load_model()

classifier = get_model()

text = st.text_area("Paste Resume Text")

if st.button("Analyze"):
    if text:
        result = classifier(text)
        st.write(result)
from database import engine, SessionLocal
from models import Base, ResumeData

from auth import register_user, login_user

from parser import (
    extract_text,
    extract_skills,
    extract_name,
    calculate_ats_score,
    extract_missing_skills,
    generate_suggestions
)

from project import predict_category


# =========================
# DATABASE
# =========================
Base.metadata.create_all(bind=engine)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================
# SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# =========================
# CUSTOM CSS
# =========================
st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(to right, #141E30, #243B55);
        color: white;
    }

    h1,h2,h3,h4 {
        color: white;
    }

    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        border: none;
    }

    .stTextInput>div>div>input {
        border-radius: 10px;
    }

    .metric-box {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# NOT LOGGED IN
# =========================
if not st.session_state.logged_in:

    st.title("📄 AI Resume Analyzer")

    st.subheader(
        "Smart ATS Resume Screening System"
    )

    st.markdown("---")

    menu = ["Login", "Register"]

    choice = st.sidebar.selectbox(
        "Navigation",
        menu
    )

    # =====================
    # REGISTER
    # =====================
    if choice == "Register":

        st.header("📝 Create Account")

        username = st.text_input("👤 Username")

        password = st.text_input(
            "🔒 Password",
            type="password"
        )

        if st.button("Register"):

            if username == "" or password == "":
                st.warning(
                    "Please fill all fields"
                )

            else:

                db = SessionLocal()

                success = register_user(
                    db,
                    username,
                    password
                )

                if success:

                    st.success(
                        "✅ Account Created Successfully"
                    )

                    st.balloons()

                else:

                    st.error(
                        "❌ Username Already Exists"
                    )

    # =====================
    # LOGIN
    # =====================
    elif choice == "Login":

        st.header("🔐 Login")

        username = st.text_input(
            "👤 Username"
        )

        password = st.text_input(
            "🔒 Password",
            type="password"
        )

        if st.button("Login"):

            db = SessionLocal()

            success = login_user(
                db,
                username,
                password
            )

            if success:

                st.session_state.logged_in = True

                st.session_state.username = username

                st.rerun()

            else:

                st.error(
                    "❌ Invalid Username or Password"
                )


# =========================
# DASHBOARD
# =========================
else:

    st.sidebar.success(
        f"Logged in as {st.session_state.username}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False

        st.session_state.username = ""

        st.rerun()

    st.title("📊 Resume Analyzer Dashboard")

    st.markdown("---")

    # =====================
    # JOB DESCRIPTION
    # =====================
    job_description = st.text_area(
        "📋 Paste Job Description",
        height=200
    )

    # =====================
    # UPLOAD RESUME
    # =====================
    uploaded_file = st.file_uploader(
        "📤 Upload Resume PDF",
        type=["pdf"]
    )

    # =====================
    # ANALYZE BUTTON
    # =====================
    if st.button("Analyze Resume"):

        if uploaded_file is None:

            st.error(
                "Please upload resume"
            )

        elif job_description.strip() == "":

            st.error(
                "Please paste job description"
            )

        else:

            save_path = os.path.join(
                UPLOAD_FOLDER,
                uploaded_file.name
            )

            with open(save_path, "wb") as f:

                f.write(
                    uploaded_file.getbuffer()
                )

            with st.spinner(
                "Analyzing Resume..."
            ):

                # Extract text
                text = extract_text(save_path)

                # Extract details
                name = extract_name(text)

                skills = extract_skills(text)

                category = predict_category(text)

                # ATS
                ats_score = calculate_ats_score(
                    text,
                    job_description
                )

                missing_skills = (
                    extract_missing_skills(
                        skills,
                        job_description
                    )
                )

                suggestions = (
                    generate_suggestions(
                        ats_score
                    )
                )

            st.success(
                "✅ Resume Analysis Completed"
            )

            st.markdown("---")

            # =================
            # RESULTS
            # =================
            col1, col2 = st.columns(2)

            with col1:

                st.info(
                    f"👤 Name: {name}"
                )

                st.success(
                    f"💼 Category: {category}"
                )

            with col2:

                st.metric(
                    "📊 ATS Score",
                    f"{ats_score}%"
                )

            # =================
            # SKILLS
            # =================
            st.subheader(
                "🛠 Extracted Skills"
            )

            if skills:

                for skill in skills:
                    st.write(f"✅ {skill}")

            else:

                st.warning(
                    "No skills detected"
                )

            # =================
            # MISSING SKILLS
            # =================
            st.subheader(
                "❌ Missing Skills"
            )

            if missing_skills:

                for skill in missing_skills:
                    st.write(f"⚠ {skill}")

            else:

                st.success(
                    "No Missing Skills"
                )

            # =================
            # SUGGESTIONS
            # =================
            st.subheader(
                "💡 Suggestions"
            )

            for suggestion in suggestions:
                st.write(f"✅ {suggestion}")

            # =================
            # RESUME TEXT
            # =================
            st.subheader(
                "📄 Resume Content"
            )

            st.text_area(
                "Extracted Text",
                text,
                height=300
            )

            # =================
            # SAVE DATABASE
            # =================
            db = SessionLocal()

            db_resume = ResumeData(
                name=name,
                category=category,
                skills=", ".join(skills),
                resume_text=text
            )

            db.add(db_resume)

            db.commit()

            st.success(
                "✅ Data Saved To Database"
            )

            # =================
            # PREVIOUS RECORDS
            # =================
            st.markdown("---")

            st.header(
                "📁 Previous Records"
            )

            records = db.query(
                ResumeData
            ).all()

            data = []

            for record in records:

                data.append({

                    "ID": record.id,
                    "Name": record.name,
                    "Category": record.category,
                    "Skills": record.skills
                })

            df = pd.DataFrame(data)

            st.dataframe(
                df,
                use_container_width=True
            )