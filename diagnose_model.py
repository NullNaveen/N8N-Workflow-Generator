#!/usr/bin/env python3
"""Diagnose the model loading issue"""

import os
import sys

os.environ["BASE_MODEL"] = "mistralai/Mistral-7B-Instruct-v0.2"
os.environ["ADAPTER_PATH"] = "trained_model"

try:
    print("[1] Loading transformers...")
    from transformers import AutoTokenizer, AutoModelForCausalLM
    print("    ✓ Transformers loaded")
    
    print("[2] Loading PEFT...")
    from peft import PeftModel
    print("    ✓ PEFT loaded")
    
    print("[3] Loading torch...")
    import torch
    print(f"    ✓ Torch loaded. Device: {torch.cuda.is_available() and 'CUDA' or 'CPU'}")
    
    base = "mistralai/Mistral-7B-Instruct-v0.2"
    adapter = "trained_model"
    
    print(f"[4] Loading tokenizer from '{adapter}'...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(adapter, use_fast=True)
        print("    ✓ Tokenizer loaded from adapter")
    except Exception as e:
        print(f"    ⚠ Can't load from adapter ({e}), trying base...")
        tokenizer = AutoTokenizer.from_pretrained(base, use_fast=True)
        print("    ✓ Tokenizer loaded from base")
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        print("    ✓ Set pad token")
    
    print(f"[5] Loading base model '{base}' (7B)...")
    print("    This will download ~14GB if not cached. May take a few minutes...")
    base_model = AutoModelForCausalLM.from_pretrained(base, torch_dtype=torch.float16, device_map="auto")
    print("    ✓ Base model loaded")
    
    print(f"[6] Loading LoRA adapter from '{adapter}'...")
    model = PeftModel.from_pretrained(base_model, adapter, is_trainable=False)
    print("    ✓ Adapter loaded")
    
    model.eval()
    print("    ✓ Model in eval mode")
    
    print("\n✅ SUCCESS! Model is ready for inference.")
    print("\nNow run: $env:BASE_MODEL='mistralai/Mistral-7B-Instruct-v0.2'; $env:ADAPTER_PATH='trained_model'; python .\\scripts\\serve\\local_inference.py")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
