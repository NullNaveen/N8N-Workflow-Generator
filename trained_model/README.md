# N8N Workflow Generator - LoRA Fine-tuned Model

## Overview

This is a LoRA-fine-tuned version of Mistral-7B-Instruct-v0.2 trained to generate n8n workflow JSON from natural language descriptions.

## Model Details

- **Base Model**: mistralai/Mistral-7B-Instruct-v0.2
- **Fine-tuning**: LoRA (Rank 16, Alpha 32)
- **Training Data**: n8n workflow examples with natural language descriptions
- **Training Epochs**: 3
- **Training Status**: ✅ Complete

## What This Model Does

Input natural language description:
```
"Create a workflow that receives webhook data and sends an email notification"
```

Output: Valid n8n workflow JSON with all nodes and connections configured.

## Installation

1. **Install dependencies**:
```bash
pip install transformers peft accelerate bitsandbytes torch
```

2. **Download model files**:
Clone or download this repository.

## Usage

### Basic Python Usage

```python
from inference import N8NWorkflowGenerator

generator = N8NWorkflowGenerator(model_dir=".")
result = generator.generate_workflow_json(
    "Create a workflow that receives data from a webhook and sends an email"
)

if result["success"]:
    workflow_json = result["workflow"]
    print(workflow_json)
else:
    print("Error:", result["error"])
```

### Run Example Script

```bash
python inference.py
```

This will generate 3 example workflows automatically.

### Interactive Jupyter Notebook

```bash
jupyter notebook Inference_Notebook.ipynb
```

Follow the cells to:
- Load the model
- Generate workflows from prompts
- Test with custom descriptions

## Model Configuration

| Parameter | Value |
|-----------|-------|
| Base Model | mistralai/Mistral-7B-Instruct-v0.2 |
| LoRA Rank | 16 |
| LoRA Alpha | 32 |
| Target Modules | q_proj, k_proj, v_proj, o_proj |
| Training Epochs | 3 |

## GPU Requirements

- **Recommended**: GPU with 6GB+ VRAM (with 4-bit quantization)
- **Alternative**: CPU (slower, ~32GB RAM)
- **Fallback**: Automatic CPU fallback if GPU unavailable

## Files

- `inference.py` - Production inference class
- `Inference_Notebook.ipynb` - Interactive testing notebook
- `adapter_model.safetensors` - LoRA weights (4.4 MB)
- `tokenizer.model` - Tokenizer weights
- Configuration files for LoRA and tokenizer

## Performance

- **Model Loading**: ~30-60 seconds (first time)
- **Generation Speed**: ~30-120 seconds per prompt
- **Model Size**: ~4.4 MB (LoRA adapter only)