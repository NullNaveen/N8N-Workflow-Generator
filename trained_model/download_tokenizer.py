#!/usr/bin/env python
"""Download proper tokenizer for Mistral model"""

from transformers import AutoTokenizer
from pathlib import Path

print("Downloading Mistral tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

print("Saving tokenizer...")
tokenizer.save_pretrained(".")
print("✅ Tokenizer saved successfully!")

# Verify
files = list(Path(".").glob("tokenizer*"))
print(f"\nTokenizer files created:")
for f in files:
    print(f"  ✅ {f.name}")
