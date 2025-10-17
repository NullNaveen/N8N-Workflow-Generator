"""
Real AI-powered N8N Workflow Generator Server
Uses the trained LoRA adapter - NO RULE-BASED FALLBACKS
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import sys
import traceback

# Add the trained_model directory to path so we can import inference.py
sys.path.insert(0, 'trained_model')

try:
    from inference import N8NWorkflowGenerator
    HAS_MODEL = True
except ImportError as e:
    print(f"WARNING: Could not import trained model: {e}")
    HAS_MODEL = False

app = Flask(__name__)
CORS(app)

# Global generator instance
generator = None

def init_model():
    """Initialize the trained model generator"""
    global generator
    if generator is None and HAS_MODEL:
        try:
            print("[*] Loading trained N8N model...")
            generator = N8NWorkflowGenerator(
                model_dir="trained_model", 
                use_quantization=True  # Use 4-bit quantization to save memory
            )
            print("[OK] Model loaded successfully!")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to load model: {e}")
            traceback.print_exc()
            return False
    return HAS_MODEL and generator is not None

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/api/generate', methods=['POST'])
def generate_workflow():
    """Generate n8n workflow using the trained AI model - NO RULE-BASED FALLBACKS"""
    try:
        data = request.get_json(silent=True) or {}
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Initialize model if needed
        if not init_model():
            return jsonify({
                'error': 'AI model not available. Please ensure the trained model is properly installed.',
                'details': 'The system requires the trained LoRA adapter to be loaded.'
            }), 500
        
        print(f"[AI] Processing prompt: {prompt[:100]}...")
        
        # Generate workflow using trained AI
        result = generator.generate_workflow_json(prompt)
        
        if result['success']:
            workflow = result['workflow']
            
            # Ensure required fields
            if 'name' not in workflow:
                workflow['name'] = prompt[:50]
            if 'active' not in workflow:
                workflow['active'] = False
            if 'settings' not in workflow:
                workflow['settings'] = {}
            
            return jsonify({
                'success': True,
                'workflow': workflow,
                'prompt': prompt,
                'method': 'trained_ai',
                'raw_output': result.get('raw', '')[:500]  # Include sample of raw output
            })
        else:
            return jsonify({
                'error': 'AI model could not generate valid workflow JSON',
                'raw_output': result.get('raw', ''),
                'details': result.get('error', 'Unknown error')
            }), 500
            
    except Exception as e:
        print(f"[ERROR] Workflow generation failed: {e}")
        traceback.print_exc()
        return jsonify({
            'error': f'Workflow generation failed: {str(e)}',
            'type': 'server_error'
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get model status"""
    model_ready = init_model()
    return jsonify({
        'model_loaded': model_ready,
        'model_type': 'trained_lora_adapter' if model_ready else 'none',
        'has_model_files': HAS_MODEL
    })

@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Get example prompts for testing"""
    examples = [
        "Whenever I receive a customer support email, save attachments to Drive, create a Zendesk ticket, send auto-response, and notify support team on Slack",
        "Monitor Google Sheets for new rows where sales > $5000, send Slack alert, SMS via Twilio, and log to another sheet",
        "When GitHub issue is created, create Trello card, notify team on Discord, send email to stakeholders, and update project dashboard",
        "Process webhook data, validate with custom function, store in MongoDB, send confirmation email, and trigger follow-up workflow",
        "Daily at 9am: fetch weather data, analyze trends, create report in Notion, share on Teams, and schedule next analysis",
        "When Stripe payment succeeds, update customer in HubSpot, send thank-you email, create invoice in QuickBooks, and notify accounting on Slack",
        "Monitor RSS feed, filter important articles, summarize with AI, post to WordPress, share on Twitter, and archive in Airtable",
        "When form submission received, validate data, save to database, send confirmation SMS, create lead in CRM, and trigger email sequence",
        "Process file upload, extract text with OCR, translate content, save to cloud storage, index in search engine, and notify reviewers",
        "When calendar event starts, send reminder emails, update project status, log time tracking, post to team chat, and sync with external tools"
    ]
    return jsonify(examples)

if __name__ == '__main__':
    print("=" * 70)
    print("🤖 N8N WORKFLOW GENERATOR - REAL AI MODE")
    print("=" * 70)
    print("🚀 Starting server...")
    print("🌐 Open your browser to: http://localhost:5000")
    print("🧠 Using trained LoRA adapter (NO rule-based fallbacks)")
    print("=" * 70)
    
    # Try to initialize model on startup
    if init_model():
        print("✅ AI model loaded successfully!")
    else:
        print("⚠️  AI model failed to load - server will return errors")
        print("   Make sure your trained model files are in 'trained_model/' folder")
    
    print("=" * 70)
    app.run(debug=True, host='0.0.0.0', port=5000)