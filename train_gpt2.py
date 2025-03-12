from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd

# Load dataset
df = pd.read_csv("api/dreamcrafter_dataset.csv")
prompts = df["Prompt"].tolist()

# Prepare dataset for GPT-2
dataset = Dataset.from_dict({"text": prompts})
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token  # Set pad token to eos_token

# Tokenize and prepare inputs with labels
def tokenize_function(examples):
    encodings = tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)
    # Labels are the same as input_ids for language modeling
    encodings["labels"] = encodings["input_ids"].copy()
    return encodings

tokenized_dataset = dataset.map(tokenize_function, batched=True)
train_dataset = tokenized_dataset.shuffle(seed=42).select(range(len(prompts)))

# Remove unnecessary columns (e.g., "text") to match expected format
train_dataset = train_dataset.remove_columns(["text"])

# Load model
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Training arguments
training_args = TrainingArguments(
    output_dir="./gpt2_dreamcrafter",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    save_steps=500,
    save_total_limit=2,
    logging_steps=10,
    eval_strategy="no",  # Updated from evaluation_strategy to avoid warning
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

# Train
trainer.train()

# Save model
model.save_pretrained("./gpt2_dreamcrafter")
tokenizer.save_pretrained("./gpt2_dreamcrafter")