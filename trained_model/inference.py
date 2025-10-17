"""
N8N Workflow Generator - Production Inference Script
Uses the trained LoRA adapter with Mistral-7B to generate n8n workflows
"""

import torch
import json
import os
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

class N8NWorkflowGenerator:
    """Generate n8n workflows from natural language descriptions using fine-tuned Mistral-7B"""
    
    def __init__(self, model_dir=".", use_quantization=True, device="cuda"):
        """
        Initialize the workflow generator
        
        Args:
            model_dir: Path to the trained model directory
            use_quantization: Whether to use 4-bit quantization (default: True)
            device: Device to use (cuda/cpu)
        """
        self.model_dir = Path(model_dir)
        self.device = device
        self.use_quantization = use_quantization
        
        print(f"[*] Loading N8N Workflow Generator from {self.model_dir}...")
        self._load_model()
        print("[OK] Model loaded successfully!")
    
    def _load_model(self):
        """Load the base model and LoRA adapter"""
        base_model = "mistralai/Mistral-7B-Instruct-v0.2"
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = 'right'
        
        # Load base model with memory-efficient settings
        try:
            # Try GPU first with reduced memory usage
            if torch.cuda.is_available():
                print("[*] Attempting GPU loading with memory optimization...")
                self.model = AutoModelForCausalLM.from_pretrained(
                    base_model,
                    torch_dtype=torch.float16,
                    device_map="auto",
                    max_memory={0: "6GB", "cpu": "8GB"},  # Limit GPU memory
                    offload_folder="./offload_tmp",
                    low_cpu_mem_usage=True
                )
            else:
                raise Exception("No CUDA available")
        except Exception as e:
            print(f"[WARNING] GPU loading failed ({e}), trying CPU...")
            try:
                # Fallback to CPU with disk offload
                self.model = AutoModelForCausalLM.from_pretrained(
                    base_model,
                    torch_dtype=torch.float32,  # CPU needs float32
                    device_map="cpu",
                    low_cpu_mem_usage=True,
                    offload_folder="./offload_tmp"
                )
                self.device = "cpu"
                print("[*] Using CPU inference (slower but works)")
            except Exception as e2:
                print(f"[ERROR] Both GPU and CPU loading failed: {e2}")
                raise
        
        # Load LoRA adapter
        self.model = PeftModel.from_pretrained(self.model, self.model_dir)
        self.model.eval()
    
    def generate(self, prompt, max_length=2048, temperature=0.7, top_p=0.9, num_return_sequences=1):
        """
        Generate n8n workflow from a natural language description
        
        Args:
            prompt: Natural language description of the workflow
            max_length: Maximum length of generated text
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            num_return_sequences: Number of variants to generate
            
        Returns:
            list: Generated workflows
        """
        # Format prompt in the same style as training
        formatted_prompt = f"""<|system|>
You are an n8n workflow generator. Convert natural language descriptions into valid n8n workflow JSON.
<|user|>
{prompt}
<|assistant|>
"""
        
        # Tokenize
        inputs = self.tokenizer(
            formatted_prompt,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.device)
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                num_return_sequences=num_return_sequences,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode
        generated_texts = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        
        # Extract just the assistant response
        workflows = []
        for text in generated_texts:
            # Split by assistant marker and get the part after it
            if "<|assistant|>" in text:
                response = text.split("<|assistant|>")[-1].strip()
                workflows.append(response)
            else:
                workflows.append(text)
        
        return workflows
    
    def generate_workflow_json(self, prompt):
        """
        Generate a complete n8n workflow and parse JSON if possible
        
        Args:
            prompt: Natural language description
            
        Returns:
            dict: Parsed workflow JSON or raw text if parsing fails
        """
        workflows = self.generate(prompt, num_return_sequences=1)
        raw_workflow = workflows[0]
        
        # Try to parse JSON
        try:
            # Find JSON in the response
            json_start = raw_workflow.find('{')
            json_end = raw_workflow.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = raw_workflow[json_start:json_end]
                workflow_json = json.loads(json_str)
                return {
                    "success": True,
                    "workflow": workflow_json,
                    "raw": raw_workflow
                }
        except (json.JSONDecodeError, ValueError) as e:
            print(f"[WARNING] JSON parsing failed: {e}")
        
        return {
            "success": False,
            "workflow": None,
            "raw": raw_workflow,
            "error": "Could not parse JSON from response"
        }


def main():
    """Example usage"""
    # Initialize generator
    generator = N8NWorkflowGenerator(model_dir=".", use_quantization=True)
    
    # Example prompts
    test_prompts = [
        "Create a workflow that receives data from a webhook, processes it, and sends an email notification",
        "Build a workflow that fetches data from an API every hour and stores it in a database",
        "Generate a workflow that listens for Slack messages and logs them to a file"
    ]
    
    print("\n" + "="*80)
    print("[RUN] N8N Workflow Generator - Demo")
    print("="*80 + "\n")
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"[TEST {i}] Example Prompt:")
        print(f"  Prompt: {prompt}\n")
        
        result = generator.generate_workflow_json(prompt)
        
        if result["success"]:
            print("[OK] Generated Workflow (JSON):")
            print(json.dumps(result["workflow"], indent=2))
        else:
            print("[OUTPUT] Generated Response:")
            print(result["raw"])
        
        print("\n" + "-"*80 + "\n")


if __name__ == "__main__":
    main()
