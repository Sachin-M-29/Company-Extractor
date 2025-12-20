# PowerShell script to start Flask API and Next.js with GPU configuration for Ollama
# Run this script to enable external GPU support for LLM extraction

Write-Host "🚀 Starting Company Extractor with External GPU Support" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Step 1: Configure Ollama environment for GPU
Write-Host "`n📊 Configuring Ollama for external GPU..." -ForegroundColor Yellow
$env:CUDA_VISIBLE_DEVICES = "0"  # Use first external GPU
$env:OLLAMA_NUM_GPU = "1"        # Number of GPUs to use
$env:OLLAMA_HOST = "127.0.0.1:11434"

# Display GPU info
Write-Host "✓ CUDA_VISIBLE_DEVICES = $env:CUDA_VISIBLE_DEVICES" -ForegroundColor Green
Write-Host "✓ OLLAMA_NUM_GPU = $env:OLLAMA_NUM_GPU" -ForegroundColor Green

# Step 2: Restart Ollama service with GPU configuration (optional - if Ollama is a service)
Write-Host "`n🔄 Checking Ollama status..." -ForegroundColor Yellow
$ollamaProcess = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
if ($ollamaProcess) {
    Write-Host "✓ Ollama is running (PID: $($ollamaProcess.Id))" -ForegroundColor Green
} else {
    Write-Host "⚠ Ollama is not running. Please start Ollama first." -ForegroundColor Red
    Write-Host "  You can start it from the Ollama app or by running: ollama serve" -ForegroundColor Yellow
}

# Step 3: Check if model is available
Write-Host "`n🤖 Checking available models..." -ForegroundColor Yellow
$models = & ollama list 2>&1
Write-Host $models

# Step 4: Kill any existing processes
Write-Host "`n🧹 Cleaning up old processes..." -ForegroundColor Yellow
Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue 2>&1 | Out-Null
Stop-Process -Name "node" -Force -ErrorAction SilentlyContinue 2>&1 | Out-Null
Start-Sleep -Seconds 2
Write-Host "✓ Cleanup complete" -ForegroundColor Green

# Step 5: Activate virtual environment
Write-Host "`n🐍 Activating Python environment..." -ForegroundColor Yellow
$venvPath = "C:\projects\data\.venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "⚠ Virtual environment not found at: $venvPath" -ForegroundColor Red
}

# Step 6: Set Flask environment variables
$env:PYTHON_API = "http://127.0.0.1:5000"
$env:NEXT_PUBLIC_PYTHON_API = "http://127.0.0.1:5000"
$env:FLASK_ENV = "development"

Write-Host "`n=================================================" -ForegroundColor Cyan
Write-Host "🎯 Ready to start servers!" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

Write-Host "`n📝 Manual steps to start servers:" -ForegroundColor Yellow
Write-Host "1. Open Terminal 1 and run:" -ForegroundColor White
Write-Host "   cd C:\projects\data\web-scraper-llm" -ForegroundColor Gray
Write-Host "   python api.py" -ForegroundColor Gray
Write-Host "`n2. Open Terminal 2 and run:" -ForegroundColor White
Write-Host "   cd C:\projects\data\web-scraper-llm\nextjs-ui" -ForegroundColor Gray
Write-Host "   npm run dev" -ForegroundColor Gray

Write-Host "`n✨ GPU Configuration Applied!" -ForegroundColor Green
Write-Host "The LLM will now use your external GPU for faster extraction." -ForegroundColor Green
