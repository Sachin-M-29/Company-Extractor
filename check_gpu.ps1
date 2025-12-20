# PowerShell script to check GPU availability and Ollama configuration

Write-Host "GPU and Ollama Configuration Check" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# Check NVIDIA GPU
Write-Host "`n1. Checking NVIDIA GPU..." -ForegroundColor Yellow
$nvidiaOutput = nvidia-smi --query-gpu=index,name,memory.total,memory.used --format=csv,noheader 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "GPU detected:" -ForegroundColor Green
    Write-Host $nvidiaOutput -ForegroundColor White
} else {
    Write-Host "NVIDIA GPU not detected" -ForegroundColor Red
}

# Check Ollama
Write-Host "`n2. Checking Ollama..." -ForegroundColor Yellow
$ollamaProcesses = Get-Process -Name "ollama*" -ErrorAction SilentlyContinue
if ($ollamaProcesses) {
    Write-Host "Ollama is running" -ForegroundColor Green
    $ollamaProcesses | ForEach-Object { 
        Write-Host "  - $($_.ProcessName) (PID: $($_.Id))" -ForegroundColor White 
    }
} else {
    Write-Host "Ollama is not running" -ForegroundColor Red
}

# Check Ollama models
Write-Host "`n3. Available Ollama models:" -ForegroundColor Yellow
ollama list

# Check environment variables
Write-Host "`n4. GPU Environment Variables:" -ForegroundColor Yellow
$envVars = @("CUDA_VISIBLE_DEVICES", "OLLAMA_NUM_GPU", "OLLAMA_HOST")
foreach ($var in $envVars) {
    $value = [Environment]::GetEnvironmentVariable($var)
    if ($value) {
        Write-Host "  $var = $value" -ForegroundColor Green
    } else {
        Write-Host "  $var = (not set)" -ForegroundColor Gray
    }
}

Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "Check complete!" -ForegroundColor Cyan
