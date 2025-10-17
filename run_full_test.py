"""
Multi-server launcher for N8N Workflow Generator.
Starts:
1. Test LLM server on port 8000
2. Frontend API on port 5000
"""

import subprocess
import time
import sys
import os
import signal

processes = []

def signal_handler(sig, frame):
    """Clean shutdown on Ctrl+C."""
    print("\n[*] Shutting down servers...")
    for p in processes:
        try:
            p.terminate()
            p.wait(timeout=3)
        except:
            p.kill()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print("=" * 70)
print("N8N WORKFLOW GENERATOR - SERVER LAUNCHER")
print("=" * 70)

# Start test LLM server (port 8000)
print("[*] Starting Test LLM Server on port 8000...")
p1 = subprocess.Popen(
    [sys.executable, "simple_test_server.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1,
    cwd=os.getcwd()
)
processes.append(p1)
time.sleep(2)

# Start frontend API (port 5000)
print("[*] Starting Frontend API on port 5000...")
env = os.environ.copy()
env["FLASK_ENV"] = "production"
p2 = subprocess.Popen(
    [sys.executable, "app.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1,
    cwd=os.getcwd(),
    env=env
)
processes.append(p2)
time.sleep(2)

print("\n" + "=" * 70)
print("[OK] Both servers running!")
print("    Frontend:   http://127.0.0.1:5000")
print("    LLM Server: http://127.0.0.1:8000")
print("\n[*] Running complex prompt tests in 3 seconds...")
time.sleep(3)

# Run tests
print("\n" + "=" * 70)
result = subprocess.run([sys.executable, "test_complex_prompts.py"], cwd=os.getcwd())
test_exit = result.returncode

# Cleanup
print("\n[*] Test completed. Cleaning up servers...")
signal_handler(None, None)
sys.exit(test_exit)
