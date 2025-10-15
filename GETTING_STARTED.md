# 🎯 GETTING STARTED - YOUR 5-MINUTE GUIDE

## 🎬 What You're About To Do

In the next 5 minutes, you'll:
1. ✅ Install Python (if not already installed)
2. ✅ Start the application
3. ✅ Generate your first workflow
4. ✅ Download it and see it work!

Let's go! 🚀

---

## 📍 START HERE

### ⚡ Super Quick Start (3 Steps)

```
STEP 1: Install Python
└─> Go to: python.org/downloads
└─> Download and install
└─> ✓ Check "Add Python to PATH"

STEP 2: Run Application  
└─> Double-click: start.bat
└─> Wait for browser to open

STEP 3: Create Workflow
└─> Type: "Send email when new Google Sheets row"
└─> Click: Send
└─> Click: Download
```

**Done!** 🎉 You now have an n8n workflow file!

---

## 📸 Visual Walkthrough

### 1️⃣ What You'll See When You Start

```
╔════════════════════════════════════════════════╗
║  🤖 N8N Workflow Generator                     ║
║  Describe your automation in plain English     ║
╠════════════════════════════════════════════════╣
║                                                ║
║  Try these examples:                           ║
║  [📧 Google Sheets → Email]                    ║
║  [📮 Email → Trello]                           ║
║  [⏰ Daily Slack Message]                      ║
║                                                ║
║  ┌──────────────────────────────────────────┐ ║
║  │ 🤖 Hi! I'm your n8n assistant.           │ ║
║  │    Tell me what you want to automate...  │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
║  ┌────────────────────────────┐  [Send]       ║
║  │ Type here...               │               ║
║  └────────────────────────────┘               ║
╚════════════════════════════════════════════════╝
```

### 2️⃣ After You Type and Send

```
╔════════════════════════════════════════════════╗
║  🤖 N8N Workflow Generator                     ║
╠════════════════════════════════════════════════╣
║                                                ║
║  ┌──────────────────────────────────────────┐ ║
║  │ 👤 Send an email when a new row is       │ ║
║  │    added to Google Sheets                │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
║  ┌──────────────────────────────────────────┐ ║
║  │ 🤖 • • •  (thinking...)                  │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
╚════════════════════════════════════════════════╝
```

### 3️⃣ Your Generated Workflow

```
╔════════════════════════════════════════════════╗
║  🤖 N8N Workflow Generator                     ║
╠════════════════════════════════════════════════╣
║                                                ║
║  ┌──────────────────────────────────────────┐ ║
║  │ 👤 Send an email when a new row is       │ ║
║  │    added to Google Sheets                │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
║  ┌──────────────────────────────────────────┐ ║
║  │ 🤖 ✅ Workflow generated successfully!   │ ║
║  │                                          │ ║
║  │    Workflow Name: Send an email when...  │ ║
║  │    Nodes: 2                              │ ║
║  │    Method: 🚀 AI-Powered                 │ ║
║  │                                          │ ║
║  │    Nodes:                                │ ║
║  │    • Google Sheets Trigger               │ ║
║  │    • Gmail                               │ ║
║  │                                          │ ║
║  │    [📥 Download Workflow JSON]           │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
╚════════════════════════════════════════════════╝
```

---

## 🎯 Try These Example Prompts

### ✉️ Email Automations
```
✓ "Send an email when a new row is added to Google Sheets"
✓ "Email me when I receive a form submission"
✓ "Send a daily email digest at 9am"
```

### 📋 Task Management
```
✓ "Create a Trello card when I receive an email"
✓ "Add a task to Notion when someone mentions me in Slack"
✓ "Create a GitHub issue from a webhook"
```

### 💬 Messaging
```
✓ "Post to Slack when a new row is added"
✓ "Send Discord notification every day at 10am"
✓ "Send Slack message when GitHub issue created"
```

### 💾 Data Storage
```
✓ "Save webhook data to Airtable"
✓ "Add rows to Google Sheets from form submissions"
✓ "Store email attachments in Google Drive"
```

---

## 🎓 Understanding Your Results

### What Gets Generated

When you type: **"Send email when new Google Sheets row"**

You get a JSON file with:

```
📄 workflow.json
├─ 🔵 Node 1: Google Sheets Trigger
│  ├─ Watches for new rows
│  ├─ Position: [250, 300]
│  └─ Type: googleSheetsTrigger
│
├─ 🔵 Node 2: Gmail
│  ├─ Sends email
│  ├─ Position: [450, 300]
│  └─ Type: gmail
│
└─ 🔗 Connection: Sheets Trigger → Gmail
```

---

## 📥 What To Do With The Downloaded File

### Step-by-Step Import to n8n

```
1. Open n8n (cloud or self-hosted)
   └─> Go to: https://n8n.io or your instance

2. Create new workflow
   └─> Click the "+" button

3. Import your file
   └─> Click menu (⋮) → "Import from File"
   └─> Select your downloaded JSON

4. Configure credentials
   └─> Click each node
   └─> Add your Gmail/Sheets account
   └─> Authorize access

5. Test it
   └─> Click "Execute Workflow"
   └─> Check if it works

6. Activate it
   └─> Toggle "Active" switch ON
   └─> Your automation is live! 🎉
```

---

## 🎨 Customization Ideas

### Make It Your Own

Once you have the basic workflow:

```
✏️ Change the email subject
   └─> Click Gmail node
   └─> Edit "Subject" field

✏️ Add conditions
   └─> Add an "IF" node
   └─> Only send email if conditions match

✏️ Filter data
   └─> Add a "Filter" node
   └─> Process only certain rows

✏️ Format data
   └─> Add a "Set" node
   └─> Transform the data structure
```

