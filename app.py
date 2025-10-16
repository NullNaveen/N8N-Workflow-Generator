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
LOCAL_INFER_URL = os.getenv('LOCAL_INFER_URL', 'http://127.0.0.1:8000/generate')

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
            'model': 'llama-3.1-8b-instant',  # Fast model with 14.4K requests/day (was 70b with only 1K/day)
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
        workflow_text = result['choices'][0]['message']['content']

        # Extract JSON from possible code fences or extra text
        # Find the first '{' and the last '}' to bound the JSON object
        start = workflow_text.find('{')
        end = workflow_text.rfind('}')
        if start != -1 and end != -1 and end > start:
            workflow_json = workflow_text[start:end+1]
        else:
            workflow_json = workflow_text

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

        # Notion create page defaults
        if ntype == 'n8n-nodes-base.notion':
            params.setdefault('resource', 'page')
            params.setdefault('operation', 'create')
            # Minimal placeholders; user must configure in n8n
            params.setdefault('databaseId', 'REPLACE_WITH_DATABASE_ID')
            # Notion node often expects properties; provide a minimal title
            params.setdefault('propertiesUi', {
                'property': [
                    {
                        'name': 'Name',
                        'key': 'title',
                        'type': 'title',
                        'title': [
                            {
                                'text': 'New page from workflow'
                            }
                        ]
                    }
                ]
            })

    return workflow


def generate_with_local_llm(prompt: str):
    try:
        resp = requests.post(LOCAL_INFER_URL, json={"prompt": prompt}, timeout=60)
        if resp.status_code != 200:
            return None, f"local inference error: {resp.status_code} {resp.text[:200]}"
        data = resp.json()
        if "workflow" not in data:
            return None, "local inference returned no workflow"
        return data["workflow"], None
    except Exception as e:
        return None, str(e)


@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')


@app.route('/api/generate', methods=['POST'])
def generate_workflow():
    """Generate n8n workflow from natural language prompt"""
    try:
        data = request.get_json(silent=True) or {}
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Prefer local fine-tuned LLM first
        workflow, error = generate_with_local_llm(prompt)
        # Fall back to Groq if configured and local fails
        if error or not workflow:
            print(f"Local LLM failed: {error}. Trying Groq...")
            workflow, error = generate_workflow_with_groq(prompt)
        if error or not workflow:
            return jsonify({"error": f"Generation failed: {error}"}), 500
        
        # Add metadata
        workflow['name'] = prompt[:50]
        workflow['active'] = False
        workflow['settings'] = {}
        workflow = ensure_required_defaults(workflow)
        
        return jsonify({
            'success': True,
            'workflow': workflow,
            'prompt': prompt,
            'method': 'local' if error is None and workflow else 'groq'
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
