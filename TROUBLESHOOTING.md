# Troubleshooting Guide

This guide helps resolve common issues when setting up and testing Secure AI.

## 🐛 Common Issues and Solutions

### 1. **ModuleNotFoundError: No module named 'fitz'**

**Problem**: PyMuPDF is not installed or wrong version.

**Solutions**:
```bash
# Install the latest compatible version
pip install PyMuPDF>=1.26.0

# Or install all dependencies
python install_dependencies.py
```

**Note**: If you're using Python 3.13, make sure to use PyMuPDF 1.26.0 or later.

### 2. **Python Version Compatibility**

**Problem**: Using an incompatible Python version.

**Solution**: Use Python 3.10-3.13:
```bash
# Check your Python version
python --version

# If using Python 3.13, update pyproject.toml
# Change requires-python to ">=3.10.0,<3.14"
```

### 3. **Tinfoil API Key Not Set**

**Problem**: Missing TINFOIL_API_KEY environment variable.

**Solution**:
```bash
# Set environment variable
export TINFOIL_API_KEY="your_api_key_here"

# On Windows PowerShell
$env:TINFOIL_API_KEY="your_api_key_here"

# On Windows Command Prompt
set TINFOIL_API_KEY=your_api_key_here
```

### 4. **Import Errors**

**Problem**: Can't import secureai modules.

**Solutions**:
```bash
# Make sure you're in the project root
cd /path/to/secureai-main

# Install the project in development mode
pip install -e .

# Or add src to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### 5. **Permission Errors**

**Problem**: File permission or access denied errors.

**Solutions**:
```bash
# Run as administrator (Windows)
# Right-click PowerShell/Command Prompt and "Run as administrator"

# Check file permissions
ls -la src/scripts/

# Make scripts executable (Linux/Mac)
chmod +x src/scripts/*.py
```

### 6. **Memory Issues**

**Problem**: MemoryError or out of memory.

**Solutions**:
```bash
# Reduce test content size
# Edit test files to use smaller test data

# Increase system memory
# Close other applications

# Use smaller chunk sizes in performance tests
```

## 🔧 **Installation Issues**

### **PyMuPDF Installation Fails**

**Problem**: PyMuPDF fails to compile from source.

**Solutions**:
```bash
# Try installing pre-compiled wheel
pip install --only-binary=all PyMuPDF

# Or install from conda
conda install -c conda-forge pymupdf

# Or use a different Python version (3.10-3.12)
```

### **Missing Visual Studio (Windows)**

**Problem**: PyMuPDF needs Visual Studio to compile.

**Solutions**:
```bash
# Install Visual Studio Build Tools
# Download from: https://visualstudio.microsoft.com/downloads/

# Or use pre-compiled wheels
pip install --only-binary=all PyMuPDF

# Or use conda
conda install -c conda-forge pymupdf
```

## 🧪 **Testing Issues**

### **Tests Fail with Import Errors**

**Problem**: Tests can't import modules.

**Solution**:
```bash
# Run from project root
cd /path/to/secureai-main

# Add src to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Run tests
python src/scripts/test_universal_redaction.py
```

### **Tests Skip Due to Missing API Key**

**Problem**: Tests are skipped because TINFOIL_API_KEY is not set.

**Solution**:
```bash
# Set the API key
export TINFOIL_API_KEY="your_api_key_here"

# Run tests again
python src/scripts/test_universal_redaction.py
```

### **Performance Tests Take Too Long**

**Problem**: Performance benchmarks are slow.

**Solutions**:
```bash
# Reduce test iterations
# Edit performance_benchmark.py to use fewer iterations

# Use smaller test content
# Reduce content sizes in test files

# Skip performance tests if not needed
# Comment out performance test calls
```

## 🚀 **Quick Fix Commands**

### **Complete Reset and Reinstall**

```bash
# Remove existing installations
pip uninstall PyMuPDF fastmcp mcp tinfoil -y

# Clear pip cache
pip cache purge

# Reinstall everything
python install_dependencies.py

# Verify installation
python -c "import fitz, fastmcp, mcp, tinfoil; print('All imports successful')"
```

### **Test Only Core Functionality**

```bash
# Run basic tests without AI processing
python -c "
from secureai.redact_content import detect_content_type
from secureai.redact_code import detect_language
print('Core functionality works')
"
```

### **Check Environment**

```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "(PyMuPDF|fastmcp|mcp|tinfoil)"

# Check environment variables
echo $TINFOIL_API_KEY
```

## 📞 **Getting Help**

If you're still having issues:

1. **Check the logs**: Look for specific error messages
2. **Verify environment**: Make sure Python version and dependencies are correct
3. **Try minimal test**: Test with the simplest possible setup
4. **Check documentation**: Review the main README and testing guide
5. **Create issue**: Report the problem with detailed error messages

### **Debug Mode**

Enable debug output for more information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run your code with debug output
from secureai import redact_content
```

### **Minimal Test Case**

Create a minimal test to isolate the issue:

```python
# minimal_test.py
try:
    import fitz
    print("✅ PyMuPDF works")
except ImportError as e:
    print(f"❌ PyMuPDF failed: {e}")

try:
    from secureai.redact_content import detect_content_type
    print("✅ Secure AI imports work")
except ImportError as e:
    print(f"❌ Secure AI imports failed: {e}")
```

Run with: `python minimal_test.py` 