# Privacy Firewall - GitHub Push Script
# This script helps push the cleaned repository to GitHub

Write-Host "Privacy Firewall - GitHub Push Helper" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Check if GitHub CLI is available
$ghAvailable = $null
try {
    $ghAvailable = Get-Command gh -ErrorAction SilentlyContinue
} catch {
    $ghAvailable = $null
}

if ($ghAvailable) {
    Write-Host "GitHub CLI found! Using GitHub CLI to push..." -ForegroundColor Yellow
    
    # Initialize git repository if not already done
    if (-not (Test-Path ".git")) {
        Write-Host "Initializing git repository..." -ForegroundColor Yellow
        git init
    }
    
    # Add all files
    Write-Host "Adding all files to git..." -ForegroundColor Yellow
    git add .
    
    # Commit changes
    Write-Host "Committing changes..." -ForegroundColor Yellow
    git commit -m "Complete repository cleanup and rebranding to Privacy Firewall

- Removed 40+ unnecessary development files
- Renamed all components to avoid copyright issues  
- Updated package structure and naming
- Enhanced .gitignore with comprehensive patterns
- Updated all documentation and examples
- Fixed Docker configuration and deployment scripts"
    
    # Create repository and push
    Write-Host "Creating GitHub repository and pushing..." -ForegroundColor Yellow
    gh repo create Privacy-Firewall --public --source=. --remote=origin --push
    
} else {
    Write-Host "GitHub CLI not found. Manual instructions:" -ForegroundColor Red
    Write-Host ""
    Write-Host "1. Install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "2. Install GitHub CLI from: https://cli.github.com/" -ForegroundColor Yellow
    Write-Host "3. Or manually upload to GitHub:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Manual Upload Steps:" -ForegroundColor Cyan
    Write-Host "1. Go to https://github.com/new" -ForegroundColor White
    Write-Host "2. Create a new repository named 'Privacy-Firewall'" -ForegroundColor White
    Write-Host "3. Upload all files from this directory" -ForegroundColor White
    Write-Host "4. Or use GitHub Desktop: https://desktop.github.com/" -ForegroundColor White
    Write-Host ""
    Write-Host "Repository Summary:" -ForegroundColor Green
    Write-Host "- Cleaned up 40+ unnecessary files" -ForegroundColor White
    Write-Host "- Renamed to Privacy Firewall branding" -ForegroundColor White
    Write-Host "- Updated all documentation and examples" -ForegroundColor White
    Write-Host "- Enhanced security and monitoring" -ForegroundColor White
}

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 