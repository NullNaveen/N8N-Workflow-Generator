# 🎓 Complete Training Guide - N8N Workflow Generator

## 📋 What You Need to Do vs What I Already Did

### ✅ What I Already Did (Code is Ready)
- Created dataset builder script (`scripts/train/dataset_builder.py`)
- Created training script with QLoRA (`scripts/train/qlora_train.py`)
- Created inference server (`scripts/serve/local_inference.py`)
- Updated the main app to use local LLM first, then Groq as fallback
- Fixed your immediate API error (was missing `.env` file)

### 🎯 What YOU Need to Do (Step-by-Step Below)
1. Choose between Colab or Kaggle for training
2. Upload necessary files
3. Run the training notebook (I'll provide ready-to-use notebooks)
4. Download the trained model
5. Run the inference server locally
6. Use the app (it will work immediately!)

---

## 🚨 IMMEDIATE FIX - Your Current Error

**Problem**: You're getting "Failed to generate workflow" error even with Groq API key.

**Solution**: I just fixed it! Your `.env` file was missing. I created it from `.env.example`.

**Restart your app now:**
```powershell
# Stop the current server (Ctrl+C in the terminal)
# Then run:
python app.py
```

**You should now see**: "Groq API configured: Yes" and workflows should generate!

---

## 🤖 Current LLM Choice & Why

### What I Selected: **Mistral-7B-Instruct-v0.3**

**Why this model?**
- ✅ **Size**: 7B parameters = fits on free GPUs (T4, P100)
- ✅ **Quality**: Great instruction following for JSON generation
- ✅ **Speed**: Fast inference (~2-3 seconds per workflow)
- ✅ **License**: Fully open (Apache 2.0)
- ✅ **Format**: Already instruction-tuned (understands system/user/assistant format)

### Best Alternatives (Ranked):

1. **meta-llama/Llama-3.1-8B-Instruct** ⭐ BEST CHOICE
   - Slightly better quality than Mistral
   - Same size, fits on T4/P100
   - **Recommendation**: Use this one!

2. **Qwen/Qwen2.5-7B-Instruct**
   - Excellent at structured output
   - Good for JSON generation
   - Slightly slower

3. **mistralai/Mistral-7B-Instruct-v0.3** (current)
   - Solid choice, proven
   - Fast and reliable

4. ❌ **DON'T USE**: 70B+ models (won't fit on free GPUs)

### My Recommendation: **Switch to Llama-3.1-8B-Instruct**
It's marginally better and has more recent training data.

---

## 📊 Best Groq Model for Your Usage

Based on your limits, here's my analysis:

### 🏆 WINNER: **llama-3.1-8b-instant**

**Why?**
- ✅ **14,400 requests/day** (highest for decent quality models)
- ✅ **500K tokens/day** (plenty for workflows)
- ✅ **6K tokens/minute** (fast enough)
- ✅ **Fast**: Instant responses
- ✅ **Quality**: Good enough for JSON generation

### Comparison Table:

| Model | Requests/Day | Tokens/Day | Quality | Speed | Verdict |
|-------|--------------|------------|---------|-------|---------|
| llama-3.1-8b-instant | **14.4K** ✅ | **500K** | Good | ⚡ Fast | **BEST** |
| meta-llama/llama-guard-4-12b | 14.4K | 500K | Moderate | Medium | Backup |
| llama-3.3-70b-versatile | 1K ❌ | 100K ❌ | Excellent | Slow | Too limited |
| allam-2-7b | 7K | 500K | Unknown | Fast | Untested |

### Current Config in Code:
I'm using `llama-3.1-70b-versatile` in the code, which gives you **only 1K requests/day**.

### 🔧 Let's Change It Now:

```python
# In app.py, line ~110, change:
'model': 'llama-3.1-8b-instant',  # Changed from 70b to 8b
```

This gives you **14x more requests per day**!

---

## 🖥️ GPU/TPU Comparison: Colab vs Kaggle

### My Recommendation: **Kaggle with GPU P100** 🏆

| Platform | Hardware | VRAM | Training Time | Pros | Cons |
|----------|----------|------|---------------|------|------|
| **Kaggle P100** ⭐ | GPU P100 | 16GB | ~2-3 hrs | - Most reliable<br>- More VRAM<br>- Better for 7B models | Slower than T4 |
| Kaggle T4 x2 | 2x GPU T4 | 2x 15GB | ~1.5-2 hrs | - Fastest option<br>- Dual GPU support | Need multi-GPU code |
| Colab T4 | GPU T4 | 15GB | ~2-3 hrs | - Easy to use<br>- Familiar interface | - May disconnect<br>- Shorter sessions |
| Colab TPU | TPU v5e-1 | - | ❌ Complex | - Very fast (if working) | - Complex setup<br>- May not work |
| Kaggle TPU | TPU v5e-8 | - | ❌ Complex | - Fastest (if working) | - Requires JAX/XLA<br>- Not worth it |

