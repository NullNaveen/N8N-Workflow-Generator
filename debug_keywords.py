#!/usr/bin/env python3
"""Debug keyword matching."""

from simple_test_server import keyword_to_nodes

prompts = [
    "Whenever a new WordPress blog post is published, shorten the URL, post it on Twitter and LinkedIn, and log the post details in Google Sheets",
    "Send an email when a new Airtable record is added, then create a task in Asana and post to Slack",
    "Monitor HubSpot for new leads, create them in Salesforce, add to Mailchimp, and notify team on Discord",
]

for prompt in prompts:
    prompt_lower = prompt.lower()
    nodes = keyword_to_nodes(prompt)
    print(f"\nPrompt: {prompt[:60]}...")
    print(f"Nodes generated: {len(nodes)} - {nodes}")
    
    # Check specific patterns
    if "twitter" in prompt_lower:
        print(f"  - Contains 'twitter': YES")
    if "linkedin" in prompt_lower:
        print(f"  - Contains 'linkedin': YES")
    if "asana" in prompt_lower:
        print(f"  - Contains 'asana': YES")
