#!/usr/bin/env python3
import requests
import json

# Test with YOUR complex prompt
prompt = "Watch my Google Sheet for rows where sales are above $5000, then send a Slack alert, SMS via Twilio, and log the alert in another sheet"

print(f"Testing prompt:\n  {prompt}\n")

try:
    resp = requests.post('http://127.0.0.1:5000/api/generate', 
                        json={'prompt': prompt}, 
                        timeout=10)
    data = resp.json()
    
    if data.get('success'):
        print("✅ SUCCESS!\n")
        workflow = data['workflow']
        print(f"Workflow Name: {workflow['name']}")
        print(f"Nodes generated: {len(workflow['nodes'])}\n")
        
        print("Nodes:")
        for node in workflow['nodes']:
            node_type = node['type'].split('.')[-1]
            disabled = " (DISABLED)" if node.get('disabled') else ""
            print(f"  • {node['name']} ({node_type}){disabled}")
        
        print(f"\nMethod: {data.get('method')}")
    else:
        print(f"❌ Error: {data.get('error')}")
        
except Exception as e:
    print(f"❌ Error: {e}")
