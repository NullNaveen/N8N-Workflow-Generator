"""
API Testing Script (Without Browser)
Tests the N8N Workflow Generator API endpoints directly
"""

import requests
import json
import time

API_URL = "http://localhost:5000"

def test_api():
    """Test the API with various prompts"""
    print("\n" + "="*70)
    print("N8N WORKFLOW GENERATOR - API TEST")
    print("="*70 + "\n")
    
    test_cases = [
        {
            "name": "Greeting Test (should be rejected)",
            "prompt": "Hi",
            "should_succeed": False
        },
        {
            "name": "Another Greeting Test (should be rejected)",
            "prompt": "Hello, how are you?",
            "should_succeed": False
        },
        {
            "name": "Off-topic Test (should be rejected)",
            "prompt": "What is your name?",
            "should_succeed": False
        },
        {
            "name": "Valid Workflow Request #1",
            "prompt": "Send email when webhook receives data",
            "should_succeed": True
        },
        {
            "name": "Valid Workflow Request #2",
            "prompt": "Create a workflow that sends Slack notification every day at 9am",
            "should_succeed": True
        },
        {
            "name": "Valid Workflow Request #3",
            "prompt": "Build workflow to save form submissions to Google Sheets",
            "should_succeed": True
        },
        {
            "name": "Valid Workflow Request #4",
            "prompt": "Generate workflow that fetches data from API and stores in database",
            "should_succeed": True
        }
    ]
    
    print(f"[*] Testing API at {API_URL}")
    print(f"[*] Running {len(test_cases)} tests...\n")
    
    results = {"passed": 0, "failed": 0, "errors": 0}
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n[TEST {i}/{len(test_cases)}] {test['name']}")
        print(f"  Prompt: '{test['prompt']}'")
        
        try:
            # Send request
            response = requests.post(
                f"{API_URL}/api/generate",
                json={"prompt": test['prompt']},
                timeout=60
            )
            
            print(f"  Status Code: {response.status_code}")
            
            # Parse response
            data = response.json()
            
            # Check if it matches expected result
            if test['should_succeed']:
                # Should generate workflow
                if response.status_code == 200 and data.get('success'):
                    print(f"  [OK] Test PASSED - Workflow generated successfully")
                    print(f"    - Method: {data.get('method', 'unknown')}")
                    print(f"    - Workflow name: {data.get('workflow', {}).get('name', 'N/A')}")
                    print(f"    - Number of nodes: {len(data.get('workflow', {}).get('nodes', []))}")
                    
                    # Show node types
                    nodes = data.get('workflow', {}).get('nodes', [])
                    if nodes:
                        print(f"    - Node types:")
                        for node in nodes[:5]:  # Show first 5 nodes
                            node_type = node.get('type', 'unknown').split('.')[-1]
                            print(f"      • {node.get('name')} ({node_type})")
                    
                    results["passed"] += 1
                else:
                    print(f"  [FAIL] Test FAILED - Expected workflow but got error")
                    print(f"    Error: {data.get('error', 'Unknown error')}")
                    results["failed"] += 1
            else:
                # Should be rejected (validation error)
                if response.status_code == 400 and data.get('type') == 'validation_error':
                    print(f"  [OK] Test PASSED - Prompt correctly rejected")
                    print(f"    Message: {data.get('error', '')[:100]}...")
                    results["passed"] += 1
                else:
                    print(f"  [FAIL] Test FAILED - Expected rejection but workflow was generated")
                    results["failed"] += 1
            
        except requests.exceptions.Timeout:
            print(f"  [ERROR] Request timed out")
            results["errors"] += 1
        except requests.exceptions.ConnectionError:
            print(f"  [ERROR] Connection failed - is the server running?")
            results["errors"] += 1
        except Exception as e:
            print(f"  [ERROR] Unexpected error: {e}")
            results["errors"] += 1
        
        # Small delay between tests
        time.sleep(1)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Total Tests: {len(test_cases)}")
    print(f"Passed: {results['passed']} ✓")
    print(f"Failed: {results['failed']} ✗")
    print(f"Errors: {results['errors']} ⚠")
    print("="*70 + "\n")
    
    if results['passed'] == len(test_cases):
        print("[OK] All tests passed! System is working correctly.")
        return True
    else:
        print("[WARNING] Some tests failed. Please review the results above.")
        return False

if __name__ == "__main__":
    try:
        success = test_api()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[*] Testing interrupted by user")
        exit(1)
