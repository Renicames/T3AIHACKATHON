from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, BitsAndBytesConfig
import torch
model_name = "t3ai-org/pt-model"
model = AutoModelForCausalLM.from_pretrained(model_name,device_map="auto" )

import json
import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, BitsAndBytesConfig
from peft import LoraConfig, PeftModel
from trl import SFTTrainer
from datasets import Dataset

# Load the dataset from the JSON file
with open('base.json', 'r') as file:
    dataset = json.load(file)

# Prepare the dataset without additional formatting
formatted_dataset = []
for example in dataset:
    # Using the original question and answer pair directly without formatting
    formatted_dataset.append({"text": f"Question: {example['soru']}\nAnswer: {example['cevap']}"})

# Convert the formatted dataset to a Pandas DataFrame and then to a Hugging Face Dataset
df = pd.DataFrame.from_dict(formatted_dataset)
dataset = Dataset.from_pandas(df)

# LoRA configuration
peft_config = LoraConfig(
    lora_alpha=32,
    lora_dropout=0.1,
    r=64,
    task_type="CAUSAL_LM",
    use_dora = True
)

# Load the tokenizer and model from the ytu-ce-cosmos repository

model.config.use_cache = False
model.config.pretraining_tp = 1
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# Training arguments
training_args = TrainingArguments(
    output_dir="./results12",
    num_train_epochs=1,
    per_device_train_batch_size=16,
    gradient_accumulation_steps=16,
    logging_steps=1500,
    report_to="tensorboard",
    learning_rate=3e-5,
    weight_decay=0.001,
    fp16=False,
    bf16=False,
    max_grad_norm=0.3,
    max_steps=-1,
    warmup_ratio=0.03,
    group_by_length=True,
    optim="paged_adamw_32bit",
    save_steps=1500,
    lr_scheduler_type="constant"
)

# Trainer setup
trainer = SFTTrainer(
    model,
    train_dataset=dataset,
    dataset_text_field="text",
    tokenizer=tokenizer,
    peft_config=peft_config,
    args=training_args,
    max_seq_length=1024
)

# Train the model
trainer.train()