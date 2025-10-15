"""
Visual ASCII Architecture Diagram
Run this file to see a visual representation of the system
"""

def print_architecture():
    print("=" * 80)
    print(" N8N WORKFLOW GENERATOR - SYSTEM ARCHITECTURE")
    print("=" * 80)
    print()
    
    print("""
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                           USER INTERFACE                                 │
    │                                                                          │
    │  ┌──────────────────────────────────────────────────────────────────┐  │
    │  │                        index.html                                 │  │
    │  │  ┌────────────────────────────────────────────────────────────┐  │  │
    │  │  │  🤖 N8N Workflow Generator                                 │  │  │
    │  │  │  ─────────────────────────────────────                     │  │  │
    │  │  │  Try: 📧 Google Sheets → Email                            │  │  │
    │  │  │  ─────────────────────────────────────                     │  │  │
    │  │  │                                                             │  │  │
    │  │  │  👤 User: Send email when new row in Sheets               │  │  │
    │  │  │                                                             │  │  │
    │  │  │  🤖 Bot: ✅ Workflow generated!                            │  │  │
    │  │  │         📥 Download Workflow JSON                          │  │  │
    │  │  │  ─────────────────────────────────────                     │  │  │
    │  │  │  [Type your automation...]                    [Send]       │  │  │
    │  │  └────────────────────────────────────────────────────────────┘  │  │
    │  └──────────────────────────────────────────────────────────────────┘  │
    └─────────────────────────────────┬───────────────────────────────────────┘
                                      │
                                      │ HTTP Request
                                      │ POST /api/generate
                                      │ {"prompt": "..."}
                                      ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                           BACKEND SERVER                                 │
    │                                                                          │
    │  ┌──────────────────────────────────────────────────────────────────┐  │
    │  │                         app.py (Flask)                            │  │
    │  │                                                                   │  │
    │  │  ┌─────────────────────────────────────────────────────────┐    │  │
    │  │  │  1. Receive Prompt                                       │    │  │
    │  │  │     "Send email when new row in Sheets"                  │    │  │
    │  │  └─────────────────────────┬────────────────────────────────┘    │  │
    │  │                            │                                      │  │
    │  │                            ▼                                      │  │
    │  │  ┌─────────────────────────────────────────────────────────┐    │  │
    │  │  │  2. Check API Configuration                              │    │  │
    │  │  │     Is GROQ_API_KEY set?                                 │    │  │
    │  │  └─────────────────────────┬────────────────────────────────┘    │  │
    │  │                            │                                      │  │
    │  │                ┌───────────┴───────────┐                         │  │
    │  │                │                       │                         │  │
    │  │                ▼                       ▼                         │  │
    │  │  ┌──────────────────────┐  ┌──────────────────────┐             │  │
    │  │  │   AI MODE (Groq)     │  │   FALLBACK MODE      │             │  │
    │  │  │                      │  │   (Pattern Match)    │             │  │
    │  │  │  • System prompt     │  │  • Detect keywords   │             │  │
    │  │  │  • Training examples │  │  • Match triggers    │             │  │
    │  │  │  • LLM processing    │  │  • Match actions     │             │  │
    │  │  │  • JSON parsing      │  │  • Build template    │             │  │
    │  │  └──────────┬───────────┘  └──────────┬───────────┘             │  │
    │  │             │                          │                         │  │
    │  │             └────────────┬─────────────┘                         │  │
    │  │                          ▼                                       │  │
    │  │  ┌─────────────────────────────────────────────────────────┐    │  │
    │  │  │  3. Generate n8n JSON                                    │    │  │
    │  │  │     {                                                    │    │  │
    │  │  │       "nodes": [...],                                    │    │  │
    │  │  │       "connections": {...}                               │    │  │
    │  │  │     }                                                    │    │  │
    │  │  └─────────────────────────┬────────────────────────────────┘    │  │
    │  │                            │                                      │  │
    │  │                            ▼                                      │  │
    │  │  ┌─────────────────────────────────────────────────────────┐    │  │
    │  │  │  4. Add Metadata                                         │    │  │
    │  │  │     • workflow name                                      │    │  │
    │  │  │     • active: false                                      │    │  │
    │  │  │     • settings: {}                                       │    │  │
    │  │  └─────────────────────────┬────────────────────────────────┘    │  │
    │  └────────────────────────────┼──────────────────────────────────┘  │
    └─────────────────────────────────┼───────────────────────────────────┘
                                      │
                                      │ HTTP Response
                                      │ {"success": true, "workflow": {...}}
                                      ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                         USER DOWNLOADS                                   │
    │                                                                          │
    │  ┌──────────────────────────────────────────────────────────────────┐  │
    │  │  workflow.json                                                    │  │
    │  │  {                                                                │  │
    │  │    "nodes": [                                                     │  │
    │  │      {"name": "Google Sheets Trigger", ...},                      │  │
    │  │      {"name": "Gmail", ...}                                       │  │
    │  │    ],                                                             │  │
    │  │    "connections": {...}                                           │  │
    │  │  }                                                                │  │
    │  └──────────────────────────────────────────────────────────────────┘  │
    └─────────────────────────────────┬───────────────────────────────────────┘
                                      │
                                      │ User imports to n8n
                                      ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                           N8N PLATFORM                                   │
    │                                                                          │
    │  ┌──────────────────────────────────────────────────────────────────┐  │
    │  │  [Google Sheets Trigger] ──────> [Gmail]                         │  │
    │  │                                                                   │  │
    │  │  User configures credentials and activates                       │  │
    │  └──────────────────────────────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────────────────────────────┘
    """)

