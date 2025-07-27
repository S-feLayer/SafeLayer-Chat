# Windows Troubleshooting Guide

This guide addresses common Windows-specific issues when setting up and running SecureAI MCP.

## Permission Issues

### PowerShell Execution Policy
**Problem:** "Execution policy prevents running scripts"
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

### File Access Denied
**Problem:** "Access denied" when creating files or directories

**Solutions:**
1. **Run as Administrator:**
   - Right-click PowerShell/Command Prompt
   - Select "Run as Administrator"

2. **Check File Permissions:**
   ```powershell
   # Grant full control to current user
   $currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
   $acl = Get-Acl .
   $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule($currentUser, "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")
   $acl.SetAccessRule($accessRule)
   Set-Acl . $acl
   ```

3. **Disable Antivirus Temporarily:**
   - Some antivirus software blocks Python/pip operations
   - Temporarily disable real-time protection during installation

### Virtual Environment Issues

**Problem:** "Virtual environment activation fails"

**Solutions:**
1. **Use PowerShell instead of Command Prompt:**
   ```powershell
   .\pdfmcp\Scripts\Activate.ps1
   ```

2. **Check activation script exists:**
   ```powershell
   Test-Path ".\pdfmcp\Scripts\Activate.ps1"
   ```

3. **Recreate virtual environment:**
   ```powershell
   Remove-Item -Recurse -Force pdfmcp
   python -m venv pdfmcp
   .\pdfmcp\Scripts\Activate.ps1
   ```

## Python Installation Issues

### Python Not Found
**Problem:** "python is not recognized"

**Solutions:**
1. **Install via winget:**
   ```powershell
   winget install Python.Python.3.12
   ```

2. **Install via Microsoft Store:**
   - Search for "Python 3.12" in Microsoft Store
   - Install the official Python app

3. **Manual installation:**
   - Download from python.org
   - Check "Add Python to PATH" during installation

### PATH Issues
**Problem:** Python installed but not in PATH

