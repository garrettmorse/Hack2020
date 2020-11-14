from typing import List

from transformers import BartForConditionalGeneration, BartTokenizer

# globals required

model = None
tokenizer = None


def initialize_globals() -> None:
    global model
    global tokenizer

    model = BartForConditionalGeneration.from_pretrained("./models/bart-coder")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-base")


def predict_batch(utterances: List[str]) -> List[str]:
    assert model is not None, "Call initialize_globals before predicting"
    assert tokenizer is not None, "Call initialize_globals before predicting"
    input_encodings = tokenizer.batch_encode_plus(
        utterances,
        max_length=32,
        truncation=True,
        padding="longest",
        return_tensors="pt",
    )

    code_ids = model.generate(
        input_encodings["input_ids"], min_length=3, num_beams=4, early_stopping=True
    )

    result: List[str] = [
        tokenizer.decode(
            g, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        for g in code_ids
    ]

    return result


def predict(utterance: str) -> str:
    return predict_batch([utterance])[0]
