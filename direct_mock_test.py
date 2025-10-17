#!/usr/bin/env python3
from mock_llm_server import generate_simple_workflow

prompt = "Watch my Google Sheet for rows where sales are above $5000, then send a Slack alert, SMS via Twilio, and log the alert in another sheet"

workflow = generate_simple_workflow(prompt)

print(f"Workflow nodes:\n")
for node in workflow['nodes']:
    print(f"  - {node['name']} ({node['type'].split('.')[-1]})")
    print(f"    Position: {node['position']}")
    if node.get('disabled'):
        print("    DISABLED")
