@echo off
echo 🚀 SafeLayer-Chat GitHub Push Script
echo =====================================

REM Check if Git is available
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    echo After installation, restart and run this script again.
    pause
    exit /b 1
)

echo ✅ Git found
echo.

REM Check if we're in a Git repository
if exist ".git" (
    echo ✅ Git repository already initialized
) else (
    echo 🔄 Initializing Git repository...
    git init
)

REM Add all files
echo 📁 Adding all files to Git...
git add .

REM Commit changes
echo 💾 Committing changes...
git commit -m "Add complete SafeLayer-Chat SDK implementation

- Production-ready SDK package with clean API
- Comprehensive documentation and tutorials
- Command-line interface
- Type-safe data models with Pydantic
- Error handling and validation
- Build and distribution tools
- Usage examples and best practices"

REM Set remote
echo 🔄 Setting up remote...
git remote add origin https://github.com/S-feLayer/SafeLayer-Chat.git 2>nul
git remote set-url origin https://github.com/S-feLayer/SafeLayer-Chat.git

REM Push to GitHub
echo 🚀 Pushing to GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo ✅ Successfully pushed to GitHub!
    echo 📋 Repository URL: https://github.com/S-feLayer/SafeLayer-Chat
) else (
    echo ❌ Failed to push to GitHub
    echo This might be due to authentication issues or repository permissions.
    echo Try running: git push -u origin main
)

echo.
echo 🎉 Setup complete!
pause 