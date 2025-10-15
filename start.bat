@echo off
echo ========================================
echo N8N Workflow Generator - Easy Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/4] Installing Python packages...
pip install -r requirements.txt

echo.
echo [2/4] Checking configuration...
if not exist .env (
    echo No .env file found. You can optionally create one for Groq API.
    echo The app will work with rule-based generation without it.
)

echo.
echo [3/4] Starting the server...
echo.
echo ========================================
echo Server will start at: http://localhost:5000
echo Open this URL in your browser
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
