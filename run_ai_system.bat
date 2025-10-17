@echo off
echo ============================================================
echo 🧠 N8N INTELLIGENT WORKFLOW GENERATOR - LAUNCH SYSTEM
echo ============================================================
echo.
echo This will start the REAL AI system (not rule-based)
echo and run comprehensive testing on 12 complex prompts
echo.
echo Starting intelligent AI server...
echo.

cd /d "c:\Users\Nike\Documents\Programming\Projects\N8N"

start "AI Server" cmd /k "python intelligent_app.py"

echo Waiting for server to initialize...
timeout /t 5 /nobreak > nul

echo.
echo Starting comprehensive testing framework...
echo This will test 12 complex prompts with 7-10 apps each
echo.
python comprehensive_tester.py

pause