# Fix Git path and push to GitHub
Write-Host "Fixing Git and pushing to GitHub..." -ForegroundColor Green

# Add Git to PATH
$env:PATH += ";C:\Program Files\Git\bin"

# Check Git version
try {
    $gitVersion = git --version
    Write-Host "Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "Git not found. Please install Git first." -ForegroundColor Red
    exit 1
}

# Initialize repository if needed
if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
}

# Add all files
Write-Host "Adding files to Git..." -ForegroundColor Yellow
git add .

# Commit changes
Write-Host "Committing changes..." -ForegroundColor Yellow
git commit -m "Add complete SafeLayer-Chat SDK implementation" -q

# Set remote
Write-Host "Setting up remote..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin https://github.com/S-feLayer/SafeLayer-Chat.git

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main

Write-Host "Done! Check https://github.com/S-feLayer/SafeLayer-Chat" -ForegroundColor Green 