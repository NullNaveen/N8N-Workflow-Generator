# N8N Workflow Generator - System Overview

## Architecture

```
User Interface (index.html)
         ↓
    Flask Backend (app.py)
         ↓
   ┌─────┴──────┐
   ↓            ↓
Local API   Groq API
(api.py)    (fallback)
   ↓
Inference Model
(inference.py)
   ↓
N8N JSON Workflow
```

## Components

### 1. Frontend (index.html)
- Chat interface for users to describe workflows
- Sends prompts to `/api/generate` endpoint
- Displays generated workflows
- Download functionality for JSON files

### 2. Backend (app.py)
- Flask application running on port 5000
- `/api/generate` - generates workflows from prompts
- Tries local inference first, falls back to Groq API
- Validates and enhances generated workflows

### 3. Local Inference (api.py)
- Runs on http://127.0.0.1:8000
- Wraps the fine-tuned LLM model
- Accepts prompts and returns JSON workflows
- Auto-loads model on startup

### 4. Model (inference.py + trained weights)
- Fine-tuned Mistral-7B-Instruct-v0.2 with LoRA
- Generates n8n workflow JSON from natural language
- Supports both GPU and CPU execution

## Installation & Setup

### Prerequisites
- Python 3.8+
- 6GB+ VRAM (GPU) or 32GB+ RAM (CPU)
- Internet for downloading model

### Step 1: Install Dependencies
```bash
pip install flask flask-cors python-dotenv requests transformers peft accelerate torch
```

### Step 2: Set Up Models Directory
```bash
# Copy model files to trained_model/ folder
# Required files:
#   - adapter_model.safetensors
#   - tokenizer.model
#   - adapter_config.json
#   - tokenizer_config.json
```

### Step 3: Optional - Configure Groq API
Edit `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get free key from: https://console.groq.com/keys

## Running the System

### Option 1: With Local Inference (Recommended)

**Terminal 1 - Start inference API:**
```bash
cd trained_model
python api.py
# Listen on http://127.0.0.1:8000
```

**Terminal 2 - Start Flask app:**
```bash
python app.py
# Open browser to http://localhost:5000
```

### Option 2: Without Local Inference (Groq Only)
```bash
python app.py
# Will use Groq API (requires valid API key)
```

## Usage

1. Open http://localhost:5000 in browser
2. Type a workflow description, e.g.:
   - "Send email when webhook receives data"
   - "Create Slack message every day at 9am"
   - "Save form responses to Google Sheets"
3. Click Send or press Enter
4. Review generated workflow
5. Download JSON file
6. Import into n8n

## API Endpoints

### POST /api/generate
Generate workflow from prompt

**Request:**
```json
{
  "prompt": "Create a workflow that..."
}
```

**Response:**
```json
{
  "success": true,
  "workflow": { ... },
  "prompt": "...",
  "method": "local" or "groq"
}
```

### GET /api/examples
Get example prompts

**Response:**
```json
[
  "Send an email when...",
  "Create a Slack message...",
  ...
]
```

## File Structure

```
N8N/
├── app.py                              # Flask backend
├── index.html                          # Web UI
├── training_examples.json              # Example workflows
├── .env.example                        # Example config
├── .env                                # Your config (ignored by git)
│
└── trained_model/
    ├── inference.py                    # Inference class
    ├── api.py                          # Local API server
    ├── adapter_model.safetensors       # LoRA weights
    ├── tokenizer.model                 # Tokenizer
    ├── adapter_config.json             # Model config
    ├── tokenizer_config.json           # Tokenizer config
    ├── README.md                       # Model docs
    └── QUICKSTART.md                   # Quick start
```

## Performance

### Speed
- **Model Loading**: 30-60 seconds (first time)
- **Generation**: 30-120 seconds per prompt (on CPU)
- **GPU**: 5-20 seconds per prompt

### Memory
- **Quantized GPU**: 5-6 GB VRAM
- **FP16 GPU**: 12-14 GB VRAM
- **CPU**: 20-32 GB RAM

## Features

### Workflow Generation
- Converts natural language to n8n workflow JSON
- Supports 40+ node types (email, Slack, webhook, etc.)
- Auto-configures safe defaults
- Disables nodes requiring credentials

### Fallback System
- **Primary**: Local fine-tuned model
- **Fallback 1**: Groq API (if configured)
- **Fallback 2**: Rule-based generation

### Safety
- Input validation
- JSON validation
- Error handling
- Graceful degradation

## Known Limitations

### Model
- Takes time to load on CPU (use GPU for production)
- May require prompt refinement
- Best with specific, clear descriptions

### API
- Groq API key in .env.example is expired (provide your own)
- Local model requires 30+ GB disk space for download
- Inference time depends on hardware

### Workflows
- Generated workflows may need tweaking
- External service nodes are disabled by default
- Complex workflows may need manual refinement

## Troubleshooting

### "Model not found"
- Check `trained_model/` contains all files
- Verify file paths

### "Out of memory"
- Use quantization (default in api.py)
- Reduce batch size
- Use GPU instead of CPU

### "Groq API error"
- Provide valid API key in `.env`
- Check internet connection
- System will fall back to local model

### Slow generation
- Use GPU for 5-10x speedup
- Local model will take 1-2 minutes on CPU
- This is expected and normal

## Development

### Customize System Prompt
Edit `create_system_prompt()` in app.py to change generation behavior

### Add New Node Types
Update `NODE_TYPES` in app.py

### Extend Validation
Modify `ensure_required_defaults()` in app.py

## Production Deployment

### Docker
```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

### Cloud Platforms
- **AWS Lambda**: Use container image
- **Google Cloud**: Run container on Cloud Run
- **Azure**: Deploy to App Service

### Performance Tips
- Use GPU instances
- Enable request queuing
- Cache frequent prompts
- Monitor API usage

## Support

### Resources
- Groq Docs: https://console.groq.com/docs
- n8n Docs: https://docs.n8n.io/
- Model: Mistral-7B-Instruct-v0.2

### Common Tasks
- **Change model**: Update base_model in inference.py
- **Fine-tune**: Use training notebook
- **Debug**: Check console output for detailed errors

---

**Status**: Production Ready (with noted limitations)  
**Last Updated**: October 17, 2025  
**Model**: Mistral-7B-Instruct v0.2 + LoRA  
**Frontend**: HTML5 + JavaScript  
**Backend**: Python 3.8+
