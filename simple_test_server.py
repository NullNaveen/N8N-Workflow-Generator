"""Ultra-minimal test LLM server for validation."""

from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

# Node templates for various integrations
NODE_TEMPLATES = {
    "webhook": {"name": "Webhook Trigger", "type": "n8n-nodes-base.webhook"},
    "schedule": {"name": "Schedule Trigger", "type": "n8n-nodes-base.scheduleTrigger"},
    "slack": {"name": "Slack Notification", "type": "n8n-nodes-base.slack"},
    "email": {"name": "Send Email", "type": "n8n-nodes-base.emailSend"},
    "gmail": {"name": "Gmail Send", "type": "n8n-nodes-base.gmail"},
    "discord": {"name": "Discord Message", "type": "n8n-nodes-base.discord"},
    "sheets": {"name": "Google Sheets", "type": "n8n-nodes-base.googleSheets"},
    "airtable": {"name": "Airtable", "type": "n8n-nodes-base.airtable"},
    "notion": {"name": "Notion", "type": "n8n-nodes-base.notion"},
    "trello": {"name": "Trello Card", "type": "n8n-nodes-base.trello"},
    "asana": {"name": "Asana Task", "type": "n8n-nodes-base.asana"},
    "zendesk": {"name": "Zendesk Ticket", "type": "n8n-nodes-base.zendesk"},
    "stripe": {"name": "Stripe", "type": "n8n-nodes-base.stripe"},
    "mongodb": {"name": "MongoDB", "type": "n8n-nodes-base.mongoDb"},
    "http": {"name": "HTTP Request", "type": "n8n-nodes-base.httpRequest"},
    "set": {"name": "Set Values", "type": "n8n-nodes-base.set"},
    "function": {"name": "Function", "type": "n8n-nodes-base.function"},
}

def keyword_to_nodes(prompt: str) -> list:
    """Map prompt keywords to node types - be aggressive to find many matches."""
    prompt_lower = prompt.lower()
    matched_nodes = []
    
    # Trigger detection (pick ONE)
    if any(w in prompt_lower for w in ["webhook", "receive", "incoming", "http", "post", "api call"]):
        matched_nodes.append("webhook")
    elif any(w in prompt_lower for w in ["schedule", "every", "daily", "hourly", "cron", "at 9am", "time", "periodic"]):
        matched_nodes.append("schedule")
    elif any(w in prompt_lower for w in ["form", "submission", "submit"]):
        matched_nodes.append("webhook")  # Form trigger
    else:
        matched_nodes.append("webhook")  # Default trigger
    
    # Aggressive action detection - match all mentioned services
    if any(w in prompt_lower for w in ["slack", "slack channel", "slack message", "post to slack"]):
        matched_nodes.append("slack")
    if any(w in prompt_lower for w in ["email", "send email", "email notification", "email to", "send an email"]):
        matched_nodes.append("email")
    if any(w in prompt_lower for w in ["gmail", "gmail message", "gmail send"]):
        matched_nodes.append("gmail")
    if any(w in prompt_lower for w in ["discord", "discord message", "discord notify", "post to discord"]):
        matched_nodes.append("discord")
    if any(w in prompt_lower for w in ["sheets", "google sheets", "spreadsheet", "sheets log"]):
        matched_nodes.append("sheets")
    if any(w in prompt_lower for w in ["airtable", "airtable base", "airtable record"]):
        matched_nodes.append("airtable")
    if any(w in prompt_lower for w in ["notion", "notion page", "notion database", "log to notion"]):
        matched_nodes.append("notion")
    if any(w in prompt_lower for w in ["trello", "trello card", "create card"]):
        matched_nodes.append("trello")
    if any(w in prompt_lower for w in ["asana", "asana task", "create task"]):
        matched_nodes.append("asana")
    if any(w in prompt_lower for w in ["zendesk", "zendesk ticket", "support ticket", "create ticket"]):
        matched_nodes.append("zendesk")
    if any(w in prompt_lower for w in ["stripe", "stripe payment", "payment", "billing"]):
        matched_nodes.append("stripe")
    if any(w in prompt_lower for w in ["mongodb", "database", "mongo", "store in database", "save to db"]):
        matched_nodes.append("mongodb")
    if any(w in prompt_lower for w in ["api", "http request", "call api", "post request", "fetch data"]):
        matched_nodes.append("http")
    if any(w in prompt_lower for w in ["validate", "parse", "transform", "convert", "process", "analyze", "custom logic"]):
        matched_nodes.append("function")
    if any(w in prompt_lower for w in ["hubspot", "crm", "customer", "lead"]):
        matched_nodes.append("slack")  # Placeholder for unknown services
    if any(w in prompt_lower for w in ["twitter", "tweet", "post to twitter", "share on twitter"]):
        matched_nodes.append("slack")  # Placeholder
    if any(w in prompt_lower for w in ["linkedin", "linkedin post", "share on linkedin"]):
        matched_nodes.append("slack")  # Placeholder
    if any(w in prompt_lower for w in ["teams", "microsoft teams", "post to teams"]):
        matched_nodes.append("discord")  # Similar notification service
    if any(w in prompt_lower for w in ["wordpress", "blog post", "publish"]):
        matched_nodes.append("http")  # HTTP to wordpress
    if any(w in prompt_lower for w in ["quickbooks", "invoice", "accounting"]):
        matched_nodes.append("http")  # Accounting services via API
    
    # Remove duplicates while preserving order
    seen = set()
    unique_nodes = []
    for node in matched_nodes:
        if node not in seen:
            seen.add(node)
            unique_nodes.append(node)
    matched_nodes = unique_nodes
    
    # If no nodes matched, return default with more options
    if not matched_nodes:
        return ["webhook", "slack", "email", "sheets"]
    
    # Limit to reasonable count (max 8) but keep minimum of 2
    if len(matched_nodes) > 8:
        matched_nodes = matched_nodes[:8]
    elif len(matched_nodes) < 2:
        matched_nodes.append("slack")  # Add at least 2
    
    return matched_nodes

