@echo off
REM Setup script for Web Scraper + LLM System
REM Run this after installing Ollama

cls
echo ============================================================================
echo    WEB SCRAPER + LLM INFORMATION EXTRACTION SYSTEM
echo ============================================================================
echo.

REM Check Python
echo [1/4] Checking Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('python --version') do set PYVER=%%i
    echo ✅ Python found: %PYVER%
) else (
    echo ❌ Python not found
    pause
    exit /b 1
)

REM Check virtual environment
echo [2/4] Checking virtual environment...
if exist venv\Scripts\activate.bat (
    echo ✅ Virtual environment exists
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment created
)

REM Check Ollama
echo [3/4] Checking Ollama...
ollama --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ollama found
    
    REM Check if model exists
    ollama list | findstr "mistral" >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Mistral model already installed
    ) else (
        echo ⚠️  Mistral model not found
        echo Pulling model (this takes 5-10 minutes)...
        ollama pull mistral:7b-instruct-q4_0
    )
) else (
    echo ❌ Ollama not found
    echo Please install from: https://ollama.ai
    echo Then restart this script
    pause
    exit /b 1
)

REM Check dependencies
echo [4/4] Checking Python dependencies...
pip list | findstr "streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -q requests beautifulsoup4 playwright streamlit ollama
    echo ✅ Dependencies installed
) else (
    echo ✅ Dependencies found
)

echo.
echo ============================================================================
echo    SETUP COMPLETE!
echo ============================================================================
echo.
echo Next steps:
echo.
echo [Terminal 1] Start Ollama server:
echo   ollama serve
echo.
echo [Terminal 2] Start the web application:
echo   streamlit run ui/app.py
echo.
echo Then visit: http://localhost:8501
echo.
echo ============================================================================
pause
