#!/usr/bin/env python3
import requests
import json

prompt = "Watch my Google Sheet for rows where sales are above $5000, then send a Slack alert, SMS via Twilio, and log the alert in another sheet"

print(f"Direct mock server test:\n")

resp = requests.post('http://127.0.0.1:8000/generate', 
                    json={'prompt': prompt}, 
                    timeout=10)
workflow = resp.json()['workflow']

print(f"Nodes generated: {len(workflow['nodes'])}\n")
for node in workflow['nodes']:
    print(f"  • {node['name']}")

prompt_lower = prompt.lower()
print(f"\nDebugging:");
print(f"  'sms' in prompt: {'sms' in prompt_lower}")
print(f"  'twilio' in prompt: {'twilio' in prompt_lower}")  
print(f"  'log' in prompt: {'log' in prompt_lower}")
print(f"  'another sheet' in prompt: {'another sheet' in prompt_lower}")
