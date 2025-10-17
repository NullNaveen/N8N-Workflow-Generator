#!/usr/bin/env python
"""Quick test to diagnose inference.py issues"""

import sys
import traceback

print("=" * 60)
print("N8N Workflow Generator - Diagnostic Test")
print("=" * 60)

# Test 1: Check imports
print("\n[1/5] Testing imports...")
try:
    import torch
    print(f"  ✅ PyTorch {torch.__version__}")
    print(f"  CUDA available: {torch.cuda.is_available()}")
except Exception as e:
    print(f"  ❌ PyTorch error: {e}")
    sys.exit(1)

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    print("  ✅ Transformers")
except Exception as e:
    print(f"  ❌ Transformers error: {e}")
    sys.exit(1)

try:
    from peft import PeftModel
    print("  ✅ PEFT")
except Exception as e:
    print(f"  ❌ PEFT error: {e}")
    sys.exit(1)

# Test 2: Check model files
print("\n[2/5] Checking model files...")
from pathlib import Path

files_to_check = [
    "adapter_model.safetensors",
    "tokenizer.model",
    "adapter_config.json",
    "tokenizer_config.json"
]

for file in files_to_check:
    exists = Path(file).exists()
    status = "✅" if exists else "❌"
    print(f"  {status} {file}")
    if not exists:
        print(f"    ERROR: {file} not found!")
        sys.exit(1)

# Test 3: Try to load the inference class
print("\n[3/5] Loading inference class...")
try:
    from inference import N8NWorkflowGenerator
    print("  ✅ Inference class loaded")
except Exception as e:
    print(f"  ❌ Error loading inference class:")
    print(f"     {str(e)}")
    traceback.print_exc()
    sys.exit(1)

# Test 4: Try to create generator (this will load model)
print("\n[4/5] Initializing model (this may take a minute)...")
try:
    print("  Loading with quantization disabled (CPU fallback)...")
    generator = N8NWorkflowGenerator(
        model_dir=".",
        use_quantization=False,
        device="cpu"
    )
    print("  ✅ Model loaded successfully!")
except Exception as e:
    print(f"  ❌ Error loading model:")
    print(f"     {str(e)}")
    traceback.print_exc()
    sys.exit(1)

# Test 5: Try to generate a workflow
print("\n[5/5] Testing workflow generation...")
try:
    print("  Generating test workflow (this may take 1-2 minutes)...")
    result = generator.generate_workflow_json(
        "Create a simple workflow with a webhook trigger"
    )
    
    if result["success"]:
        print("  ✅ Generation successful!")
        print(f"  Generated {len(str(result['workflow']))} characters of JSON")
    else:
        print(f"  ⚠️  Generation returned error: {result.get('error', 'Unknown')}")
except Exception as e:
    print(f"  ❌ Error during generation:")
    print(f"     {str(e)}")
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ All tests passed! Inference is working correctly.")
print("=" * 60)
