# Windows Setup Script for Secure AI MCP
# Run this script as Administrator to resolve permission issues

param(
    [switch]$SkipPythonCheck,
    [switch]$SkipVirtualEnv,
    [switch]$SkipInstall,
    [string]$PythonVersion = "3.12"
)

# Set execution policy to allow script execution
Write-Host "🔧 Setting execution policy..." -ForegroundColor Yellow
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# Function to check if running as administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check if running as administrator
if (-not (Test-Administrator)) {
    Write-Host "⚠️  This script should be run as Administrator for best results" -ForegroundColor Yellow
    Write-Host "   Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        exit 1
    }
}

Write-Host "🚀 Secure AI Windows Setup" -ForegroundColor Green
Write-Host "================================"

# 1. Check Python installation
if (-not $SkipPythonCheck) {
    Write-Host "🐍 Checking Python installation..." -ForegroundColor Yellow
    
    $pythonVersions = @("python", "python3", "py")
    $pythonCmd = $null
    
    foreach ($cmd in $pythonVersions) {
        try {
            $version = & $cmd --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $pythonCmd = $cmd
                Write-Host "✅ Found Python: $version" -ForegroundColor Green
                break
            }
        }
        catch {
            continue
        }
    }
    
    if (-not $pythonCmd) {
        Write-Host "❌ Python not found. Installing Python $PythonVersion..." -ForegroundColor Red
        
        # Download and install Python using winget
        try {
            winget install Python.Python.$PythonVersion
            Write-Host "✅ Python $PythonVersion installed successfully" -ForegroundColor Green
            $pythonCmd = "python"
        }
        catch {
            Write-Host "❌ Failed to install Python via winget. Please install manually from python.org" -ForegroundColor Red
            exit 1
        }
    }
    
    # Verify Python version
    $version = & $pythonCmd --version 2>&1
    Write-Host "Using Python: $version" -ForegroundColor Green
}

# 2. Create virtual environment
if (-not $SkipVirtualEnv) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    
    $venvPath = "pdfmcp"
    if (Test-Path $venvPath) {
        $overwrite = Read-Host "Virtual environment 'pdfmcp' already exists. Overwrite? (y/N)"
        if ($overwrite -eq "y" -or $overwrite -eq "Y") {
            Remove-Item -Recurse -Force $venvPath
        } else {
            Write-Host "Using existing virtual environment" -ForegroundColor Yellow
        }
    }
    
    if (-not (Test-Path $venvPath)) {
        & $pythonCmd -m venv $venvPath
        Write-Host "✅ Virtual environment created" -ForegroundColor Green
    }
    
    # Activate virtual environment
    $activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
    if (Test-Path $activateScript) {
        & $activateScript
        Write-Host "✅ Virtual environment activated" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
        exit 1
    }
}

# 3. Install Secure AI
if (-not $SkipInstall) {
    Write-Host "📦 Installing Secure AI..." -ForegroundColor Yellow
    
    # Upgrade pip first
    & python -m pip install --upgrade pip
    
    # Install Secure AI
    try {
        & python -m pip install git+https://github.com/postralai/secureai@main
        Write-Host "✅ Secure AI installed successfully" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed to install Secure AI: $_" -ForegroundColor Red
        exit 1
    }
    
    # Configure Claude
    Write-Host "⚙️  Configuring Claude..." -ForegroundColor Yellow
    try {
        & python -m secureai.configure_claude
        Write-Host "✅ Claude configuration completed" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️  Claude configuration failed: $_" -ForegroundColor Yellow
        Write-Host "   You may need to configure manually" -ForegroundColor Yellow
    }
}

# 4. Set up environment variables
Write-Host "🔧 Setting up environment variables..." -ForegroundColor Yellow

# Create .env file if it doesn't exist
$envFile = ".env"
if (-not (Test-Path $envFile)) {
    $envContent = @"
# Secure AI Environment Variables
# Add your Tinfoil API key here
TINFOIL_API_KEY=your_api_key_here

# Optional: Set custom paths
# SECUREAI_CACHE_DIR=./cache
# SECUREAI_LOG_LEVEL=INFO
"@
    $envContent | Out-File -FilePath $envFile -Encoding UTF8
    
    Write-Host "✅ Created .env file" -ForegroundColor Green
    Write-Host "   Please edit .env file and add your Tinfoil API key" -ForegroundColor Yellow
}

# 5. Create test directory with proper permissions
$testDir = "test_files"
if (-not (Test-Path $testDir)) {
    New-Item -ItemType Directory -Path $testDir | Out-Null
    Write-Host "✅ Created test directory: $testDir" -ForegroundColor Green
}

# 6. Set file permissions for Windows
Write-Host "🔐 Setting file permissions..." -ForegroundColor Yellow

# Grant full control to current user on project directory
$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$projectPath = Get-Location

try {
    $acl = Get-Acl $projectPath
    $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule($currentUser, "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")
    $acl.SetAccessRule($accessRule)
    Set-Acl $projectPath $acl
    Write-Host "✅ Set permissions for current user" -ForegroundColor Green
}
catch {
    Write-Host "⚠️  Could not set permissions: $_" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file and add your Tinfoil API key" -ForegroundColor White
Write-Host "2. Activate virtual environment: .\pdfmcp\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "3. Run tests: python src\scripts\test_universal_redaction.py" -ForegroundColor White
Write-Host "4. Try multilingual demo: python src\scripts\llama_multilingual_demo.py" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Troubleshooting:" -ForegroundColor Cyan
Write-Host "- If you encounter permission errors, run PowerShell as Administrator" -ForegroundColor White
Write-Host "- Check docs\windows_troubleshooting.md for common issues" -ForegroundColor White
Write-Host "- Ensure your antivirus isn't blocking Python or pip" -ForegroundColor White 