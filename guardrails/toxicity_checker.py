from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

class ToxicityDetector:
    def __init__(self):
        self.toxic_tokenizer = AutoTokenizer.from_pretrained("unitary/toxic-bert")
        self.toxic_model = AutoModelForSequenceClassification.from_pretrained("unitary/toxic-bert")

    def is_toxic(self, text: str, threshold: float = 0.8) -> bool:
        inputs = self.toxic_tokenizer(text, return_tensors="pt", truncation=True)
        outputs = self.toxic_model(**inputs)
        scores = torch.sigmoid(outputs.logits)[0]
        return any(score.item() > threshold for score in scores)

    def is_malicious(self, text: str) -> bool:
        return self.is_toxic(text)