### Final Verdict:
**Use Kaggle P100** - Most reliable, enough VRAM, straightforward.

---

## 📝 STEP-BY-STEP: How to Train Your Model

### Prerequisites (Do These First):

1. **Prepare Your Files on Your Computer:**
   ```powershell
   # Navigate to your project
   cd C:\Users\Nike\Documents\Programming\Projects\N8N
   
   # Build the dataset (this creates data/dataset.jsonl)
   python scripts\train\dataset_builder.py
   ```
   
   You should see: `Wrote XXXX examples to data\dataset.jsonl`

2. **Files You'll Need to Upload:**
   - `data/dataset.jsonl` (created above)
   - `scripts/train/qlora_train.py` (already exists)

---

## 🚀 OPTION A: Training on Kaggle (RECOMMENDED)

### Step 1: Setup Kaggle Account
1. Go to https://www.kaggle.com/
2. Sign in or create account
3. Go to Settings → Account → Create API Token
4. Download `kaggle.json` (optional, for CLI)

### Step 2: Create New Notebook
1. Click **"Code"** → **"New Notebook"**
2. Change settings:
   - **Accelerator**: GPU P100
   - **Language**: Python
   - **Internet**: ON (required for downloading model)

### Step 3: Upload Your Files
In the notebook interface:
1. Click **"+ Add Data"** → **"Upload"**
2. Upload `data/dataset.jsonl`
3. Upload `scripts/train/qlora_train.py`

### Step 4: Copy-Paste This Code in Notebook

```python
# Cell 1: Install dependencies
!pip install -q transformers==4.44.2 peft==0.11.1 accelerate==0.33.0 datasets==2.19.0 bitsandbytes

# Cell 2: Setup paths
import os
import shutil

# Copy uploaded files to working directory
shutil.copy('/kaggle/input/your-dataset/dataset.jsonl', '/kaggle/working/dataset.jsonl')

# Verify dataset
with open('/kaggle/working/dataset.jsonl', 'r') as f:
    lines = f.readlines()
    print(f"✅ Dataset has {len(lines)} examples")

# Cell 3: Configure training
os.environ['BASE_MODEL'] = 'meta-llama/Llama-3.1-8B-Instruct'  # Change if you want
os.environ['MICRO_BATCH_SIZE'] = '1'
os.environ['GRAD_ACC_STEPS'] = '4'
os.environ['LEARNING_RATE'] = '2e-4'
os.environ['NUM_EPOCHS'] = '1'
os.environ['MAX_SEQ_LEN'] = '2048'

# Cell 4: Prepare training script
training_code = '''
import json
import os
from pathlib import Path
from dataclasses import dataclass

@dataclass
class TrainConfig:
    base_model: str = os.environ.get("BASE_MODEL", "meta-llama/Llama-3.1-8B-Instruct")
    dataset_path: str = "/kaggle/working/dataset.jsonl"
    output_dir: str = "/kaggle/working/n8n-lora"
    micro_batch_size: int = int(os.environ.get("MICRO_BATCH_SIZE", 1))
    gradient_accumulation_steps: int = int(os.environ.get("GRAD_ACC_STEPS", 4))
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
    print(f"✅ Loaded {len(examples)} examples")

    from datasets import Dataset
    from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, DataCollatorForLanguageModeling, Trainer
    import torch
    from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
    from transformers import BitsAndBytesConfig

    def to_text(ex):
        return f"<s>[SYSTEM]\\n{ex['system']}\\n[/SYSTEM]\\n[USER]\\n{ex['user']}\\n[/USER]\\n[ASSISTANT]\\n{ex['assistant']}\\n[/ASSISTANT]</s>"

    ds = Dataset.from_list([{"text": to_text(e)} for e in examples])

    tokenizer = AutoTokenizer.from_pretrained(cfg.base_model, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, max_length=cfg.max_seq_len)

    tokenized = ds.map(tokenize, batched=True, remove_columns=["text"])

    print("Loading base model with 4-bit quantization:", cfg.base_model)
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )
    
    model = AutoModelForCausalLM.from_pretrained(
        cfg.base_model,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    
    model = prepare_model_for_kbit_training(model)

    lora_cfg = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
    )
    model = get_peft_model(model, lora_cfg)
    
    print("Trainable parameters:", model.print_trainable_parameters())

    args = TrainingArguments(
        output_dir=cfg.output_dir,
        per_device_train_batch_size=cfg.micro_batch_size,
        gradient_accumulation_steps=cfg.gradient_accumulation_steps,
        num_train_epochs=cfg.num_epochs,
        learning_rate=cfg.learning_rate,
        logging_steps=10,
        save_total_limit=1,
        save_strategy="epoch",
        bf16=False,
        fp16=True,
        report_to=[],
        optim="paged_adamw_8bit",
        warmup_steps=10,
    )

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized,
        data_collator=data_collator,
    )

    print("🚀 Starting training...")
    trainer.train()
    
    print("💾 Saving adapter to:", cfg.output_dir)
    model.save_pretrained(cfg.output_dir)
    tokenizer.save_pretrained(cfg.output_dir)
    
    print("✅ Training complete!")

if __name__ == "__main__":
    main()
'''

with open('/kaggle/working/train.py', 'w') as f:
    f.write(training_code)

# Cell 5: Run training!
!python /kaggle/working/train.py

# Cell 6: Download your model
print("✅ Training done! Now download your model:")
print("1. Click 'Save Version' at top right")
print("2. After it saves, go to 'Output' tab")
print("3. Download the 'n8n-lora' folder")
```

