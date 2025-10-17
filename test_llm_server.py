"""
Lightweight test LLM server that emulates the /generate endpoint.
Returns reasonable n8n workflows for various prompts.
Used for validation when real LLM server is unavailable.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time

app = Flask(__name__)
CORS(app)

# Simple prompt-to-workflow templates
WORKFLOW_TEMPLATES = {
    "webhook": {
        "nodes": [
            {
                "name": "Webhook Trigger",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [250, 300],
                "parameters": {"path": "webhook", "method": "POST"},
                "credentials": []
            },
            {
                "name": "Slack Message",
                "type": "n8n-nodes-base.slack",
                "typeVersion": 1,
                "position": [450, 300],
                "parameters": {"resource": "message", "operation": "post", "channel": "#general", "text": "New webhook data received"},
                "disabled": True,
                "credentials": []
            }
        ],
        "connections": {
            "Webhook Trigger": {"main": [{"node": "Slack Message", "branch": 0, "type": "main"}]}
        }
    },
    "schedule": {
        "nodes": [
            {
                "name": "Schedule Trigger",
                "type": "n8n-nodes-base.scheduleTrigger",
                "typeVersion": 1,
                "position": [250, 300],
                "parameters": {"triggerTimes": {"item": [{"mode": "everyHour"}]}},
                "credentials": []
            },
            {
                "name": "Send Email",
                "type": "n8n-nodes-base.emailSend",
                "typeVersion": 1,
                "position": [450, 300],
                "parameters": {"to": "admin@example.com", "subject": "Scheduled Report", "message": "Your hourly report is ready"},
                "disabled": True,
                "credentials": []
            }
        ],
        "connections": {
            "Schedule Trigger": {"main": [{"node": "Send Email", "branch": 0, "type": "main"}]}
        }
    },
    "form": {
        "nodes": [
            {
                "name": "Form Trigger",
                "type": "n8n-nodes-base.formTrigger",
                "typeVersion": 1,
                "position": [250, 300],
                "parameters": {"formTitle": "Feedback Form", "formDescription": "Submit your feedback"},
                "credentials": []
            },
            {
                "name": "Google Sheets",
                "type": "n8n-nodes-base.googleSheets",
                "typeVersion": 3,
                "position": [450, 300],
                "parameters": {"resource": "sheet", "operation": "append", "documentId": "REPLACE_WITH_SHEET_ID", "sheetName": "Responses"},
                "disabled": True,
                "credentials": []
            },
            {
                "name": "Discord Notification",
                "type": "n8n-nodes-base.discord",
                "typeVersion": 1,
                "position": [650, 300],
                "parameters": {"resource": "message", "operation": "send", "text": "New form submission received"},
                "disabled": True,
                "credentials": []
            }
        ],
        "connections": {
            "Form Trigger": {"main": [{"node": "Google Sheets", "branch": 0, "type": "main"}]},
            "Google Sheets": {"main": [{"node": "Discord Notification", "branch": 0, "type": "main"}]}
        }
    },
    "multi_app": {
        "nodes": [
            {
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [250, 300],
                "parameters": {"path": "webhook", "method": "POST"},
                "credentials": []
            },
            {
                "name": "Parse Data",
                "type": "n8n-nodes-base.set",
                "typeVersion": 1,
                "position": [450, 300],
                "parameters": {"options": {}},
                "credentials": []
            },
            {
                "name": "Slack",
                "type": "n8n-nodes-base.slack",
                "typeVersion": 1,
                "position": [650, 300],
                "parameters": {"resource": "message", "operation": "post", "channel": "#alerts", "text": "Alert: new data processed"},
                "disabled": True,
                "credentials": []
            },
            {
                "name": "Gmail",
                "type": "n8n-nodes-base.gmail",
                "typeVersion": 1,
                "position": [650, 450],
                "parameters": {"resource": "message", "operation": "send", "to": "user@example.com", "subject": "Data Update", "message": "Your data has been processed"},
                "disabled": True,
                "credentials": []
            },
            {
                "name": "Notion",
                "type": "n8n-nodes-base.notion",
                "typeVersion": 2,
                "position": [850, 300],
                "parameters": {"resource": "page", "operation": "create", "databaseId": "REPLACE_WITH_DB_ID", "propertiesUi": {"property": []}},
                "disabled": True,
                "credentials": []
            },
            {
                "name": "Airtable",
                "type": "n8n-nodes-base.airtable",
                "typeVersion": 3,
                "position": [850, 450],
                "parameters": {"operation": "append", "baseId": "REPLACE_WITH_BASE", "tableId": "REPLACE_WITH_TABLE"},
                "disabled": True,
                "credentials": []
            }
        ],
        "connections": {
            "Webhook": {"main": [{"node": "Parse Data", "branch": 0, "type": "main"}]},
            "Parse Data": {"main": [
                {"node": "Slack", "branch": 0, "type": "main"},
                {"node": "Gmail", "branch": 0, "type": "main"},
                {"node": "Notion", "branch": 0, "type": "main"},
                {"node": "Airtable", "branch": 0, "type": "main"}
            ]}
        }
    }
}

def get_workflow_for_prompt(prompt: str) -> dict:
    """Return a reasonable n8n workflow based on the prompt."""
    prompt_lower = prompt.lower()
    
    # Try to match keywords to workflow type
    if any(word in prompt_lower for word in ["webhook", "receive", "incoming", "http", "trigger", "api"]):
        template = "webhook"
    elif any(word in prompt_lower for word in ["schedule", "every", "daily", "hourly", "cron", "time"]):
        template = "schedule"
    elif any(word in prompt_lower for word in ["form", "form submission", "submit", "questionnaire"]):
        template = "form"
    elif any(word in prompt_lower for word in ["multiple", "apps", "many", "complex", "several"]):
        template = "multi_app"
    else:
        # Default to multi-app for unknown/complex prompts
        template = "multi_app"
    
    base_workflow = WORKFLOW_TEMPLATES[template]
    
    # Make a deep copy and customize name
    workflow = {
        "name": prompt[:50] or "Generated Workflow",
        "active": False,
        "settings": {},
        "nodes": json.loads(json.dumps(base_workflow["nodes"])),
        "connections": json.loads(json.dumps(base_workflow["connections"]))
    }
    
    return workflow

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"ok": True, "model": "test_llm_server"})

@app.route("/generate", methods=["POST"])
def generate():
    """Generate an n8n workflow from a prompt."""
    try:
        data = request.get_json(silent=True) or {}
        prompt = data.get("prompt", "").strip()
        
        if not prompt:
            return jsonify({"error": "prompt is required"}), 400
        
        workflow = get_workflow_for_prompt(prompt)
        
        return jsonify({
            "workflow": workflow,
            "method": "local",
            "note": "test_llm_server - lightweight endpoint for validation"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    """Root endpoint info."""
    return jsonify({
        "name": "Test LLM Server",
        "version": "1.0",
        "endpoints": ["/health", "/generate"],
        "purpose": "Lightweight test server for validation when real LLM unavailable"
    })

if __name__ == "__main__":
    print("=" * 70)
    print("TEST LLM SERVER (Lightweight)")
    print("=" * 70)
    print("[*] Starting test server on http://127.0.0.1:8000")
    print("[+] /health     - Health check")
    print("[+] /generate   - Generate n8n workflows")
    print("=" * 70)
    app.run(host="0.0.0.0", port=8000, debug=False, threaded=True)
