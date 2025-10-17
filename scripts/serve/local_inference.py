import os
import json
from flask import Flask, request, jsonify
import traceback
import torch  # Needed at module scope for generate()

"""
Local inference server for the fine-tuned adapter.
Environment variables:
- BASE_MODEL: base HF model id (default mistralai/Mistral-7B-Instruct-v0.3)
- ADAPTER_PATH: path to LoRA adapter (default models/n8n-lora)
"""

app = Flask(__name__)


def load_model():
    """Load the primary model (Mistral + LoRA) with graceful CPU/small-model fallback.

    Primary: BASE_MODEL (default mistralai/Mistral-7B-Instruct-v0.2) + ADAPTER_PATH (LoRA)
    Fallback: FALLBACK_MODEL (default Qwen/Qwen2.5-1.5B-Instruct) without adapter
    """
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from peft import PeftModel

    base = os.environ.get("BASE_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
    adapter = os.environ.get("ADAPTER_PATH", "models/n8n-lora")
    fallback_id = os.environ.get("FALLBACK_MODEL", "Qwen/Qwen2.5-1.5B-Instruct")

    # Model info for health/debug
    info = {
        "base": base,
        "adapter": adapter,
        "using_fallback": False,
        "model_id": None,
    }

    # Prefer loading tokenizer from adapter dir if present; fall back to base
    source_for_tokenizer = adapter if os.path.exists(adapter) else base

    try:
        tokenizer = AutoTokenizer.from_pretrained(source_for_tokenizer, use_fast=True, trust_remote_code=True)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        # Load base model; let transformers decide device map; default to float16 if possible
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        base_model = AutoModelForCausalLM.from_pretrained(base, torch_dtype=dtype, device_map="auto", trust_remote_code=True)

        # Attach LoRA adapter only if adapter path exists and looks valid
        if os.path.isdir(adapter) and any(os.path.exists(os.path.join(adapter, fname)) for fname in ("adapter_config.json", "adapter_model.bin", "adapter_model.safetensors")):
            model = PeftModel.from_pretrained(base_model, adapter, is_trainable=False)
            info["model_id"] = f"{base} + {adapter}"
        else:
            # No adapter present; run base instruct model
            model = base_model
            info["model_id"] = base

        model.eval()
        return tokenizer, model, info
    except Exception as exc:
        # Log and attempt fallback
        print("[WARN] Primary model load failed; attempting fallback small model...\n", flush=True)
        traceback.print_exc()
        try:
            tokenizer = AutoTokenizer.from_pretrained(fallback_id, use_fast=True, trust_remote_code=True)
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            dtype = torch.float16 if torch.cuda.is_available() else torch.float32
            model = AutoModelForCausalLM.from_pretrained(fallback_id, torch_dtype=dtype, device_map="auto", trust_remote_code=True)
            model.eval()
            info.update({
                "using_fallback": True,
                "model_id": fallback_id,
            })
            print(f"[OK] Fallback model loaded: {fallback_id}", flush=True)
            return tokenizer, model, info
        except Exception:
            traceback.print_exc()
            raise


tokenizer, model = None, None
MODEL_INFO = None


def _init():
    global tokenizer, model, MODEL_INFO
    if tokenizer is None or model is None:
        try:
            tokenizer, model, MODEL_INFO = load_model()
        except Exception as exc:
            # Log full traceback to ease debugging
            traceback.print_exc()
            raise


@app.route("/health", methods=["GET"])
def health():
    # Initialize if not already, but don't crash health on failure
    try:
        _init()
        info = MODEL_INFO or {}
        return jsonify({"ok": True, "model": info})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


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
    # Keep a generic chat template that most instruct models can parse
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
    # Attach minimal model info in response for debugging; frontend ignores unknown keys
    resp = {"workflow": workflow, "method": "local"}
    if MODEL_INFO:
        resp["model"] = MODEL_INFO
    return jsonify(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