**Solutions:**
1. **Add Python to PATH manually:**
   - System Properties → Environment Variables
   - Add Python installation directory to PATH
   - Typical paths: `C:\Users\[username]\AppData\Local\Programs\Python\Python312\` and `C:\Users\[username]\AppData\Local\Programs\Python\Python312\Scripts\`

2. **Use py launcher:**
   ```powershell
   py -3.12 -m pip install --upgrade pip
   py -3.12 -m venv pdfmcp
   ```

## Package Installation Issues

### pip Upgrade Fails
**Problem:** "pip upgrade fails with permission errors"

**Solutions:**
1. **Use user installation:**
   ```powershell
   python -m pip install --user --upgrade pip
   ```

2. **Use virtual environment:**
   ```powershell
   .\pdfmcp\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   ```

### Git Installation Required
**Problem:** "git is not recognized"

**Solutions:**
1. **Install Git for Windows:**
   ```powershell
   winget install Git.Git
   ```

2. **Download from git-scm.com:**
   - Download and install Git for Windows
   - Restart PowerShell after installation

### SSL Certificate Issues
**Problem:** "SSL certificate verification failed"

**Solutions:**
1. **Update certificates:**
   ```powershell
   python -m pip install --upgrade certifi
   ```

2. **Temporary workaround (not recommended for production):**
   ```powershell
   python -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org git+https://github.com/postralai/secureai@main
   ```

## Network Issues

### Proxy Configuration
**Problem:** "Connection timeout" behind corporate firewall

**Solutions:**
1. **Configure pip proxy:**
   ```powershell
   python -m pip install --proxy http://proxy.company.com:8080 git+https://github.com/postralai/secureai@main
   ```

2. **Set environment variables:**
   ```powershell
   $env:HTTP_PROXY = "http://proxy.company.com:8080"
   $env:HTTPS_PROXY = "http://proxy.company.com:8080"
   ```

### Firewall Issues
**Problem:** "Connection refused" when accessing APIs

**Solutions:**
1. **Add Python to firewall exceptions:**
   - Windows Defender Firewall → Allow an app through firewall
   - Add Python executable

2. **Check antivirus settings:**
   - Add Python and project directory to exclusions

## Performance Issues

### Slow Installation
**Problem:** "pip install takes too long"

**Solutions:**
1. **Use faster mirrors:**
   ```powershell
   python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple git+https://github.com/postralai/secureai@main
   ```

2. **Use conda instead of pip:**
   ```powershell
   conda install -c conda-forge secureai
   ```

### Memory Issues
**Problem:** "Out of memory" during processing

**Solutions:**
1. **Increase virtual memory:**
   - System Properties → Advanced → Performance Settings → Advanced → Virtual Memory
   - Increase page file size

2. **Process smaller files:**
   - Split large documents into smaller chunks
   - Use batch processing

## Claude Desktop Integration Issues

### Configuration File Location
**Problem:** "Cannot find Claude configuration file"

**Solutions:**
1. **Find config file:**
   ```powershell
   # Windows: %APPDATA%\Claude\claude_desktop_config.json
   $configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
   ```

2. **Create if missing:**
   ```powershell
   if (-not (Test-Path $configPath)) {
       New-Item -ItemType File -Path $configPath -Force
   }
   ```

### MCP Server Configuration
**Problem:** "MCP server not starting"

**Solutions:**
1. **Check Python path:**
   ```powershell
   .\pdfmcp\Scripts\Activate.ps1
   Get-Command python | Select-Object Source
   ```

2. **Check MCP file path:**
   ```powershell
   python -c "import secureai as m; print(f'{m.__path__[0]}/mcp_universal_redaction.py')"
   ```

3. **Verify configuration:**
   ```json
   {
     "mcpServers": {
       "universal-redaction": {
         "command": "C:\\path\\to\\pdfmcp\\Scripts\\python.exe",
         "args": ["C:\\path\\to\\secureai\\mcp_universal_redaction.py"],
         "env": {
           "TINFOIL_API_KEY": "your_api_key"
         }
       }
     }
   }
   ```

## Testing Issues

### Import Errors
**Problem:** "Module not found" errors

**Solutions:**
1. **Check virtual environment:**
   ```powershell
   .\pdfmcp\Scripts\Activate.ps1
   python -c "import sys; print(sys.executable)"
   ```

2. **Reinstall packages:**
   ```powershell
   python -m pip install --force-reinstall git+https://github.com/postralai/secureai@main
   ```

### Test File Permissions
**Problem:** "Cannot create test files"

**Solutions:**
1. **Create test directory:**
   ```powershell
   New-Item -ItemType Directory -Path "test_files" -Force
   ```

2. **Set permissions:**
   ```powershell
   $acl = Get-Acl "test_files"
   $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule($env:USERNAME, "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")
   $acl.SetAccessRule($accessRule)
   Set-Acl "test_files" $acl
   ```

## Common Error Messages

### "Access is denied"
- Run as Administrator
- Check file permissions
- Disable antivirus temporarily

### "The system cannot find the path specified"
- Check if Python is in PATH
- Verify virtual environment exists
- Use absolute paths

### "SSL: CERTIFICATE_VERIFY_FAILED"
- Update certificates: `python -m pip install --upgrade certifi`
- Check system date/time
- Use trusted hosts (temporary)

### "PermissionError: [Errno 13] Permission denied"
- Run as Administrator
- Check file permissions
- Close files that might be in use

## Getting Help

If you're still experiencing issues:

1. **Check logs:**
   ```powershell
   python -c "import logging; logging.basicConfig(level=logging.DEBUG)"
   ```

2. **Run diagnostic script:**
   ```powershell
   python src\scripts\comprehensive_test_suite.py
   ```

3. **Create issue report:**
   - Include Windows version: `winver`
   - Include Python version: `python --version`
   - Include error messages and stack traces
   - Include system information: `systeminfo`

4. **Community support:**
   - Check GitHub issues
   - Join Discord community
   - Contact support team 