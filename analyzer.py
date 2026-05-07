import re

import os

# 🔹 predefined important skills
SKILLS = [
    "python", "java", "c++", "html", "css", "javascript",
    "react", "django", "flask", "sql", "machine learning",
    "data analysis", "git", "github", "docker", "aws", "azure",
    "tensorflow", "pytorch", "node.js", "typescript", "mongodb"
]

def clean_text(text):
    text = text.lower()
    return set(re.findall(r'\b[a-z0-9+#.]+\b', text))

def extract_skills(text):
    words = clean_text(text)
    found_skills = [skill for skill in SKILLS if skill in text.lower()]
    return set(found_skills)

def analyze_resume_local(resume_text, job_desc):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_desc)

    matched = resume_skills.intersection(job_skills)
    missing = job_skills - resume_skills

    score = int((len(matched) / len(job_skills)) * 100) if job_skills else 0
    
    result = {
        "score": score,
        "matched": list(matched),
        "missing": list(missing),
        "suggestions": "Consider adding the missing skills to your resume if you have experience with them."
    }
    return score, result

def analyze_resume_ai(resume_text, job_desc, api_key):
    
    prompt = f"""
    Analyze the resume against the job description.
    Resume: {resume_text[:4000]}
    Job Description: {job_desc[:2000]}
    Return JSON: {{"score": 0-100, "matched": [], "missing": [], "strengths": [], "suggestions": []}}
    """
    try:
       
     
        import json
        
       
    except Exception as e:
        return 0, {"error": str(e)}

def analyze_resume(resume_text, job_desc, api_key=None):
    if api_key:
        return analyze_resume_ai(resume_text, job_desc, api_key)
    return analyze_resume_local(resume_text, job_desc)