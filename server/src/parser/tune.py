import argparse

import datasets
import torch
from transformers import BartForConditionalGeneration, Trainer, TrainingArguments

from . import disk

# load data

dataset = datasets.load_from_disk(disk.UNVERSIONED_DATA_DIR / "features")


# fine tune

device = torch.device("cuda") if torch.cuda.is_available else torch.device("cpu")  # type: ignore

# 1. instantiate the model
def train(cli_args: argparse.Namespace) -> None:
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-base")
    model.to(device)

    training_args = TrainingArguments(
        output_dir="./models/bart-coder",
        num_train_epochs=cli_args.epochs,
        per_device_train_batch_size=128,
        per_device_eval_batch_size=128,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="./logs",
        fp16=True,
        remove_unused_columns=True,
        dataloader_num_workers=4,
    )

    print("training on:", training_args.device)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
    )

    trainer.train()
    trainer.save_model()
    print(trainer.evaluate())


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Tune a BART model on code generation.")
    parser.add_argument("--epochs", type=int, help="number of epochs to train for")
    args = parser.parse_args()

    train(args)
