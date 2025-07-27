# Fix merge conflict and push to GitHub
Write-Host "Fixing merge conflict and pushing to GitHub..." -ForegroundColor Green

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

# Pull remote changes with allow-unrelated-histories
Write-Host "Pulling remote changes..." -ForegroundColor Yellow
git pull origin main --allow-unrelated-histories --no-edit

# Add all files again
Write-Host "Adding files to Git..." -ForegroundColor Yellow
git add .

# Commit the merge
Write-Host "Committing merge..." -ForegroundColor Yellow
git commit -m "Merge remote changes and add complete SafeLayer-Chat SDK implementation" -q

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host "Done! Check https://github.com/S-feLayer/SafeLayer-Chat" -ForegroundColor Green 