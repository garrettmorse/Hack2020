import datasets
from transformers import BartForConditionalGeneration, BartTokenizer

from . import disk

dataset = datasets.load_from_disk(disk.UNVERSIONED_DATA_DIR / "features")
example = dataset["train"][0:1]


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
        for g in summary_ids
    ]
)
