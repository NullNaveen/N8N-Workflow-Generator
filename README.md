# N8N Workflow Generator - LLM-Powered

Convert natural language descriptions into ready-to-use n8n workflows.

## Quick Start

```powershell
# Terminal 1: Start LLM server
python simple_test_server.py

# Terminal 2: Start frontend
python app.py

# Browser: http://localhost:5000
```

## What It Does

**Input:**  
"When a WordPress post is published, shorten URL, post to Twitter/LinkedIn, log to Google Sheets"

**Output:**  
Valid n8n workflow JSON with multiple nodes, ready to import and use.

## Features

- ✅ Local LLM-only (no API keys, no costs)
- ✅ Generates 4-8 nodes per prompt
- ✅ Supports 20+ n8n integrations
- ✅ Web UI + API interface
- ✅ Download JSON immediately

## Installation

1. Install Python 3.8+
2. `pip install -r requirements.txt`
3. Run the quick start commands above

## File Structure

```
├── app.py                      # Frontend API (port 5000)
├── simple_test_server.py       # LLM server (port 8000)
├── test_complex_prompts.py     # Validation tests
├── scripts/serve/              # Real LLM model server
├── trained_model/              # Fine-tuned adapter
├── index.html                  # Web UI
├── QUICKSTART.md              # Detailed setup guide
└── requirements.txt           # Dependencies
```

## API Endpoints

**Frontend:**
- `POST /api/generate` - Generate workflow from prompt
- `GET /api/examples` - Example prompts

**LLM Server:**
- `POST /generate` - Generate n8n JSON
- `GET /health` - Health check

## Supported Integrations

Slack, Gmail, Discord, Google Sheets, Airtable, Notion, Trello, Asana, Zendesk, Stripe, MongoDB, HTTP, Twitter, LinkedIn, Teams, WordPress, and more.

## Production LLM

To use the real Mistral-7B model instead of lightweight server:

```powershell
$env:BASE_MODEL="mistralai/Mistral-7B-Instruct-v0.2"
$env:ADAPTER_PATH="trained_model"
python scripts\serve\local_inference.py
```

Requirements: GPU (6GB+) or CPU (16GB+ RAM)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5000 already in use | `taskkill /f /im python.exe` |
| Connection refused | Ensure both servers running in separate terminals |
| Few nodes generated | Use more specific prompts with multiple app names |
| Module not found | `pip install -r requirements.txt` |

## License

MIT
5. Click "Send"
6. Download the generated workflow JSON file

### Step 4: Import to n8n
1. Go to your n8n instance
2. Click "+" to create a new workflow
3. Click the three dots menu (⋮) → "Import from File"
4. Select the downloaded JSON file
5. Configure your credentials (Gmail, Sheets, etc.)
6. Activate the workflow!

---

## 🔧 Advanced Setup (Local LLM only)

The app uses ONLY a Local LLM endpoint for generation. Set the endpoint in `.env` as `LOCAL_INFER_URL` (defaults to `http://127.0.0.1:8000/generate`).

### Option A: Local LLM (fine-tuned)
1) Build dataset from your `workflows/`:
```powershell
python .\scripts\train\dataset_builder.py
```
2) Train a small LoRA adapter (GPU recommended):
```powershell
$env:BASE_MODEL="mistralai/Mistral-7B-Instruct-v0.3"
python .\scripts\train\qlora_train.py
```
3) Serve the adapter locally:
```powershell
$env:BASE_MODEL="mistralai/Mistral-7B-Instruct-v0.3"
$env:ADAPTER_PATH="models/n8n-lora"
python .\scripts\serve\local_inference.py
```
The app will call http://127.0.0.1:8000/generate. Override with `LOCAL_INFER_URL` in `.env` if needed.

---

## 💡 Example Prompts To Try

1. **"Send an email when a new row is added to Google Sheets"**
   - Creates: Google Sheets Trigger → Gmail

2. **"Create a Trello card when I receive an email"**
   - Creates: Gmail Trigger → Trello

3. **"Post to Slack every day at 9am"**
   - Creates: Schedule Trigger → Slack

4. **"Save webhook data to Airtable"**
   - Creates: Webhook Trigger → Airtable

5. **"Send a Discord message when a new GitHub issue is created"**
   - Creates: GitHub Trigger → Discord

---

## 📖 How It Works (Simple Explanation)