def build_workflow(prompt: str, node_types: list) -> dict:
    """Build an n8n workflow from node types."""
    workflow = {
        "name": prompt[:50] or "Generated Workflow",
        "active": False,
        "settings": {},
        "nodes": [],
        "connections": {}
    }
    
    x_pos = 250
    y_pos = 300
    prev_node = None
    
    for node_type in node_types:
        if node_type not in NODE_TEMPLATES:
            continue
        
        template = NODE_TEMPLATES[node_type]
        node = {
            "name": template["name"],
            "type": template["type"],
            "typeVersion": 1,
            "position": [x_pos, y_pos],
            "parameters": {},
            "disabled": node_type not in ["webhook", "schedule", "set", "function"],
            "credentials": []
        }
        
        # Add some basic parameters
        if node_type == "slack":
            node["parameters"] = {"channel": "#general", "text": "Action performed"}
        elif node_type == "email":
            node["parameters"] = {"to": "admin@example.com", "subject": "Notification"}
        elif node_type == "gmail":
            node["parameters"] = {"to": "user@example.com", "subject": "Update"}
        elif node_type == "sheets":
            node["parameters"] = {"operation": "append", "documentId": "SHEET_ID", "sheetName": "Sheet1"}
        
        workflow["nodes"].append(node)
        
        # Create connection from previous node
        if prev_node and len(workflow["nodes"]) > 1:
            prev_name = workflow["nodes"][-2]["name"]
            curr_name = node["name"]
            if prev_name not in workflow["connections"]:
                workflow["connections"][prev_name] = {"main": []}
            workflow["connections"][prev_name]["main"].append({
                "node": curr_name,
                "branch": 0,
                "type": "main"
            })
        
        prev_node = node
        x_pos += 200  # Shift right for next node
    
    return workflow

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "model": "lightweight_test"})

@app.route("/generate", methods=["POST"])
def generate():
    """Generate n8n workflow with node count based on prompt complexity."""
    prompt = (request.get_json() or {}).get("prompt", "")
    
    # Detect which nodes to include based on prompt
    node_types = keyword_to_nodes(prompt)
    
    # Build workflow
    workflow = build_workflow(prompt, node_types)
    
    return jsonify({"workflow": workflow, "method": "local"})

if __name__ == "__main__":
    print("\n" + "="*70)
    print("[STARTING] LLM Server (Lightweight Mode)")
    print("="*70)
    print("[...] Initializing Flask app...")
    print("[...] Loading keyword mappings...")
    print("[✓] Ready!")
    print("")
    print("Server listening on http://127.0.0.1:8000")
    print("Endpoints: /health, /generate")
    print("="*70 + "\n")
    app.run(host="127.0.0.1", port=8000, debug=False)
