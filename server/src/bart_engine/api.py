from typing import List

from transformers import BartForConditionalGeneration, BartTokenizer


class BartEngine:
    def __init__(self):
        self.model = BartForConditionalGeneration.from_pretrained("./models/bart-coder")
        self.tokenizer = BartTokenizer.from_pretrained("facebook/bart-base")

    def preprocess(self, text: str) -> str:
        return (
            text.lower()
            .replace("+", "plus")
            .replace("*", "times")
            .replace("-", "minus")
        )

    def predict_batch(self, utterances: List[str]) -> List[List[str]]:
        utterances = [self.preprocess(u) for u in utterances]
        input_encodings = self.tokenizer.batch_encode_plus(
            utterances,
            max_length=32,
            truncation=True,
            padding="longest",
            return_tensors="pt",
        )

        code_ids = self.model.generate(
            input_encodings["input_ids"], min_length=3, num_beams=4, early_stopping=True
        )

        result: List[List[str]] = [
            self.tokenizer.decode(
                g, skip_special_tokens=True, clean_up_tokenization_spaces=False
            ).split()
            for g in code_ids
        ]

        return result

    def predict(self, utterance: str) -> List[str]:
        if utterance.lower() in set(["tapout", "tabout", "tab out", "tap out"]):
            return ["tabout"]
        return self.predict_batch([utterance])[0]
