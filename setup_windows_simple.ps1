# Simple Windows Setup Script for Secure AI MCP
Write-Host "🚀 Secure AI Windows Setup" -ForegroundColor Green
Write-Host "================================"

# Set execution policy
Write-Host "🔧 Setting execution policy..." -ForegroundColor Yellow
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# Check Python
Write-Host "🐍 Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.10+ from python.org" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "pdfmcp") {
    Write-Host "Virtual environment already exists" -ForegroundColor Yellow
} else {
    python -m venv pdfmcp
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
$activateScript = "pdfmcp\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Install Secure AI
Write-Host "📦 Installing Secure AI..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install git+https://github.com/postralai/secureai@main
Write-Host "✅ Secure AI installed" -ForegroundColor Green

# Create .env file
Write-Host "🔧 Creating .env file..." -ForegroundColor Yellow
$envContent = "# Secure AI Environment Variables`n# Add your Tinfoil API key here`nTINFOIL_API_KEY=your_api_key_here`n`n# Optional: Set custom paths`n# SECUREAI_CACHE_DIR=./cache`n# SECUREAI_LOG_LEVEL=INFO"
$envContent | Out-File -FilePath ".env" -Encoding UTF8
Write-Host "✅ Created .env file" -ForegroundColor Green

# Create test directory
Write-Host "📁 Creating test directory..." -ForegroundColor Yellow
if (-not (Test-Path "test_files")) {
    New-Item -ItemType Directory -Path "test_files" | Out-Null
    Write-Host "✅ Created test directory" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file and add your Tinfoil API key" -ForegroundColor White
Write-Host "2. Activate virtual environment: .\pdfmcp\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "3. Run tests: python src/scripts/test_universal_redaction.py" -ForegroundColor White
Write-Host "4. Try multilingual demo: python src/scripts/llama_multilingual_demo.py" -ForegroundColor White 