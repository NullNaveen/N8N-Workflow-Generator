# Quick Start - N8N Workflow Generator (LLM Only)

You have removed Groq completely. The app now uses only a **local LLM server** to generate n8n workflows from natural language prompts.

## 🚀 Fast Start (< 1 minute)

**Start Everything at Once:**
```powershell
python run_full_test.py
```

This will:
1. Start the lightweight test LLM server on port 8000
2. Start the frontend API on port 5000
3. Run 10 complex prompts through the system
4. Show you the results

If you see `RESULTS: 10 PASSED, 0 FAILED` → **Your setup is working!** ✅

---

## 🔧 Manual Setup (if you prefer separate terminals)

### Terminal 1: Start the LLM Server (port 8000)

**For fast, lightweight testing:**
```powershell
python simple_test_server.py
```

**For AI-powered generation (if GPU available):**
```powershell
$env:BASE_MODEL="mistralai/Mistral-7B-Instruct-v0.2"
$env:ADAPTER_PATH="trained_model"
$env:FALLBACK_MODEL="Qwen/Qwen2.5-1.5B-Instruct"
python scripts\serve\local_inference.py
```

### Terminal 2: Start the Frontend (port 5000)

```powershell
python app.py
```

### Open Your Browser:
```
http://localhost:5000
```

---

## 🧪 Test the API

Instead of the browser, you can test directly:

```powershell
python test_complex_prompts.py
```

This runs 10 complex prompts through the system and validates the output.

Expected output:
```
RESULTS: 10 PASSED, 0 FAILED
- Test 1: 6 nodes generated ✓
- Test 2: 7 nodes generated ✓
- Test 3: 6 nodes generated ✓
...
```

---

## 📝 What Happens

**You enter a prompt:**
```
When a customer support email arrives, save to Google Drive, 
create Zendesk ticket, post to Slack, send SMS, and store in Airtable
```

**The app generates n8n JSON with:**
- 5-7 nodes (one per service)
- Proper trigger + action nodes
- Valid connections between nodes
- Default parameters ready to customize

**You import into n8n and:**
1. Add your API credentials
2. Customize parameters as needed
3. Deploy your workflow

---

## ⚙️ Architecture

```
Your Browser
    ↓
Frontend API (port 5000) - app.py
    ↓
LLM Server (port 8000) - simple_test_server.py or scripts/serve/local_inference.py
    ↓
n8n Workflow JSON
```

---

## 🎯 Two LLM Server Options

### Option 1: Lightweight Test Server (Recommended for Now)
- **Command:** `python simple_test_server.py`
- **Speed:** Instant responses
- **Requires:** Nothing (no model downloads)
- **Capability:** Maps prompts to n8n nodes by keywords
- **Node Count:** 4-7 nodes per complex prompt

### Option 2: Real AI Model (Better Quality, Slower)
- **Command:** `python scripts\serve\local_inference.py`
- **Speed:** 30-60 seconds per prompt
- **Requires:** GPU (6GB+) or CPU (16GB+ RAM)
- **Capability:** AI-powered understanding of complex workflows
- **Model:** Mistral-7B + LoRA fine-tuning, auto-fallback to Qwen 1.5B
- **Download:** ~5GB first run (cached after)

---

## ✅ Validation Checklist

- [ ] Both servers start without errors
- [ ] `run_full_test.py` shows 10 PASSED
- [ ] Frontend responds to prompts at http://localhost:5000
- [ ] Generated workflows have 4-7 nodes
- [ ] Method shows "local" (not rule-based or groq)

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 5000 already in use | Kill: `taskkill /f /im python.exe` then restart |
| "Connection refused" | Check both servers are running in separate terminals |
| Only 2-3 nodes generated | Try a more specific prompt with multiple apps mentioned |
| Memory error on real model | Use `simple_test_server.py` instead (no GPU needed) |

---

## 📚 Next Steps

1. **Explore the UI** - http://localhost:5000
2. **Try different prompts** - See how multi-app workflows are generated
3. **Export and import** - Copy the JSON and paste into n8n
4. **Customize** - Edit nodes and connections in n8n as needed

---

## 🔗 Key Files

- `app.py` - Main Flask frontend API (port 5000)
- `simple_test_server.py` - Lightweight test LLM (port 8000)
- `scripts/serve/local_inference.py` - Real AI model (port 8000)
- `test_complex_prompts.py` - Validation test suite
- `run_full_test.py` - Automated setup and test runner

---

**Happy workflow generating! 🎉**

You've successfully removed Groq. Here's how to run the system now:

## Two Servers Need to Run:

### 1. **LLM Backend Server** (port 8000)
Choose ONE of these options:

#### Option A: Mock Server (FAST - for testing)
```powershell
python mock_llm_server.py
```
✓ No downloads required
✓ Instant responses
✓ Works for simple/moderate complexity prompts
✗ Rule-based only (limited to keyword matching)

#### Option B: Real Trained Model (BETTER - but slower first time)
```powershell
$env:BASE_MODEL="mistralai/Mistral-7B-Instruct-v0.2"
$env:ADAPTER_PATH="trained_model"
python scripts/serve/local_inference.py
```
✓ AI-powered - understands complex prompts
✓ Your fine-tuned n8n knowledge
✗ Downloads 7B model (~14GB first time, takes ~5-15 min)
✗ Needs GPU or will be slow on CPU

### 2. **Frontend Server** (port 5000) - In a NEW Terminal Window
```powershell
python app.py
```

## Then Open in Browser:
```
http://localhost:5000
```

---

## Your Current Setup

✅ **Groq is REMOVED** - No API keys needed
✅ **LLM-Only** - Using `LOCAL_INFER_URL` from `.env`
✅ **Two-Server Architecture**:
   - LLM Server (8000) - generates workflows
   - Flask Server (5000) - web UI

---

## Recommendation for You

**For IMMEDIATE testing:**
1. Start Mock Server: `python mock_llm_server.py`
2. In another terminal, start Flask: `python app.py`
3. Go to http://localhost:5000
4. Try your prompts - it will work for most cases

**For BEST RESULTS (when you have time):**
1. Start Real Model: `$env:BASE_MODEL="mistralai/Mistral-7B-Instruct-v0.2"; $env:ADAPTER_PATH="trained_model"; python scripts/serve/local_inference.py`
2. Wait for model to load (can take 5-15 minutes)
3. In another terminal: `python app.py`
4. Go to http://localhost:5000

---

## Next Steps

If you want to test the REAL model but it's slow/not loading:
1. Run: `python diagnose_model.py` (this will show you what's happening)
2. Or just use the mock server for now - it's perfectly fine for testing!
