import json
import torch
from transformers import AutoTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset

# Load dataset from the generated JSON file
def load_data(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    texts = [item["text"] for item in data]
    labels = [0 if item["label"] == "PLAY_MUSIC" else 1 for item in data]  # Binary classification
    return texts, labels

# Tokenize dataset
def tokenize_data(texts, tokenizer):
    return tokenizer(texts, padding=True, truncation=True, return_tensors="pt")

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("huawei-noah/TinyBERT_General_4L_312D")
model = BertForSequenceClassification.from_pretrained("huawei-noah/TinyBERT_General_4L_312D", num_labels=2)

# Load and prepare dataset
texts, labels = load_data("data.json")  # Replace with your dataset file
encodings = tokenize_data(texts, tokenizer)
dataset = Dataset.from_dict({"input_ids": encodings["input_ids"], "attention_mask": encodings["attention_mask"], "labels": labels})

# Define training arguments
training_args = TrainingArguments(
    output_dir="./tinybert_finetuned",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
)

# Trainer setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    eval_dataset=dataset,
)

# Fine-tune the model
trainer.train()

# Save the model
model.save_pretrained("./tinybert_finetuned")
tokenizer.save_pretrained("./tinybert_finetuned")