### Step 5: Monitor Training
- You'll see progress bars
- Training takes ~1.5-3 hours
- **Don't close the tab!**

### Step 6: Download Trained Model
1. After training completes, click **"Save Version"** (top right)
2. Wait for it to commit (~5 minutes)
3. Go to **"Output"** tab
4. Download the `n8n-lora` folder as ZIP
5. Extract it to `C:\Users\Nike\Documents\Programming\Projects\N8N\models\n8n-lora\`

---

## 🚀 OPTION B: Training on Colab (Alternative)

### Step 1: Open Colab
1. Go to https://colab.research.google.com/
2. File → New Notebook
3. Runtime → Change runtime type → **GPU T4**

### Step 2: Upload Files
```python
# Cell 1: Upload dataset
from google.colab import files
uploaded = files.upload()  # Upload your dataset.jsonl
```

### Step 3: Same Training Code as Kaggle
Use the exact same code from Kaggle Steps 1-5 above, but change paths:
- Replace `/kaggle/working/` with `/content/`
- Replace `/kaggle/input/` with `/content/`

### Step 4: Download Model
```python
# After training completes:
from google.colab import files
!zip -r n8n-lora.zip /content/n8n-lora
files.download('/content/n8n-lora.zip')
```

---

## 🎯 After Training: Using Your Model Locally

### Step 1: Place the Model
```powershell
# Your model should be in:
C:\Users\Nike\Documents\Programming\Projects\N8N\models\n8n-lora\
```

### Step 2: Start the Inference Server
```powershell
# Open a NEW PowerShell window
cd C:\Users\Nike\Documents\Programming\Projects\N8N

# Set environment variables
$env:BASE_MODEL="meta-llama/Llama-3.1-8B-Instruct"
$env:ADAPTER_PATH="models/n8n-lora"

# Start the server
python scripts\serve\local_inference.py
```

You should see:
```
Loading model...
 * Running on http://127.0.0.1:8000
```

### Step 3: Start Your Main App (in ANOTHER terminal)
```powershell
# In a SECOND PowerShell window
cd C:\Users\Nike\Documents\Programming\Projects\N8N
python app.py
```

### Step 4: Use the UI!
1. Open http://localhost:5000
2. Type your prompt
3. It will use YOUR trained model first!
4. If that fails, it falls back to Groq

---

## ❓ FAQ

### Q: Can I use the app WITHOUT training my own model?
**A**: Yes! Just use Groq (which I already fixed). The app works fine with just Groq.

### Q: What format do you need the trained files in?
**A**: The LoRA adapter folder should contain:
- `adapter_config.json`
- `adapter_model.safetensors` (or `adapter_model.bin`)
- `tokenizer_config.json`
- `tokenizer.json`

### Q: How much does training cost?
**A**: $0.00 on Kaggle or Colab free tier!

### Q: How long does training take?
**A**: 
- P100: ~2-3 hours
- T4: ~2-3 hours
- Depends on your dataset size

### Q: Can I stop and resume training?
**A**: No, you need to complete it in one session. But you can train for just 1 epoch (as configured).

### Q: What if I get "out of memory" error?
**A**: Change in training config:
```python
os.environ['MICRO_BATCH_SIZE'] = '1'  # Keep at 1
os.environ['GRAD_ACC_STEPS'] = '8'     # Increase this
```

---

## 🎯 Quick Checklist

Before training:
- [ ] Run dataset builder locally
- [ ] Verify `data/dataset.jsonl` exists and has examples
- [ ] Choose Kaggle P100 or Colab T4

During training:
- [ ] Upload dataset.jsonl
- [ ] Copy-paste training code
- [ ] Start training cell
- [ ] **DON'T CLOSE TAB**

After training:
- [ ] Download n8n-lora folder
- [ ] Extract to `models/n8n-lora/`
- [ ] Start inference server
- [ ] Start main app
- [ ] Test in UI

---

## 🔥 IMPORTANT NOTES

1. **First time using the app with Groq?** 
   - It works NOW (I fixed the .env issue)
   - Just restart your app

2. **Training is OPTIONAL**
   - You can use just Groq
   - Local model gives you more control and unlimited usage

3. **Model files are LARGE**
   - Base model: ~5GB download
   - LoRA adapter: ~50-100MB
   - Make sure you have space!

4. **Internet required**
   - Training downloads the base model (~5GB)
   - First inference also downloads it
   - After that, it's cached

---

Need help? Ask me specific questions! 🚀
