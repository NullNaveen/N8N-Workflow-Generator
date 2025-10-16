import json
import os
from pathlib import Path
from dataclasses import dataclass

"""
Minimal QLoRA training scaffold using Hugging Face Transformers + PEFT.
This prepares instruction-tuning data from data/dataset.jsonl and trains a
small adapter on a chosen base model (e.g., mistralai/Mistral-7B-Instruct-v0.3).

Note: This is a scaffold; adjust batch sizes/learning rate/epochs based on your GPU.
"""


@dataclass
class TrainConfig:
    base_model: str = os.environ.get("BASE_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
    dataset_path: str = "data/dataset.jsonl"
    output_dir: str = "models/n8n-lora"
    micro_batch_size: int = int(os.environ.get("MICRO_BATCH_SIZE", 1))
    gradient_accumulation_steps: int = int(os.environ.get("GRAD_ACC_STEPS", 16))
    learning_rate: float = float(os.environ.get("LEARNING_RATE", 2e-4))
    num_epochs: int = int(os.environ.get("NUM_EPOCHS", 1))
    max_seq_len: int = int(os.environ.get("MAX_SEQ_LEN", 2048))


def load_examples(path: str):
    examples = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            prompt = obj.get("prompt", "")
            wf = obj.get("workflow", {})
            if not prompt or not isinstance(wf, dict):
                continue
            # SFT style: ask model to return only valid JSON
            system = (
                "You are an expert n8n workflow designer. Convert the user's prompt to a valid n8n JSON workflow. "
                "Return ONLY JSON."
            )
            user = prompt
            assistant = json.dumps(wf, ensure_ascii=False)
            examples.append({"system": system, "user": user, "assistant": assistant})
    return examples


def main():
    cfg = TrainConfig()
    print("Loading dataset...", cfg.dataset_path)
    examples = load_examples(cfg.dataset_path)
    print(f"Loaded {len(examples)} examples")

    # Lazy imports to keep app deps light
    from datasets import Dataset
    from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, DataCollatorForLanguageModeling, Trainer
    import torch
    from peft import LoraConfig, get_peft_model, TaskType

    # Build dataset of concatenated conversations
    def to_text(ex):
        return f"<s>[SYSTEM]\n{ex['system']}\n[/SYSTEM]\n[USER]\n{ex['user']}\n[/USER]\n[ASSISTANT]\n{ex['assistant']}\n[/ASSISTANT]</s>"

    ds = Dataset.from_list([{"text": to_text(e)} for e in examples])

    tokenizer = AutoTokenizer.from_pretrained(cfg.base_model, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, max_length=cfg.max_seq_len)

    tokenized = ds.map(tokenize, batched=True, remove_columns=["text"])  # type: ignore

    print("Loading base model:", cfg.base_model)
    model = AutoModelForCausalLM.from_pretrained(cfg.base_model, torch_dtype=torch.float16, device_map="auto")

    lora_cfg = LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )
    model = get_peft_model(model, lora_cfg)

    args = TrainingArguments(
        output_dir=cfg.output_dir,
        per_device_train_batch_size=cfg.micro_batch_size,
        gradient_accumulation_steps=cfg.gradient_accumulation_steps,
        num_train_epochs=cfg.num_epochs,
        learning_rate=cfg.learning_rate,
        logging_steps=50,
        save_total_limit=2,
        save_strategy="epoch",
        bf16=torch.cuda.is_available(),
        fp16=not torch.cuda.is_available(),
        report_to=[],
    )

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized,
        data_collator=data_collator,
    )

    print("Starting training...")
    trainer.train()
    print("Saving adapter to:", cfg.output_dir)
    model.save_pretrained(cfg.output_dir)
    tokenizer.save_pretrained(cfg.output_dir)


if __name__ == "__main__":
    main()
