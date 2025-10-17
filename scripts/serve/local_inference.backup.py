import os
import json
from flask import Flask, request, jsonify

"""
Local inference server for the fine-tuned adapter.
Environment variables:
- BASE_MODEL: base HF model id (default mistralai/Mistral-7B-Instruct-v0.3)
- ADAPTER_PATH: path to LoRA adapter (default models/n8n-lora)
"""

app = Flask(__name__)


def load_model():
    from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
    from peft import PeftModel
    import torch
    base = os.environ.get("BASE_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
    adapter = os.environ.get("ADAPTER_PATH", "models/n8n-lora")

    tokenizer = AutoTokenizer.from_pretrained(adapter if os.path.exists(adapter) else base, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    base_model = AutoModelForCausalLM.from_pretrained(base, torch_dtype=torch.float16, device_map="auto")
    model = PeftModel.from_pretrained(base_model, adapter, is_trainable=False)
    model.eval()
    return tokenizer, model


tokenizer, model = None, None


def _init():
    global tokenizer, model
    if tokenizer is None:
        tokenizer, model = load_model()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True})


@app.route("/generate", methods=["POST"])
def generate():
    _init()  # Ensure model is loaded
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "prompt is required"}), 400

    system = (
        "You are an expert n8n workflow designer. Convert the user's prompt to a valid n8n JSON workflow. "
        "Return ONLY JSON."
    )
    text = (
        f"<s>[SYSTEM]\n{system}\n[/SYSTEM]\n[USER]\n{prompt}\n[/USER]\n[ASSISTANT]\n"
    )

    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=1024,
            do_sample=True,
            temperature=0.2,
            top_p=0.95,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    full = tokenizer.decode(out[0], skip_special_tokens=True)
    # Extract JSON
    start = full.find('{')
    end = full.rfind('}')
    if start != -1 and end != -1 and end > start:
        content = full[start:end+1]
    else:
        content = full
    # Validate JSON
    try:
        workflow = json.loads(content)
    except Exception as e:
        return jsonify({"error": f"invalid json: {str(e)}", "raw": full[-2000:]}), 500
    return jsonify({"workflow": workflow, "method": "local"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
