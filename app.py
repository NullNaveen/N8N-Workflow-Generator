"""
N8N Workflow Generator API
A Flask application that converts natural language prompts to n8n workflow JSON files
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import requests
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Load environment variables from .env, and if missing, fall back to .env.example (without overriding)
load_dotenv(override=False)
if not os.getenv('GROQ_API_KEY') and os.path.exists('.env.example'):
    load_dotenv('.env.example', override=False)

# Load training examples
with open('training_examples.json', 'r') as f:
    TRAINING_EXAMPLES = json.load(f)

# Configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')  # Groq API key from environment or .env files
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

# Common n8n node types and their purposes
NODE_TYPES = {
    "triggers": {
        "webhook": "n8n-nodes-base.webhook",
        "schedule": "n8n-nodes-base.scheduleTrigger",
        "cron": "n8n-nodes-base.cron",
        "manual": "n8n-nodes-base.manualTrigger",
        "gmail": "n8n-nodes-base.gmailTrigger",
        "google sheets": "n8n-nodes-base.googleSheetsTrigger",
        "github": "n8n-nodes-base.githubTrigger",
        "form": "n8n-nodes-base.formTrigger"
    },
    "actions": {
        "gmail": "n8n-nodes-base.gmail",
        "email": "n8n-nodes-base.emailSend",
        "slack": "n8n-nodes-base.slack",
        "discord": "n8n-nodes-base.discord",
        "google sheets": "n8n-nodes-base.googleSheets",
        "airtable": "n8n-nodes-base.airtable",
        "trello": "n8n-nodes-base.trello",
        "notion": "n8n-nodes-base.notion",
        "http": "n8n-nodes-base.httpRequest",
        "webhook response": "n8n-nodes-base.respondToWebhook"
    }
}

def create_system_prompt():
    """Create the system prompt for the LLM"""
    examples_text = "\n\n".join([
        f"Example {i+1}:\nPrompt: {ex['prompt']}\nWorkflow: {json.dumps(ex['workflow'], indent=2)}"
        for i, ex in enumerate(TRAINING_EXAMPLES[:3])
    ])
    
    return f"""You are an expert n8n workflow designer. Your task is to convert natural language automation requests into valid n8n workflow JSON.

N8N WORKFLOW STRUCTURE:
A workflow consists of:
1. "nodes": Array of node objects with name, type, position, parameters, and typeVersion
2. "connections": Object mapping node connections

COMMON NODE TYPES:
Triggers: {json.dumps(NODE_TYPES['triggers'], indent=2)}
Actions: {json.dumps(NODE_TYPES['actions'], indent=2)}

EXAMPLES:
{examples_text}

RULES:
1. Always include at least one trigger node (the starting point)
2. Position nodes horizontally: first node at [250, 300], next at [450, 300], etc. (increment x by 200)
3. Use simple, descriptive node names
4. Connect nodes in the "connections" object
5. Include typeVersion: 1 for all nodes
6. Return ONLY valid JSON, no markdown or explanations
7. If the request is unclear, create a basic workflow that matches the intent