---

## 🚀 Advanced: Enable AI Mode

Want even better results? Enable AI mode!

### Get Groq API Key (Free)

```
STEP 1: Sign Up
└─> Go to: https://console.groq.com
└─> Create free account
└─> Verify email

STEP 2: Get API Key
└─> Go to "API Keys" section
└─> Click "Create API Key"
└─> Copy the key (starts with "gsk_")

STEP 3: Add to App
└─> Open Notepad
└─> Type: GROQ_API_KEY=your_key_here
└─> Save as: .env
└─> Location: Same folder as app.py

STEP 4: Restart
└─> Close the app
└─> Run start.bat again
└─> You'll see: "Groq API configured: Yes"
```

### What Changes?

```
❌ Before (Fallback):
   • Pattern matching
   • Simple prompts work best
   
✅ After (AI Mode):
   • AI understands context
   • Complex prompts work
   • Better accuracy
   • Still 100% FREE!
```

---

## 🎯 Quick Troubleshooting

### Problem: "Python not found"
```
Solution:
└─> Install Python from python.org
└─> ✓ Check "Add Python to PATH"
└─> Restart computer
```

### Problem: "Port 5000 in use"
```
Solution:
└─> Close other apps
└─> Or change port in app.py to 5001
```

### Problem: "Workflow doesn't work in n8n"
```
Solution:
└─> This is normal!
└─> Add your credentials in n8n
└─> Configure each node's settings
└─> Test each node individually
```

### Problem: "Nothing happens when I click Send"
```
Solution:
└─> Check browser console (F12)
└─> Make sure backend is running
└─> Look for errors in terminal window
```

---

## 📊 What Happens Behind The Scenes

### The Magic Explained Simply

```
Your Prompt: "Send email when new Google Sheets row"

Step 1: Word Analysis
└─> "new Google Sheets row" = Trigger
└─> "send email" = Action

Step 2: Node Selection
└─> Trigger Type: googleSheetsTrigger
└─> Action Type: gmail

Step 3: JSON Creation
└─> Build nodes array
└─> Build connections object
└─> Add metadata

Step 4: Validation
└─> Check JSON structure
└─> Verify node types exist
└─> Ensure connections valid

Step 5: Response
└─> Send to frontend
└─> Display preview
└─> Enable download
```

---

## 🎉 You're Ready!

### Final Checklist

```
✓ Python installed
✓ Application running
✓ Browser showing chat interface
✓ Can type and send messages
✓ Workflows generate successfully
✓ Can download JSON files
✓ (Optional) Groq API configured
```

### What's Next?

```
1. Generate 3-5 different workflows
2. Import them to n8n
3. Configure and test each one
4. Activate your favorites
5. Automate your life! 🚀
```

---

## 💡 Pro Tips

### Get Better Results

```
✅ Be specific
   "Send email to admin@example.com when new row in Sheet1"
   
✅ Include details
   "Post to #general Slack channel every day at 9am with a greeting"
   
✅ Use clear triggers
   "When I receive an email"
   "Every Monday at 10am"
   "When webhook receives data"
   
✅ Specify exact services
   "Gmail" not just "email"
   "Google Sheets" not just "spreadsheet"
```

---

## 🎯 Example Session

### A Complete Example

```
1. You type:
   "Send a Slack message when a GitHub issue is created"

2. App analyzes:
   • Trigger: GitHub issue created
   • Action: Slack message

3. App generates:
   {
     "nodes": [
       GitHub Trigger,
       Slack
     ],
     "connections": { ... }
   }

4. You download:
   n8n_workflow_1729000000.json

5. You import to n8n:
   • Connect GitHub account
   • Connect Slack account
   • Choose Slack channel
   • Test and activate

6. Result:
   ✅ Automation works!
   ✅ Gets notified on Slack for every new issue
```

---

## 📚 Resources

### Learn More

```
📖 Full Documentation: README.md
📖 Detailed Setup Guide: SETUP_GUIDE.md
📖 Project Overview: PROJECT_SUMMARY.md
📖 Quick Commands: QUICKSTART.md
📖 System Architecture: architecture.py

🌐 External Resources:
   • n8n Docs: https://docs.n8n.io
   • Groq API: https://console.groq.com/docs
   • Python Docs: https://docs.python.org
```

---

## 🎊 Success Stories

### What You Can Build

```
✉️ Email Management
   • Auto-reply to certain emails
   • Save attachments to cloud
   • Filter and categorize

📊 Data Automation
   • Sync between platforms
   • Daily reports
   • Data backup

📱 Notifications
   • Custom alerts
   • Status updates
   • Daily summaries

🔄 Integration
   • Connect your favorite tools
   • Automate repetitive tasks
   • Build custom workflows
```

---

## 🎯 Your First Goal

### Today's Mission

```
✓ Generate 1 workflow
✓ Download the JSON
✓ Look at the structure
✓ Understand what it does

Tomorrow:
✓ Import to n8n
✓ Configure credentials
✓ Test and activate
✓ Celebrate! 🎉
```

---

## 🚀 Ready? Let's Go!

### The Command

```
Windows:
└─> Double-click: start.bat

Mac/Linux:
└─> Terminal: python3 app.py

Browser:
└─> http://localhost:5000
```

### Your First Prompt

```
"Send an email when a new row is added to Google Sheets"
```

### Then

```
📥 Download
📤 Import to n8n
⚙️ Configure
▶️ Activate
🎉 Celebrate!
```

---

**NOW GO BUILD SOMETHING AWESOME! 🚀**

---

*Last Updated: October 2025*
*Version: 1.0*
*Status: Ready to Rock! ✅*
