# pyrefly: ignore [missing-import]
import pdfplumber
import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# Extract Text From PDF
# =========================
def extract_text(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

    return text


# =========================
# Extract Skills
# =========================
def extract_skills(text):

    skills_list = [

        # Programming
        "python",
        "java",
        "c++",
        "c",
        "javascript",
        "typescript",
        "php",

        # Web
        "html",
        "css",
        "react",
        "nodejs",
        "flask",
        "django",
        "bootstrap",

        # Data Science
        "machine learning",
        "deep learning",
        "nlp",
        "tensorflow",
        "pytorch",
        "pandas",
        "numpy",
        "scikit-learn",

        # Database
        "sql",
        "mysql",
        "mongodb",
        "sqlite",

        # Cloud & DevOps
        "aws",
        "docker",
        "kubernetes",
        "devops",
        "linux",

        # Other
        "streamlit",
        "git",
        "github",
        "data analysis",
        "power bi",
        "excel"
    ]

    found_skills = []

    lower_text = text.lower()

    for skill in skills_list:

        if skill.lower() in lower_text:
            found_skills.append(skill)

    return list(set(found_skills))


# =========================
# Extract Name
# =========================
def extract_name(text):

    lines = text.split("\n")

    for line in lines[:5]:

        line = line.strip()

        if len(line.split()) >= 2:
            return line

    return "Unknown"


# =========================
# ATS Score Calculation
# =========================
def calculate_ats_score(resume_text, job_description):

    if job_description.strip() == "":
        return 0

    documents = [resume_text, job_description]

    cv = CountVectorizer().fit_transform(documents)

    similarity = cosine_similarity(cv)

    score = similarity[0][1] * 100

    return round(score, 2)


# =========================
# Missing Skills Detection
# =========================
def extract_missing_skills(resume_skills, job_description):

    # Extract skills from job description
    jd_skills = extract_skills(job_description)

    # Normalize both lists
    resume_skills = set(
        skill.strip().lower()
        for skill in resume_skills
    )

    jd_skills = set(
        skill.strip().lower()
        for skill in jd_skills
    )

    # Find missing skills
    missing_skills = list(
        jd_skills - resume_skills
    )

    return missing_skills


# =========================
# Resume Suggestions
# =========================
def generate_suggestions(score):

    suggestions = []

    if score < 40:

        suggestions.append(
            "Add more relevant technical skills"
        )

        suggestions.append(
            "Improve resume formatting"
        )

        suggestions.append(
            "Add project experience"
        )

        suggestions.append(
            "Include certifications"
        )

        suggestions.append(
            "Use keywords from job description"
        )

    elif score < 70:

        suggestions.append(
            "Optimize resume keywords"
        )

        suggestions.append(
            "Add measurable achievements"
        )

        suggestions.append(
            "Improve project descriptions"
        )

    else:

        suggestions.append(
            "Resume is highly optimized"
        )

        suggestions.append(
            "Resume matches job description well"
        )

    return suggestions 