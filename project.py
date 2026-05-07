# pyrefly: ignore [missing-import]
from transformers import AutoTokenizer

# pyrefly: ignore [missing-import]
from transformers import AutoModelForSequenceClassification
# pyrefly: ignore [missing-import]
import torch
import os

# Absolute path to your trained model
from transformers import pipeline

MODEL_NAME = "YOUR_USERNAME/resume-analyzer-model"

classifier = pipeline(
    "text-classification",
    model=MODEL_NAME,
    tokenizer=MODEL_NAME
)

def predict_category(text):
    result = classifier(text)
    return result[0]["label"]

# Check if model folder exists
if not os.path.exists(MODEL_PATH):
    raise Exception(f"Model folder not found: {MODEL_PATH}")

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

# Labels
labels = {
    0: "Data Science",
    1: "Web Development",
    2: "Android Development",
    3: "HR",
    4: "Testing",
    5: "DevOps",
    6: "Cyber Security"
}


def predict_category(text):

    inputs = tokenizer(
        text,
        truncation=True,
        padding=True,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model(**inputs)

    prediction = torch.argmax(outputs.logits, dim=1).item()

    return labels.get(prediction, "Unknown")