Respond with ONLY the JSON workflow object."""


def generate_workflow_with_groq(prompt):
    """Generate workflow using Groq API (free tier)"""
    if not GROQ_API_KEY:
        return None, "Groq API key not configured"
    
    try:
        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'llama-3.1-70b-versatile',  # Free model
            'messages': [
                {'role': 'system', 'content': create_system_prompt()},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.3,
            'max_tokens': 2000
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        
    result = response.json()
    workflow_json = result['choices'][0]['message']['content']

    # Try to parse the JSON
    workflow = json.loads(workflow_json)
    return workflow, None
        
    except Exception as e:
        return None, str(e)


def ensure_required_defaults(workflow: dict) -> dict:
    """Ensure minimal required params so nodes import cleanly; also disable nodes needing credentials.
    - Add default params (e.g., Gmail send needs to/subject/message)
    - Disable external-action nodes so workflow can execute without credentials
    """
    nodes = workflow.get('nodes', [])
    for node in nodes:
        ntype = node.get('type', '')
        params = node.setdefault('parameters', {})

        # Heuristic: disable nodes that likely require credentials or external services
        external_types = (
            'n8n-nodes-base.gmail', 'n8n-nodes-base.slack', 'n8n-nodes-base.discord',
            'n8n-nodes-base.googleSheets', 'n8n-nodes-base.airtable', 'n8n-nodes-base.trello',
            'n8n-nodes-base.notion', 'n8n-nodes-base.httpRequest'
        )
        if any(ntype.endswith(ext.split('.')[-1]) for ext in external_types):
            node.setdefault('disabled', True)

        # Gmail send defaults
        if ntype == 'n8n-nodes-base.gmail':
            params.setdefault('resource', 'message')
            params.setdefault('operation', 'send')
            params.setdefault('to', 'you@example.com')
            params.setdefault('subject', 'Automated notification')
            params.setdefault('message', 'This is an automated message from your workflow.')

        # Slack post message defaults
        if ntype == 'n8n-nodes-base.slack':
            params.setdefault('resource', 'message')
            params.setdefault('operation', 'post')
            params.setdefault('channel', '#general')
            params.setdefault('text', 'Automated notification')

        # Discord send message defaults
        if ntype == 'n8n-nodes-base.discord':
            params.setdefault('resource', 'message')
            params.setdefault('operation', 'send')
            params.setdefault('text', 'Automated notification')
            params.setdefault('channelId', 'REPLACE_WITH_CHANNEL_ID')

        # Google Sheets append defaults
        if ntype == 'n8n-nodes-base.googleSheets':
            params.setdefault('operation', 'append')
            params.setdefault('resource', 'sheet')
            # Placeholders to avoid execution until user configures
            params.setdefault('documentId', 'REPLACE_WITH_SHEET_ID')
            params.setdefault('sheetName', 'Sheet1')

        # Google Sheets Trigger defaults (keep disabled until configured)
        if ntype == 'n8n-nodes-base.googleSheetsTrigger':
            node.setdefault('disabled', True)

    return workflow


def generate_workflow_fallback(prompt):
    """Fallback method using simple pattern matching"""
    prompt_lower = prompt.lower()
    
    # Detect trigger type
    trigger_node = None
    trigger_name = None
    
    if 'webhook' in prompt_lower or 'receive data' in prompt_lower:
        trigger_node = {
            "name": "Webhook",
            "type": "n8n-nodes-base.webhook",
            "position": [250, 300],
            "parameters": {"path": "automation", "responseMode": "lastNode"},
            "typeVersion": 1
        }
        trigger_name = "Webhook"
    elif 'schedule' in prompt_lower or 'every day' in prompt_lower or 'daily' in prompt_lower or 'time' in prompt_lower or 'every ' in prompt_lower:
        trigger_node = {
            "name": "Schedule Trigger",
            "type": "n8n-nodes-base.scheduleTrigger",
            "position": [250, 300],
            "parameters": {"rule": {"interval": [{"field": "hours", "hoursInterval": 24}]}},
            "typeVersion": 1
        }
        trigger_name = "Schedule Trigger"
    elif 'gmail' in prompt_lower or 'email received' in prompt_lower or 'new email' in prompt_lower:
        trigger_node = {
            "name": "Gmail Trigger",
            "type": "n8n-nodes-base.gmailTrigger",
            "position": [250, 300],
            "parameters": {"options": {}},
            "typeVersion": 1
        }
        trigger_name = "Gmail Trigger"
    elif ('google sheets' in prompt_lower or 'spreadsheet' in prompt_lower) and ('new row' in prompt_lower or 'added' in prompt_lower):
        trigger_node = {
            "name": "Google Sheets Trigger",
            "type": "n8n-nodes-base.googleSheetsTrigger",
            "position": [250, 300],
            "parameters": {"event": "rowAdded"},
            "typeVersion": 1,
            "disabled": True
        }
        trigger_name = "Google Sheets Trigger"
    else:
        # Default to manual trigger
        trigger_node = {
            "name": "Manual Trigger",
            "type": "n8n-nodes-base.manualTrigger",
            "position": [250, 300],
            "parameters": {},
            "typeVersion": 1
        }
        trigger_name = "Manual Trigger"
    
    # Detect action type
    action_node = None
    action_name = None
    
    if 'gmail' in prompt_lower or 'send email' in prompt_lower or ('email' in prompt_lower and 'trigger' not in prompt_lower):
        action_node = {
            "name": "Gmail",
            "type": "n8n-nodes-base.gmail",
            "position": [450, 300],
            "parameters": {
                "operation": "send",
                "resource": "message",
                "to": "you@example.com",
                "subject": "Automated notification",
                "message": "This is an automated message"
            },
            "typeVersion": 1,
            "disabled": True
        }
        action_name = "Gmail"
    elif 'slack' in prompt_lower:
        action_node = {
            "name": "Slack",
            "type": "n8n-nodes-base.slack",
            "position": [450, 300],
            "parameters": {
                "operation": "post",
                "resource": "message",
                "channel": "#general",
                "text": "Automated notification"
            },
            "typeVersion": 1,
            "disabled": True
        }
        action_name = "Slack"
    elif 'discord' in prompt_lower:
        action_node = {
            "name": "Discord",
            "type": "n8n-nodes-base.discord",
            "position": [450, 300],
            "parameters": {
                "resource": "message",
                "operation": "send",
                "text": "Automated notification",
                "channelId": "REPLACE_WITH_CHANNEL_ID"
            },
            "typeVersion": 1,
            "disabled": True
        }
        action_name = "Discord"
    elif 'google sheets' in prompt_lower or 'spreadsheet' in prompt_lower:
        action_node = {
            "name": "Google Sheets",
            "type": "n8n-nodes-base.googleSheets",
            "position": [450, 300],
            "parameters": {
                "operation": "append",
                "resource": "sheet",
                "documentId": "REPLACE_WITH_SHEET_ID",
                "sheetName": "Sheet1"
            },
            "typeVersion": 1,
            "disabled": True
        }
        action_name = "Google Sheets"
    elif 'trello' in prompt_lower:
        action_node = {
            "name": "Trello",
            "type": "n8n-nodes-base.trello",
            "position": [450, 300],
            "parameters": {
                "operation": "create",
                "resource": "card",
                "name": "New card"
            },
            "typeVersion": 1,
            "disabled": True
        }
        action_name = "Trello"
    elif 'airtable' in prompt_lower:
        action_node = {
            "name": "Airtable",
            "type": "n8n-nodes-base.airtable",
            "position": [450, 300],
            "parameters": {
                "operation": "create",
                "resource": "row"
            },
            "typeVersion": 1,
            "disabled": True
        }
        action_name = "Airtable"
    else:
        # Default to HTTP request
        action_node = {
            "name": "HTTP Request",
            "type": "n8n-nodes-base.httpRequest",
            "position": [450, 300],
            "parameters": {
                "method": "POST",
                "url": ""
            },
            "typeVersion": 1,
            "disabled": True
        }
        action_name = "HTTP Request"
    
    # Build workflow
    workflow = {
        "nodes": [trigger_node, action_node],
        "connections": {
            trigger_name: {
                "main": [[{"node": action_name, "type": "main", "index": 0}]]
            }
        }
    }
    
    return ensure_required_defaults(workflow)


@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')


@app.route('/api/generate', methods=['POST'])
def generate_workflow():
    """Generate n8n workflow from natural language prompt"""
    try:
        data = request.json
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Try Groq API first
        workflow, error = generate_workflow_with_groq(prompt)
        
        # If Groq fails, use fallback
        if error or not workflow:
            print(f"Groq failed: {error}, using fallback method")
            workflow = generate_workflow_fallback(prompt)
        
        # Add metadata
        workflow['name'] = prompt[:50]
        workflow['active'] = False
        workflow['settings'] = {}
        workflow = ensure_required_defaults(workflow)
        
        return jsonify({
            'success': True,
            'workflow': workflow,
            'prompt': prompt,
            'method': 'groq' if not error else 'fallback'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Get training examples"""
    return jsonify([ex['prompt'] for ex in TRAINING_EXAMPLES])


if __name__ == '__main__':
    print("=" * 60)
    print("N8N WORKFLOW GENERATOR")
    print("=" * 60)
    print(f"Server starting...")
    print(f"Open your browser to: http://localhost:5000")
    print(f"Groq API configured: {'Yes' if GROQ_API_KEY else 'No (using fallback)'}")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
