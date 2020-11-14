from transformers import BartForConditionalGeneration

# dataloader

# 1. preprocess the data with bart tokenizer and the embedding matrix
# 2. store the preprocessed data on disk in a .pckl file
# 3. create a dataloader that loads the data from disk to memory on-demand

# fine tune

# 1. instantiate the model
model = BartForConditionalGeneration.from_pretrained("facebook/bart-base")
# 2. get the training dataloader
# 3. create an optimizer
# 4. enumerate in batches over the training dataloader
# 5. training loop
# 6. save the model checkpoint after each epoch

# evaluate

# 1. load the model checkpoint
# 2. load the validation dataloader
# 3. evaluate the model on the val set
