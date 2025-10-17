#!/usr/bin/env python3
"""Direct test of frontend API."""

import requests
import json

print("[1] Testing simple_test_server directly...")
try:
    r1 = requests.post('http://localhost:8000/generate', json={'prompt':'send email'}, timeout=5)
    print(f"  Status: {r1.status_code}")
    if r1.status_code == 200:
        print(f"  Nodes: {len(r1.json().get('workflow', {}).get('nodes', []))}")
except Exception as e:
    print(f"  Error: {e}")

print("\n[2] Testing frontend API...")
try:
    r2 = requests.post('http://localhost:5000/api/generate', json={'prompt':'send email to admin'}, timeout=10)
    print(f"  Status: {r2.status_code}")
    print(f"  Response: {r2.text[:300]}")
except Exception as e:
    print(f"  Error: {e}")

print("\nDone!")
