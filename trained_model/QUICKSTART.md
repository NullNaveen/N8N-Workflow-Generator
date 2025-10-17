# Quick Start - N8N Workflow Generator

## Installation

### 1. Install Dependencies

```bash
pip install transformers peft accelerate bitsandbytes torch
```

### 2. Run the Model

```bash
python inference.py
```

This will automatically:
- Load the trained model
- Generate example workflows
- Display the output

## Usage

### Python Script

```python
from inference import N8NWorkflowGenerator

generator = N8NWorkflowGenerator(model_dir=".")
result = generator.generate_workflow_json(
    "Create a workflow that receives webhook data and sends an email"
)

if result["success"]:
    workflow_json = result["workflow"]
    print(workflow_json)
```

### Jupyter Notebook

```bash
jupyter notebook Inference_Notebook.ipynb
```

Run cells sequentially to:
- Load the model
- Generate workflows
- Test with custom prompts

## Configuration

### GPU Usage

```python
# With 4-bit quantization (uses less VRAM)
generator = N8NWorkflowGenerator(
    model_dir=".",
    use_quantization=True,
    device="cuda"
)

# CPU fallback (slower)
generator = N8NWorkflowGenerator(
    model_dir=".",
    device="cpu"
)
```

### Generation Parameters

```python
result = generator.generate(
    prompt="Your description",
    temperature=0.7,      # 0-1, lower=deterministic, higher=creative
    top_p=0.9,           # Nucleus sampling
    max_length=2048      # Maximum tokens
)
```

## Files

- `inference.py` - Main inference script
- `Inference_Notebook.ipynb` - Interactive testing
- `adapter_model.safetensors` - Trained weights
- `tokenizer.model` - Tokenizer
- `README.md` - Full documentation
