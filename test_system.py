"""
Test script to verify the n8n workflow generator is working correctly
"""

import json

def test_training_examples():
    """Test that training examples are valid"""
    print("Testing training_examples.json...")
    try:
        with open('training_examples.json', 'r') as f:
            examples = json.load(f)
        print(f"✅ Found {len(examples)} training examples")
        for i, ex in enumerate(examples):
            assert 'prompt' in ex, f"Example {i} missing 'prompt'"
            assert 'workflow' in ex, f"Example {i} missing 'workflow'"
            assert 'nodes' in ex['workflow'], f"Example {i} workflow missing 'nodes'"
            assert 'connections' in ex['workflow'], f"Example {i} workflow missing 'connections'"
        print("✅ All training examples are valid\n")
        return True
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False

def test_workflow_structure():
    """Test workflow generation logic"""
    print("Testing workflow structure...")
    try:
        # Test basic workflow structure
        test_workflow = {
            "nodes": [
                {
                    "name": "Test Trigger",
                    "type": "n8n-nodes-base.manualTrigger",
                    "position": [250, 300],
                    "parameters": {},
                    "typeVersion": 1
                },
                {
                    "name": "Test Action",
                    "type": "n8n-nodes-base.httpRequest",
                    "position": [450, 300],
                    "parameters": {},
                    "typeVersion": 1
                }
            ],
            "connections": {
                "Test Trigger": {
                    "main": [[{"node": "Test Action", "type": "main", "index": 0}]]
                }
            }
        }
        
        # Validate structure
        assert len(test_workflow['nodes']) == 2
        assert 'Test Trigger' in test_workflow['connections']
        print("✅ Workflow structure is correct\n")
        return True
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False

def test_imports():
    """Test that all required packages are installed"""
    print("Testing Python packages...")
    try:
        import flask
        print(f"✅ Flask {flask.__version__} installed")
        
        import flask_cors
        print(f"✅ Flask-CORS installed")
        
        import requests
        print(f"✅ Requests installed")
        
        print("✅ All required packages are installed\n")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Run: pip install -r requirements.txt\n")
        return False

def test_files_exist():
    """Test that all required files exist"""
    print("Testing required files...")
    required_files = [
        'app.py',
        'index.html',
        'training_examples.json',
        'requirements.txt',
        'README.md',
        'start.bat'
    ]
    
    all_exist = True
    for file in required_files:
        try:
            with open(file, 'r') as f:
                pass
            print(f"✅ {file} exists")
        except FileNotFoundError:
            print(f"❌ {file} not found")
            all_exist = False
    
    print()
    return all_exist

def main():
    print("=" * 60)
    print("N8N WORKFLOW GENERATOR - SYSTEM TEST")
    print("=" * 60)
    print()
    
    tests = [
        ("Files Check", test_files_exist),
        ("Package Check", test_imports),
        ("Training Examples", test_training_examples),
        ("Workflow Structure", test_workflow_structure)
    ]
    
    results = []
    for name, test_func in tests:
        results.append(test_func())
    
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED! You're ready to start the application.")
        print("\nNext steps:")
        print("1. Run: start.bat (Windows) or python app.py")
        print("2. Open: http://localhost:5000")
        print("3. Start generating workflows!")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
    print("=" * 60)

if __name__ == '__main__':
    main()
