# pyrefly: ignore [missing-import]
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

MODEL_NAME = "aqibhussain/resume-analyzer-model"

@staticmethod
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

    classifier = pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer
    )

    return classifier