def print_file_structure():
    print()
    print("=" * 80)
    print(" FILE STRUCTURE")
    print("=" * 80)
    print()
    
    print("""
    N8N/
    │
    ├── 📱 FRONTEND
    │   └── index.html                    # Chat interface (HTML/CSS/JS)
    │
    ├── 🧠 BACKEND
    │   ├── app.py                        # Flask server + AI logic
    │   └── training_examples.json        # Example workflows for AI
    │
    ├── 🔧 CONFIGURATION
    │   ├── requirements.txt              # Python dependencies
    │   ├── .env.example                  # API key template
    │   └── .gitignore                    # Git ignore rules
    │
    ├── 🚀 SCRIPTS
    │   ├── start.bat                     # Windows startup script
    │   ├── test_system.py                # System verification
    │   └── architecture.py               # This file!
    │
    ├── 📚 DOCUMENTATION
    │   ├── README.md                     # Technical documentation
    │   ├── SETUP_GUIDE.md               # Non-technical guide
    │   ├── QUICKSTART.md                # Quick reference
    │   └── PROJECT_SUMMARY.md           # Overview
    │
    └── 📦 EXISTING DATA
        ├── workflows/                    # 2000+ example workflows
        └── n8n_nodes/                   # Node type directories
    """)

def print_data_flow():
    print()
    print("=" * 80)
    print(" DATA FLOW")
    print("=" * 80)
    print()
    
    print("""
    Step 1: USER INPUT
    ┌───────────────────────────────────────────────────────────┐
    │ "Send an email when a new row is added to Google Sheets" │
    └───────────────────────────┬───────────────────────────────┘
                                │
                                ▼
    Step 2: FRONTEND PROCESSING
    ┌───────────────────────────────────────────────────────────┐
    │ • Capture input                                           │
    │ • Show typing indicator                                   │
    │ • Send POST request to /api/generate                      │
    └───────────────────────────┬───────────────────────────────┘
                                │
                                ▼
    Step 3: BACKEND ANALYSIS
    ┌───────────────────────────────────────────────────────────┐
    │ Analyze prompt:                                           │
    │ • Trigger: "new row" → Google Sheets Trigger             │
    │ • Action: "send email" → Gmail                           │
    │ • Pattern: trigger + action                              │
    └───────────────────────────┬───────────────────────────────┘
                                │
                                ▼
    Step 4: AI GENERATION (if API key exists)
    ┌───────────────────────────────────────────────────────────┐
    │ Send to Groq API:                                         │
    │ • System prompt (n8n structure guide)                     │
    │ • Training examples (3 workflows)                         │
    │ • User prompt                                             │
    │ • Get JSON response                                       │
    └───────────────────────────┬───────────────────────────────┘
                                │
                                ▼
    Step 5: JSON CONSTRUCTION
    ┌───────────────────────────────────────────────────────────┐
    │ Build workflow object:                                    │
    │ {                                                         │
    │   "nodes": [                                              │
    │     {                                                     │
    │       "name": "Google Sheets Trigger",                    │
    │       "type": "n8n-nodes-base.googleSheetsTrigger",       │
    │       "position": [250, 300],                             │
    │       "parameters": {"event": "rowAdded"}                 │
    │     },                                                    │
    │     {                                                     │
    │       "name": "Gmail",                                    │
    │       "type": "n8n-nodes-base.gmail",                     │
    │       "position": [450, 300],                             │
    │       "parameters": {"operation": "send"}                 │
    │     }                                                     │
    │   ],                                                      │
    │   "connections": {                                        │
    │     "Google Sheets Trigger": {                            │
    │       "main": [[                                          │
    │         {"node": "Gmail", "type": "main", "index": 0}     │
    │       ]]                                                  │
    │     }                                                     │
    │   }                                                       │
    │ }                                                         │
    └───────────────────────────┬───────────────────────────────┘
                                │
                                ▼
    Step 6: RESPONSE TO FRONTEND
    ┌───────────────────────────────────────────────────────────┐
    │ {                                                         │
    │   "success": true,                                        │
    │   "workflow": {...},                                      │
    │   "prompt": "...",                                        │
    │   "method": "groq"                                        │
    │ }                                                         │
    └───────────────────────────┬───────────────────────────────┘
                                │
                                ▼
    Step 7: UI UPDATE
    ┌───────────────────────────────────────────────────────────┐
    │ • Remove typing indicator                                 │
    │ • Show workflow preview                                   │
    │ • Display download button                                 │
    │ • Enable input field                                      │
    └───────────────────────────┬───────────────────────────────┘
                                │
                                ▼
    Step 8: DOWNLOAD
    ┌───────────────────────────────────────────────────────────┐
    │ • Create JSON blob                                        │
    │ • Trigger browser download                                │
    │ • Save as: n8n_workflow_[timestamp].json                  │
    └───────────────────────────────────────────────────────────┘
    """)

