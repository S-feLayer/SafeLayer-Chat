#!/usr/bin/env python3
"""
Installation script for Secure AI dependencies.
This script helps install all required dependencies for the project.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and 10 <= version.minor <= 13:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python version not compatible. Requires Python 3.10-3.13")
        return False

def install_dependencies():
    """Install all required dependencies."""
    print("🚀 Installing Secure AI Dependencies")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Core dependencies
    dependencies = [
        ("PyMuPDF>=1.26.0", "PyMuPDF (PDF processing)"),
        ("fastmcp==0.4.1", "FastMCP (MCP server)"),
        ("mcp==1.3.0", "MCP (Model Context Protocol)"),
        ("tinfoil", "Tinfoil (AI processing)"),
    ]
    
    # Testing dependencies
    test_dependencies = [
        ("psutil>=5.8.0", "psutil (system monitoring)"),
        ("pytest>=7.0.0", "pytest (testing framework)"),
        ("pytest-cov>=4.0.0", "pytest-cov (test coverage)"),
        ("coverage>=7.0.0", "coverage (coverage reporting)"),
    ]
    
    # Install core dependencies
    print("\n📦 Installing core dependencies...")
    for dep, desc in dependencies:
        if not run_command(f"pip install {dep}", desc):
            return False
    
    # Install testing dependencies
    print("\n🧪 Installing testing dependencies...")
    for dep, desc in test_dependencies:
        if not run_command(f"pip install {dep}", desc):
            return False
    
    return True

def verify_installation():
    """Verify that all dependencies are installed correctly."""
    print("\n🔍 Verifying installation...")
    
    try:
        # Test imports
        import fitz
        print("✅ PyMuPDF imported successfully")
        
        import fastmcp
        print("✅ FastMCP imported successfully")
        
        import mcp
        print("✅ MCP imported successfully")
        
        import tinfoil
        print("✅ Tinfoil imported successfully")
        
        import psutil
        print("✅ psutil imported successfully")
        
        import pytest
        print("✅ pytest imported successfully")
        
        print("\n🎉 All dependencies installed and verified successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main installation function."""
    print("🚀 Secure AI Dependency Installer")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Installation failed. Please check the errors above.")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("\n❌ Verification failed. Please check the errors above.")
        sys.exit(1)
    
    print("\n✅ Installation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Set your TINFOIL_API_KEY environment variable")
    print("2. Run tests: python src/scripts/test_universal_redaction.py")
    print("3. Try the example: python src/scripts/example_usage.py")

if __name__ == "__main__":
    main() 