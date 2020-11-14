import datasets
from transformers import BartForConditionalGeneration, Trainer, TrainingArguments

from . import disk

# load data

dataset = datasets.load_from_disk(disk.UNVERSIONED_DATA_DIR / "features")


# fine tune


# 1. instantiate the model
def train() -> None:
    raise NotImplementedError()


def sanity_check() -> None:
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-base")

    training_args = TrainingArguments(
        output_dir="./models/bart-coder",
        num_train_epochs=5,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="./logs",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"].select(range(5)),
        eval_dataset=dataset["validation"].select(range(5)),
    )

    trainer.train()
    trainer.save_model()
    print(trainer.evaluate())


if __name__ == "__main__":
    sanity_check()
