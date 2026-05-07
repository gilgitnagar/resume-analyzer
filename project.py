# pyrefly: ignore [missing-import]
from transformers import pipeline
# pyrefly: ignore [missing-import]
import streamlit as st

MODEL_NAME = "aqibhussain/resume-analyzer-model"

@st.cache_resource
def load_classifier():
    classifier = pipeline(
        "text-classification",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME
    )
    return classifier

try:
    classifier = load_classifier()
except Exception as e:
    classifier = None

def predict_category(text):
    if classifier is None:
        return "Unknown"
    try:
        result = classifier(text)
        return result[0]["label"]
    except Exception:
        return "Unknown"