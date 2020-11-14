import datasets
from transformers import BartForConditionalGeneration, BartTokenizer

from . import disk

dataset = datasets.load_from_disk(disk.UNVERSIONED_DATA_DIR / "features")
example = dataset["test"][0:5]

model = BartForConditionalGeneration.from_pretrained("./models/bart-coder")
tokenizer = BartTokenizer.from_pretrained("facebook/bart-base")


summary_ids = model.generate(
    example["input_ids"], min_length=3, num_beams=4, early_stopping=True
)

print(
    [
        tokenizer.decode(
            g, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        for g in example["input_ids"]
    ]
)

print(
    [
        tokenizer.decode(
            g, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        for g in summary_ids
    ]
)

print(
    [
        tokenizer.decode(
            g, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        for g in example["decoder_input_ids"]
    ]
)


def predict(utterance: str) -> str:
    input_encodings = tokenizer.batch_encode_plus(
        [utterance],
        max_length=128,
        truncation=True,
        padding="longest",
        return_tensors="pt",
    )

    code_ids = model.generate(
        input_encodings["input_ids"], min_length=3, num_beams=4, early_stopping=True
    )

    print(
        [
            tokenizer.decode(
                g, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )
            for g in code_ids
        ]
    )
