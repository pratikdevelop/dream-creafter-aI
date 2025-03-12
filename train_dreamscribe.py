# from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
# import pandas as pd
# from sklearn.model_selection import train_test_split
# import torch
# import numpy as np
# from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# # Load dataset
# df = pd.read_csv("/home/pc-25/Music/app-v3/api/dreamcrafter_dataset.csv")  # Match your file name
# texts = df["Text"].tolist()  # Capitalized as per your CSV
# emotion_map = {"Positive": 0, "Negative": 1, "Neutral": 2, "Bittersweet": 3}  # Multi-class mapping
# labels = df["Emotion"].map(emotion_map).tolist()

# # Tokenize
# tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
# encodings = tokenizer(texts, truncation=True, padding=True, max_length=128)

# # Dataset class
# class DreamDataset(torch.utils.data.Dataset):
#     def __init__(self, encodings, labels):
#         self.encodings = encodings
#         self.labels = labels

#     def __getitem__(self, idx):
#         item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
#         item["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)  # Long for multi-class
#         return item

#     def __len__(self):
#         return len(self.labels)

# # Split data
# train_texts, val_texts, train_labels, val_labels = train_test_split(
#     texts, labels, test_size=0.2, random_state=42  # Added random_state for reproducibility
# )
# train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
# val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=128)
# train_dataset = DreamDataset(train_encodings, train_labels)
# val_dataset = DreamDataset(val_encodings, val_labels)

# # Model (4 classes for 4 emotions)
# model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=4)

# # Compute metrics function for evaluation
# def compute_metrics(pred):
#     labels = pred.label_ids
#     preds = np.argmax(pred.predictions, axis=1)
#     precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average="weighted")
#     acc = accuracy_score(labels, preds)
#     return {
#         "accuracy": acc,
#         "f1": f1,
#         "precision": precision,
#         "recall": recall
#     }

# # Training arguments
# training_args = TrainingArguments(
#     output_dir="./dreamcrafter_results",  # Updated to match app name
#     num_train_epochs=3,
#     per_device_train_batch_size=8,
#     per_device_eval_batch_size=8,
#     warmup_steps=500,
#     weight_decay=0.01,
#     logging_dir="./logs",
#     logging_steps=10,  # Log more frequently to monitor progress
#     evaluation_strategy="epoch",  # Evaluate after each epoch
#     save_strategy="epoch",  # Save model after each epoch
#     load_best_model_at_end=True,  # Load the best model based on eval metric
#     metric_for_best_model="accuracy",  # Optimize for accuracy
# )

# # Trainer
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=train_dataset,
#     eval_dataset=val_dataset,
#     compute_metrics=compute_metrics,  # Added for performance tracking
# )

# # Train
# trainer.train()

# # Save model and tokenizer
# model.save_pretrained("./dreamcrafter_model")
# tokenizer.save_pretrained("./dreamcrafter_model")

# # Evaluate final model
# eval_results = trainer.evaluate()
# print("Evaluation results:", eval_results)


from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd

# Load dataset
df = pd.read_csv("api/dreamcrafter_dataset.csv")
prompts = df["Prompt"].tolist()

# Prepare dataset for GPT-2
dataset = Dataset.from_dict({"text": prompts})
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

tokenized_dataset = dataset.map(tokenize_function, batched=True)
train_dataset = tokenized_dataset.shuffle(seed=42).select(range(len(prompts)))

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
    evaluation_strategy="no",
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