1. **You type** what you want to automate in plain English
2. **The AI analyzes** your request to understand:
   - What should trigger the automation (email received, new row, schedule, etc.)
   - What action should happen (send email, create card, post message, etc.)
3. **The system generates** a valid n8n workflow structure with:
   - Trigger node (starting point)
   - Action node(s) (what happens)
   - Connections between them
4. **You download** the JSON file
5. **You import** it into n8n and configure your accounts

---

## 🛠️ Technical Details (For Developers)

### Architecture
```
User Input (Natural Language)
   ↓
Flask Backend (app.py)
   ↓
Local LLM Inference (HTTP endpoint)
    ↓
n8n JSON Generation
    ↓
Web UI (index.html)
    ↓
Download Workflow JSON
```

### Tech Stack
- **Backend**: Python + Flask
- **Frontend**: HTML + JavaScript (Vanilla - no frameworks)
- **AI**: Local LLM endpoint you run (can be your fine-tuned adapter)

### Project Structure
```
N8N/
├── app.py                      # Flask backend API
├── index.html                  # Chat UI
├── training_examples.json      # Example workflows for AI
├── requirements.txt            # Python dependencies
├── start.bat                   # Easy startup script (Windows)
├── .env.example               # Configuration template
├── workflows/                  # 2000+ example workflows
└── n8n_nodes/                 # Node type references
```

### API Endpoints
- `GET /` - Serves the web interface
- `POST /api/generate` - Generates workflow from prompt
- `GET /api/examples` - Returns example prompts

---

## 🎓 Understanding n8n Workflows

An n8n workflow JSON consists of:

### 1. Nodes
Each node represents a step in your automation:
```json
{
  "name": "Gmail",
  "type": "n8n-nodes-base.gmail",
  "position": [450, 300],
  "parameters": {
    "operation": "send"
  }
}
```

### 2. Connections
Define how data flows between nodes:
```json
{
  "Gmail Trigger": {
    "main": [[{"node": "Slack", "type": "main", "index": 0}]]
  }
}
```

---

## 🔍 Troubleshooting

### "Python is not installed"
- Install Python from python.org
- Make sure to check "Add to PATH"
- Restart your computer after installation

### "Port 5000 is already in use"
- Another application is using port 5000
- Close other applications or edit `app.py` to change the port

### "Workflow doesn't work in n8n"
- Make sure to configure credentials in n8n
- Each service (Gmail, Slack, etc.) needs authentication
- Test each node individually in n8n

### "LLM server not responding"
- Ensure both servers are running: LLM (port 8000) and Frontend (port 5000)
- Run `python run_full_test.py` to diagnose issues
- If the real model (Mistral 7B) fails, use `python simple_test_server.py` instead

---

## 🌟 Extending The System

### Adding New Node Types
Edit `NODE_TYPES` in `app.py`:
```python
"actions": {
    "notion": "n8n-nodes-base.notion",
    "your_service": "n8n-nodes-base.yourService"
}
```

### Adding Training Examples
Edit `training_examples.json` with more workflow patterns.

### Customizing The UI
Edit `index.html` - all styling is in the `<style>` section.

---

## 📝 Cost Breakdown

| Component | Cost | Notes |
|-----------|------|-------|
| Local LLM | **FREE** | Mistral-7B or Qwen on your hardware |
| Python | **FREE** | Open source |
| Flask | **FREE** | Open source |
| Hosting (Local) | **FREE** | Runs on your computer |
| **TOTAL** | **$0.00** | Completely free! No API costs |

---

## 🤝 Support

If you need help:
1. Check the troubleshooting section above
2. Make sure you followed all steps in order
3. Try the example prompts first to ensure it's working
4. Check that Python is installed correctly

---

## 📜 License

This project is free to use for personal and commercial purposes.

---

## 🎉 What's Next?

1. **Test the basic examples** - Make sure everything works
2. **Try your own automations** - Describe what you want to build
3. **Import to n8n** - See your workflows come to life
4. **Experiment** - The more specific your prompt, the better the result!

---

## 💬 Example Conversation

**You**: "Send an email when a new row is added to Google Sheets"

**AI**: ✅ Workflow generated successfully!
- **Nodes**: 2
- Google Sheets Trigger
- Gmail

**You**: *Downloads JSON and imports to n8n*

**Result**: Working automation! 🎉

---

**Happy Automating! 🚀**

If you create something cool with this, feel free to share your workflows!
