"""
Test suite: 10 complex prompts to validate LLM-only workflow generation.
Each prompt should produce valid JSON with multiple nodes and connections.
"""

import requests
import json
import sys

# Frontend API endpoint
FRONTEND_URL = "http://127.0.0.1:5000/api/generate"

# Complex test prompts covering various scenarios with 7-10+ distinct apps/integrations
TEST_PROMPTS = [
    # 1. Multi-channel customer notification
    "When a customer support email arrives, save attachments to Google Drive, create a ticket in Zendesk, post notification to Slack channel, send SMS via Twilio, store in Airtable, and notify via Discord",
    
    # 2. Sales monitoring with multiple actions
    "Monitor Google Sheets for new rows where sales exceed $5000; alert team on Slack, send email, create follow-up task in Asana, update dashboard in Notion, log to MongoDb, and post to Twitter",
    
    # 3. GitHub workflow automation
    "When a GitHub issue is created with 'bug' label, create Trello card, notify team on Teams, send email to stakeholders, log in Notion, create task in Asana, post to Slack, and update project dashboard",
    
    # 4. Data pipeline with validation
    "Process incoming webhook data, validate with custom function, store in MongoDB, send confirmation email, create record in Airtable, post summary to Slack, update Google Sheets, and notify via SMS",
    
    # 5. Scheduled reporting workflow
    "Daily at 9am UTC: fetch weather data, analyze trends with custom code, create report in Notion, share on Microsoft Teams, schedule next run, email stakeholders, post summary to Slack, and backup to Google Drive",
    
    # 6. E-commerce fulfillment
    "When Stripe payment succeeds, update customer in HubSpot CRM, send thank you email, create invoice in QuickBooks, notify warehouse on Slack, log in Airtable, update Google Sheets inventory, and trigger email sequence",
    
    # 7. Content distribution pipeline
    "Monitor RSS feed, filter articles by keyword, summarize with AI, post to WordPress, share on Twitter, post to Slack, save to Airtable, email subscribers, and archive in Google Drive",
    
    # 8. Lead management workflow
    "When form submission received, validate email and phone, save to database, send SMS confirmation, create lead in HubSpot CRM, post alert to Slack, add to Google Sheets, email sales team, and schedule follow-up",
    
    # 9. Document processing pipeline
    "When file uploaded, extract text with OCR, translate to Spanish, save to cloud storage, index in search engine, create record in Notion, notify in Slack, email team lead, and log activity to database",
    
    # 10. Complex multi-condition workflow
    "When calendar event starts, send reminder emails to all attendees, update project status in Asana, log time entry in Harvest, post to team Slack channel, update Google Sheets, sync with CRM, notify via Discord, and create backup"
]

def validate_workflow(workflow: dict, prompt: str) -> tuple[bool, list]:
    """Validate that the workflow is a valid n8n structure with reasonable complexity."""
    errors = []
    
    # Check required fields
    if not isinstance(workflow, dict):
        errors.append("Workflow is not a dictionary")
        return False, errors
    
    if "nodes" not in workflow:
        errors.append("Missing 'nodes' field")
    if "connections" not in workflow:
        errors.append("Missing 'connections' field")
    if "name" not in workflow:
        errors.append("Missing 'name' field")
    
    if errors:
        return False, errors
    
    # Validate nodes
    nodes = workflow.get("nodes", [])
    if not isinstance(nodes, list):
        errors.append("'nodes' is not a list")
        return False, errors
    
    if len(nodes) < 2:
        errors.append(f"Only {len(nodes)} nodes (expected at least 2)")
    
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"Node {i} is not a dictionary")
            continue
        if "name" not in node or "type" not in node:
            errors.append(f"Node {i} missing 'name' or 'type'")
        if "position" not in node:
            errors.append(f"Node {i} missing 'position'")
    
    # Validate connections
    connections = workflow.get("connections", {})
    if not isinstance(connections, dict):
        errors.append("'connections' is not a dictionary")
    
    return len(errors) == 0, errors

def run_tests():
    """Run all 10 prompts and collect results."""
    print("=" * 80)
    print("N8N WORKFLOW GENERATOR - COMPLEX PROMPT TEST SUITE")
    print("=" * 80)
    print(f"Testing {len(TEST_PROMPTS)} complex prompts...\n")
    
    results = []
    passed = 0
    failed = 0
    
    for i, prompt in enumerate(TEST_PROMPTS, 1):
        print(f"[TEST {i}/10] Prompt: {prompt[:70]}...")
        
        try:
            # Send request to frontend API
            response = requests.post(FRONTEND_URL, json={"prompt": prompt}, timeout=30)
            
            if response.status_code != 200:
                print(f"  [FAIL] HTTP {response.status_code}: {response.text[:100]}")
                results.append({"test": i, "passed": False, "error": f"HTTP {response.status_code}"})
                failed += 1
                continue
            
            data = response.json()
            
            # Check response structure
            if not data.get("success"):
                error_msg = data.get("error", "Unknown error")
                print(f"  [FAIL] API error: {error_msg[:100]}")
                results.append({"test": i, "passed": False, "error": error_msg})
                failed += 1
                continue
            
            # Validate workflow
            workflow = data.get("workflow", {})
            is_valid, val_errors = validate_workflow(workflow, prompt)
            
            if not is_valid:
                print(f"  [FAIL] Invalid workflow:")
                for err in val_errors[:3]:
                    print(f"    - {err}")
                results.append({"test": i, "passed": False, "error": "; ".join(val_errors[:2])})
                failed += 1
                continue
            
            # Success
            nodes_count = len(workflow.get("nodes", []))
            print(f"  [PASS] Generated {nodes_count} nodes, method={data.get('method', 'unknown')}")
            results.append({"test": i, "passed": True, "nodes": nodes_count})
            passed += 1
            
        except requests.RequestException as e:
            print(f"  [FAIL] Connection error: {str(e)[:100]}")
            results.append({"test": i, "passed": False, "error": f"Connection: {str(e)[:50]}"})
            failed += 1
        except Exception as e:
            print(f"  [FAIL] Unexpected error: {str(e)[:100]}")
            results.append({"test": i, "passed": False, "error": f"Exception: {str(e)[:50]}"})
            failed += 1
    
    # Summary
    print("\n" + "=" * 80)
    print(f"RESULTS: {passed} PASSED, {failed} FAILED")
    print("=" * 80)
    
    if failed > 0:
        print("\nFailed tests:")
        for r in results:
            if not r["passed"]:
                print(f"  Test {r['test']}: {r['error']}")
    
    print("\nPassed tests:")
    for r in results:
        if r["passed"]:
            print(f"  Test {r['test']}: {r['nodes']} nodes")
    
    return passed, failed

if __name__ == "__main__":
    try:
        passed, failed = run_tests()
        sys.exit(0 if failed == 0 else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