def print_ai_vs_fallback():
    print()
    print("=" * 80)
    print(" AI MODE vs FALLBACK MODE")
    print("=" * 80)
    print()
    
    print("""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                            AI MODE                                   │
    │                      (With Groq API Key)                             │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                      │
    │  Advantages:                                                         │
    │  ✅ Understands complex prompts                                     │
    │  ✅ Better context understanding                                    │
    │  ✅ Can handle variations in wording                                │
    │  ✅ Learns from examples                                            │
    │  ✅ More accurate node selection                                    │
    │                                                                      │
    │  How it works:                                                       │
    │  1. System prompt teaches n8n structure                             │
    │  2. Few-shot learning with 3 examples                               │
    │  3. LLM (Llama 3.1 70B) processes request                           │
    │  4. Generates JSON directly                                         │
    │                                                                      │
    │  Example prompt it handles well:                                    │
    │  "Whenever someone fills out my contact form, I want to             │
    │   automatically create a new card in my Trello board and            │
    │   send me a Slack notification"                                     │
    │                                                                      │
    │  Cost: FREE (14,400 requests/day)                                   │
    │                                                                      │
    └─────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │                         FALLBACK MODE                                │
    │                  (No API Key Required)                               │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                      │
    │  Advantages:                                                         │
    │  ✅ Works immediately                                               │
    │  ✅ No configuration needed                                         │
    │  ✅ No internet dependency                                          │
    │  ✅ Fast response time                                              │
    │  ✅ Predictable results                                             │
    │                                                                      │
    │  How it works:                                                       │
    │  1. Scan prompt for keywords                                        │
    │  2. Match trigger patterns (schedule, webhook, email)               │
    │  3. Match action patterns (send, create, save)                      │
    │  4. Apply predefined template                                       │
    │                                                                      │
    │  Example prompt it handles well:                                    │
    │  "Send an email when a new row is added to Google Sheets"           │
    │                                                                      │
    │  Cost: FREE (always)                                                │
    │                                                                      │
    └─────────────────────────────────────────────────────────────────────┘

    RECOMMENDATION:
    ╔═══════════════════════════════════════════════════════════════════╗
    ║  Start with Fallback Mode (no setup required)                     ║
    ║  Try a few examples                                               ║
    ║  If you need more complex workflows → Add Groq API key            ║
    ║  Both modes produce valid n8n workflows!                          ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)

def main():
    print_architecture()
    print_file_structure()
    print_data_flow()
    print_ai_vs_fallback()
    
    print()
    print("=" * 80)
    print(" READY TO START!")
    print("=" * 80)
    print()
    print("Run: start.bat")
    print("Or:  python app.py")
    print()
    print("Then open: http://localhost:5000")
    print()
    print("=" * 80)

if __name__ == '__main__':
    main()
