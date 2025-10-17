#!/usr/bin/env python3
"""
Diagnose why the real model server is failing to load
"""

import os
import sys

# Set environment variables
os.environ["BASE_MODEL"] = "mistralai/Mistral-7B-Instruct-v0.2"
os.environ["ADAPTER_PATH"] = "trained_model"

print("🔍 DIAGNOSING MODEL LOADING ISSUES")
print("=" * 50)

try:
    print("[1/8] Checking Python environment...")
    print(f"    Python version: {sys.version}")
    print(f"    Python executable: {sys.executable}")
    
    print("[2/8] Checking file system...")
    base_model = "mistralai/Mistral-7B-Instruct-v0.2"
    adapter_path = "trained_model"
    
    if os.path.exists(adapter_path):
        files = os.listdir(adapter_path)
        print(f"    ✓ Adapter path exists with {len(files)} files")
        print(f"    Files: {', '.join(files[:5])}{'...' if len(files) > 5 else ''}")
    else:
        print(f"    ❌ Adapter path '{adapter_path}' not found!")
        sys.exit(1)
    
    print("[3/8] Testing imports...")
    try:
        import torch
        print(f"    ✓ PyTorch {torch.__version__}")
        print(f"    CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"    GPU: {torch.cuda.get_device_name(0)}")
    except ImportError as e:
        print(f"    ❌ PyTorch import failed: {e}")
        sys.exit(1)
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        print("    ✓ Transformers imported")
    except ImportError as e:
        print(f"    ❌ Transformers import failed: {e}")
        sys.exit(1)
    
    try:
        from peft import PeftModel
        print("    ✓ PEFT imported")
    except ImportError as e:
        print(f"    ❌ PEFT import failed: {e}")
        sys.exit(1)
    
    print("[4/8] Loading tokenizer...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(adapter_path, use_fast=True)
        print("    ✓ Tokenizer loaded from adapter")
    except Exception as e:
        print(f"    ⚠ Adapter tokenizer failed ({e}), trying base model...")
        try:
            tokenizer = AutoTokenizer.from_pretrained(base_model, use_fast=True)
            print("    ✓ Tokenizer loaded from base model")
        except Exception as e2:
            print(f"    ❌ Base model tokenizer failed: {e2}")
            sys.exit(1)
    
    print("[5/8] Setting pad token...")
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        print("    ✓ Pad token set")
    else:
        print("    ✓ Pad token already set")
    
    print("[6/8] Loading base model (this takes time)...")
    print(f"    Base model: {base_model}")
    print("    This will download ~14GB if not cached...")
    
    try:
        base_model_obj = AutoModelForCausalLM.from_pretrained(
            base_model, 
            torch_dtype=torch.float16, 
            device_map="auto"
        )
        print("    ✓ Base model loaded successfully")
    except Exception as e:
        print(f"    ❌ Base model loading failed: {e}")
        print("    This is likely due to insufficient memory or missing model files")
        sys.exit(1)
    
    print("[7/8] Loading PEFT adapter...")
    try:
        model = PeftModel.from_pretrained(base_model_obj, adapter_path, is_trainable=False)
        print("    ✓ PEFT adapter loaded successfully")
    except Exception as e:
        print(f"    ❌ PEFT adapter loading failed: {e}")
        sys.exit(1)
    
    print("[8/8] Setting model to eval mode...")
    model.eval()
    print("    ✓ Model ready for inference")
    
    print("\n" + "=" * 50)
    print("🎉 SUCCESS! Your trained model loaded correctly!")
    print("=" * 50)
    print()
    print("The model is ready. You can now run:")
    print("$env:BASE_MODEL='mistralai/Mistral-7B-Instruct-v0.2'")
    print("$env:ADAPTER_PATH='trained_model'")
    print("python .\\scripts\\serve\\local_inference.py")
    
except KeyboardInterrupt:
    print("\n⚠ Interrupted by user")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ UNEXPECTED ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)