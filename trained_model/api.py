#!/usr/bin/env python
"""
Local N8N Workflow Generator API
Provides an API endpoint for the Flask app to call inference
"""

from flask import Flask, request, jsonify
import json
import sys
from pathlib import Path
from inference import N8NWorkflowGenerator

app = Flask(__name__)

# Global generator instance (loaded once)
generator = None

def load_generator():
    """Load the model once on startup"""
    global generator
    if generator is None:
        print("[*] Loading N8N Workflow Generator...")
        try:
            # Try with quantization first (uses less memory)
            generator = N8NWorkflowGenerator(
                model_dir=".",
                use_quantization=True,
                device="cuda"
            )
        except Exception as e:
            print(f"[WARNING] Quantization failed: {e}")
            print("[*] Trying without quantization...")
            try:
                generator = N8NWorkflowGenerator(
                    model_dir=".",
                    use_quantization=False,
                    device="cuda"
                )
            except Exception as e2:
                print(f"[WARNING] CUDA failed: {e2}")
                print("[*] Falling back to CPU...")
                generator = N8NWorkflowGenerator(
                    model_dir=".",
                    use_quantization=False,
                    device="cpu"
                )
        print("[OK] Model loaded!")
    return generator


@app.route('/generate', methods=['POST'])
def generate():
    """Generate workflow from prompt"""
    try:
        data = request.get_json(silent=True) or {}
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        gen = load_generator()
        result = gen.generate_workflow_json(prompt)
        
        if result['success']:
            return jsonify({
                'success': True,
                'workflow': result['workflow'],
                'prompt': prompt
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Generation failed')
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    print("=" * 60)
    print("[SERVER] N8N Workflow Generator - Local API")
    print("=" * 60)
    print("[INFO] Starting on http://127.0.0.1:8000")
    print("[INFO] Endpoint: POST http://127.0.0.1:8000/generate")
    print("=" * 60)
    
    # Load model on startup
    try:
        load_generator()
        print("[OK] API Ready!")
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}")
        sys.exit(1)
    
    app.run(host='127.0.0.1', port=8000, debug=False)
