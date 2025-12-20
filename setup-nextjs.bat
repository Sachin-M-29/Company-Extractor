@echo off
REM Setup script for Company Information Extractor on Windows

echo 🚀 Setting up Company Information Extractor...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed.
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is required but not installed.
    exit /b 1
)

echo ✓ Python and Node.js found

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install flask flask-cors requests beautifulsoup4 playwright

REM Install Playwright browsers
python -m playwright install

REM Setup Next.js UI
echo 📦 Setting up Next.js UI...
cd nextjs-ui
call npm install
cd ..

echo ✅ Setup complete!
echo.
echo 📋 Next steps:
echo 1. Make sure Ollama is running: ollama serve
echo 2. Start Flask API: python api.py
echo 3. Start Next.js dev: cd nextjs-ui ^&^& npm run dev
echo 4. Open http://localhost:3000 in your browser
