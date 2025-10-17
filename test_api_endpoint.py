#!/usr/bin/env python3
"""Test the full workflow generation API."""

import requests
import json

# Test with the WordPress prompt
prompt = "Whenever a new WordPress blog post is published, shorten the URL, post it on Twitter and LinkedIn, and log the post details in Google Sheets"

print("\n" + "="*70)
print("[TEST] Full Workflow Generation API")
print("="*70)
print(f"\nPrompt: {prompt}\n")

try:
    # Call frontend API
    response = requests.post(
        "http://localhost:5000/api/generate",
        json={"prompt": prompt},
        timeout=10
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nResponse keys: {list(data.keys())}")
        
        if "workflow" in data:
            workflow = data["workflow"]
            nodes = workflow.get("nodes", [])
            print(f"\n✓ Generated {len(nodes)} nodes:")
            for i, node in enumerate(nodes, 1):
                node_name = node.get("name", "Unknown")
                node_type = node.get("type", "unknown")
                print(f"  {i}. {node_name} ({node_type})")
            
            print(f"\nWorkflow name: {workflow.get('name', 'N/A')}")
            print(f"Generation method: {data.get('method', 'N/A')}")
            
            # Check for model info
            if "model" in data:
                print(f"\nModel info: {data['model']}")
    else:
        print(f"Error: {response.text[:500]}")

except Exception as e:
    print(f"Exception: {e}")

print("\n" + "="*70 + "\n")
