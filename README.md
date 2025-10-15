# 🤖 N8N Workflow Generator - AI-Powered Automation Builder

**Convert plain English into ready-to-use n8n workflow JSON files!**

This project uses AI to automatically generate n8n automation workflows from natural language descriptions. Simply describe what you want to automate, and the system creates a downloadable n8n workflow file.

---

## 🎯 What This Project Does

- **Input**: "Send an email when a new row is added to Google Sheets"
- **Output**: A complete n8n workflow JSON file ready to import into n8n

### Features
✅ **Zero Cost** - Uses free Groq API or works without API  
✅ **Chat Interface** - Simple, user-friendly web UI  
✅ **AI-Powered** - Intelligent workflow generation using LLM  
✅ **Instant Download** - Get your workflow JSON immediately  
✅ **No Coding Required** - Just describe what you want in plain English  

---

## 📁 What Are The Files You Have?

### **workflows/** folder
This contains **2000+ real n8n workflow examples**. These are actual automation workflows that show you what's possible with n8n. We use a few of these as reference examples to help the AI understand n8n's structure.

### **n8n_nodes/** folder
These folders represent all the available n8n integrations (Gmail, Slack, Google Sheets, etc.). They're currently empty but show you what services n8n can connect to.

---

## 🚀 Quick Start Guide (For Non-Technical Users)

### Step 1: Install Python
1. Go to https://www.python.org/downloads/
2. Download Python (version 3.8 or newer)
3. **IMPORTANT**: During installation, check the box that says "Add Python to PATH"
4. Complete the installation

### Step 2: Set Up The Project
1. Open the project folder in File Explorer
2. Double-click on **`start.bat`**
3. Wait for the installation to complete (first time only)
4. The server will start automatically

### Step 3: Use The Chat Interface
1. Your browser will show: `http://localhost:5000`
2. If it doesn't open automatically, open your browser and go to that address
3. You'll see a chat interface
4. Type what automation you want (example: "Send an email when a new row is added to Google Sheets")
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

## 🔧 Advanced Setup (Optional - For Better AI Results)

The system works in **two modes**:

### Mode 1: Rule-Based (Default - FREE)
- Works immediately without any setup
- Uses pattern matching to generate workflows
- Good for common automation patterns
- **No API key needed**

### Mode 2: AI-Powered (Recommended - FREE)
- Uses Groq's free AI API for smarter generation
- Better understanding of complex requests
- Still completely free!

**To enable AI mode:**

1. Get a free Groq API key:
   - Go to https://console.groq.com/
   - Sign up (it's free)
   - Go to "API Keys" and create a new key
   - Copy the key

2. Create a `.env` file in the project folder:
   ```
   GROQ_API_KEY=your_key_here
   ```

3. Restart the application (close the terminal and run `start.bat` again)

That's it! The AI mode will automatically activate.

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
AI Processing (Groq API) OR Rule-Based Fallback
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
- **AI**: Groq API (llama-3.1-70b-versatile model)
- **Fallback**: Pattern matching for common scenarios

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

### "AI mode not working"
- Check your Groq API key in `.env`
- Make sure there are no spaces or quotes around the key
- The app will automatically fall back to rule-based mode

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
| Groq API | **FREE** | 14,400 requests/day on free tier |
| Python | **FREE** | Open source |
| Flask | **FREE** | Open source |
| Hosting (Local) | **FREE** | Runs on your computer |
| **TOTAL** | **$0.00** | Completely free! |

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
