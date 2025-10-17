import requests
import json

# Test the intelligent AI system
url = "http://localhost:6000/api/generate"
test_prompt = "When I receive a customer support email, create Zendesk ticket, send auto-response via Gmail, and notify team on Slack"

print("🧪 Testing Intelligent AI Workflow Generator")
print("="*60)
print(f"Prompt: {test_prompt}")
print("-"*60)

try:
    response = requests.post(url, json={"prompt": test_prompt}, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        workflow = data.get('workflow', {})
        
        print("✅ SUCCESS!")
        print(f"Generated {len(workflow.get('nodes', []))} nodes:")
        
        for i, node in enumerate(workflow.get('nodes', []), 1):
            print(f"  {i}. {node.get('name')} ({node.get('type')})")
        
        print(f"\nConnections: {len(workflow.get('connections', {}))}")
        print(f"Method: {data.get('method', 'unknown')}")
        
        # Save the workflow
        with open('test_workflow.json', 'w') as f:
            json.dump(workflow, f, indent=2)
        print(f"\n💾 Workflow saved to: test_workflow.json")
        
    else:
        print(f"❌ FAILED - HTTP {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ ERROR: {e}")

print("\n" + "="*60)