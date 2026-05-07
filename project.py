# pyrefly: ignore [missing-import]
from transformers import pipeline

# Hugging Face model repository
MODEL_NAME = "aqibhussain/resume-analyzer-model"

# Load classification pipeline
classifier = pipeline(
    "text-classification",
    model=MODEL_NAME,
    tokenizer=MODEL_NAME
)

# Label mapping
labels = {
    "LABEL_0": "Data Science",
    "LABEL_1": "Web Development",
    "LABEL_2": "Android Development",
    "LABEL_3": "HR",
    "LABEL_4": "Testing",
    "LABEL_5": "DevOps",
    "LABEL_6": "Cyber Security"
}


def predict_category(text):

    try:
        result = classifier(text)

        predicted_label = result[0]["label"]

        return labels.get(predicted_label, predicted_label)

    except Exception as e:
        return f"Prediction Error: {str(e)}"
