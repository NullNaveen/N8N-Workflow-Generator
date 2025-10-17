#!/usr/bin/env python3
"""Quick test of simple_test_server node generation with complex prompts."""

import requests
import json

BASE_URL = "http://localhost:8000"

# Test prompts
prompts = [
    "Whenever a new WordPress blog post is published, shorten the URL, post it on Twitter and LinkedIn, and log the post details in Google Sheets",
    "Send an email when a new Airtable record is added, then create a task in Asana and post to Slack",
    "Monitor HubSpot for new leads, create them in Salesforce, add to Mailchimp, and notify team on Discord",
]

print("\n" + "="*70)
print("[TEST] Simple_Test_Server Node Generation")
print("="*70)

for i, prompt in enumerate(prompts, 1):
    print(f"\n[Test {i}] {prompt[:60]}...")
    try:
        response = requests.post(
            f"{BASE_URL}/generate",
            json={"prompt": prompt},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            workflow = data.get("workflow", {})
            nodes = workflow.get("nodes", [])
            print(f"  ✓ Generated {len(nodes)} nodes")
            for node in nodes:
                node_type = node.get("type", "unknown")
                print(f"    - {node_type}")
        else:
            print(f"  ✗ Error {response.status_code}: {response.text[:100]}")
    except Exception as e:
        print(f"  ✗ Exception: {str(e)}")

print("\n" + "="*70)
print("[DONE] Tests Complete")
print("="*70 + "\n")
