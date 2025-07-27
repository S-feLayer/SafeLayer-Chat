#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Push SafeLayer-Chat repository to GitHub
    
.DESCRIPTION
    This script sets up Git and pushes the SafeLayer-Chat repository to GitHub.
    It handles the initial setup, adds all files, and pushes to the target repository.
#>

param(
    [string]$RepositoryUrl = "https://github.com/S-feLayer/SafeLayer-Chat.git",
    [string]$Branch = "main"
)

Write-Host "🚀 SafeLayer-Chat GitHub Push Script" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Check if Git is available
try {
    $gitVersion = git --version
    Write-Host "✅ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "After installation, restart PowerShell and run this script again." -ForegroundColor Yellow
    exit 1
}

# Check if we're in a Git repository
if (Test-Path ".git") {
    Write-Host "✅ Git repository already initialized" -ForegroundColor Green
} else {
    Write-Host "🔄 Initializing Git repository..." -ForegroundColor Yellow
    git init
}

# Check current remote
$currentRemote = git remote get-url origin 2>$null
if ($currentRemote) {
    Write-Host "📡 Current remote: $currentRemote" -ForegroundColor Cyan
    if ($currentRemote -ne $RepositoryUrl) {
        Write-Host "🔄 Updating remote URL..." -ForegroundColor Yellow
        git remote set-url origin $RepositoryUrl
    }
} else {
    Write-Host "🔄 Adding remote origin..." -ForegroundColor Yellow
    git remote add origin $RepositoryUrl
}

# Add all files
Write-Host "📁 Adding all files to Git..." -ForegroundColor Yellow
git add .

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    Write-Host "💾 Committing changes..." -ForegroundColor Yellow
    git commit -m "Add complete SafeLayer-Chat SDK implementation

- Production-ready SDK package with clean API
- Comprehensive documentation and tutorials
- Command-line interface
- Type-safe data models with Pydantic
- Error handling and validation
- Build and distribution tools
- Usage examples and best practices"
} else {
    Write-Host "ℹ️  No changes to commit" -ForegroundColor Cyan
}

# Check if branch exists
$currentBranch = git branch --show-current
if ($currentBranch -ne $Branch) {
    Write-Host "🔄 Creating/checking out $Branch branch..." -ForegroundColor Yellow
    git checkout -b $Branch 2>$null
}

# Push to GitHub
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
try {
    git push -u origin $Branch
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "📋 Repository URL: $RepositoryUrl" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Failed to push to GitHub" -ForegroundColor Red
    Write-Host "This might be due to:" -ForegroundColor Yellow
    Write-Host "  - Authentication issues (check your GitHub credentials)" -ForegroundColor Yellow
    Write-Host "  - Repository permissions" -ForegroundColor Yellow
    Write-Host "  - Network connectivity" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Try running: git push -u origin $Branch" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🎉 Setup complete!" -ForegroundColor Green
Write-Host "Your SafeLayer-Chat repository is now available at:" -ForegroundColor Cyan
Write-Host "https://github.com/S-feLayer/SafeLayer-Chat" -ForegroundColor Blue 