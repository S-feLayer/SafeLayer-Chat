# Basic Windows Setup Script for SecureAI MCP
Write-Host "Starting SecureAI Windows Setup..."

# Set execution policy
Write-Host "Setting execution policy..."
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# Check Python
Write-Host "Checking Python..."
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found Python: $pythonVersion"
} catch {
    Write-Host "Python not found. Please install Python 3.10+ from python.org"
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..."
if (Test-Path "pdfmcp") {
    Write-Host "Virtual environment already exists"
} else {
    python -m venv pdfmcp
    Write-Host "Virtual environment created"
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
$activateScript = "pdfmcp\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "Virtual environment activated"
} else {
    Write-Host "Failed to activate virtual environment"
    exit 1
}

# Install SecureAI
Write-Host "Installing SecureAI..."
python -m pip install --upgrade pip
python -m pip install git+https://github.com/postralai/secureai@main
Write-Host "SecureAI installed"

# Create .env file
Write-Host "Creating .env file..."
$envContent = "# SecureAI Environment Variables`nTINFOIL_API_KEY=your_api_key_here"
$envContent | Out-File -FilePath ".env" -Encoding UTF8
Write-Host "Created .env file"

# Create test directory
Write-Host "Creating test directory..."
if (-not (Test-Path "test_files")) {
    New-Item -ItemType Directory -Path "test_files" | Out-Null
    Write-Host "Created test directory"
}

Write-Host ""
Write-Host "Setup completed successfully!"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Edit .env file and add your Tinfoil API key"
Write-Host "2. Activate virtual environment: .\pdfmcp\Scripts\Activate.ps1"
Write-Host "3. Run tests: python src/scripts/test_universal_redaction.py"
Write-Host "4. Try multilingual demo: python src/scripts/llama_multilingual_demo.py" 