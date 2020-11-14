from typing import Any, Dict

import datasets
from transformers import BartForConditionalGeneration, BartTokenizer
from transformers.modeling_bart import shift_tokens_right

from . import disk


# 1. preprocess the data with bart tokenizer and the embedding matrix
def convert_to_features(example_batch: Dict[str, Any]) -> Dict[str, Any]:
    input_encodings = tokenizer.batch_encode_plus(
        example_batch["utterance"],
        max_length=128,
        truncation=True,
        padding="longest",
        return_tensors="pt",
    )
    target_encodings = tokenizer.batch_encode_plus(
        example_batch["code"],
        max_length=128,
        truncation=True,
        padding="longest",
        return_tensors="pt",
    )

    labels = target_encodings["input_ids"]
    decoder_input_ids = shift_tokens_right(labels, model.config.pad_token_id)
    labels[labels[:, :] == model.config.pad_token_id] = -100

    encodings = {
        "input_ids": input_encodings["input_ids"].numpy().copy(),
        "attention_mask": input_encodings["attention_mask"].numpy().copy(),
        "decoder_input_ids": decoder_input_ids.numpy().copy(),
        "labels": labels.numpy().copy(),
    }

    return encodings


# 2. store the preprocessed data on disk in a .pckl file
# 3. create a dataloader that loads the data from disk to memory on-demand


if __name__ == "__main__":
    dataset = datasets.load_dataset(
        "json",
        data_files={
            "train": "./data-versioned/v0.1/generated/train.json",
            "test": "./data-versioned/v0.1/generated/test.json",
            "validation": "./data-versioned/v0.1/generated/validation.json",
        },
    )

    tokenizer = BartTokenizer.from_pretrained("facebook/bart-base")
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-base")

    dataset = dataset.map(convert_to_features, batched=True)

    columns = ["input_ids", "labels", "decoder_input_ids", "attention_mask"]
    dataset.set_format(type="torch", columns=columns)

    dataset.save_to_disk(disk.UNVERSIONED_DATA_DIR / "features")
