#!/usr/bin/env python3
"""
Test script to verify SecureAI installation and basic functionality.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import secureai
        print("secureai imported successfully")
    except ImportError as e:
        print(f"Failed to import secureai: {e}")
        return False
    
    try:
        from secureai.tinfoil_llm import TinfoilLLM
        print("TinfoilLLM imported successfully")
    except ImportError as e:
        print(f"Failed to import TinfoilLLM: {e}")
        return False
    
    try:
        from secureai import redact_content
        print("redact_content imported successfully")
    except ImportError as e:
        print(f"Failed to import redact_content: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality without API calls."""
    print("\nTesting basic functionality...")
    
    try:
        from secureai import redact_text
        
        # Test simple text redaction (without AI for basic test)
        test_text = "Hello, my name is John Doe and my email is john.doe@example.com"
        # For basic test, we'll just verify the function exists and can be called
        # In production, you would pass a tinfoil_llm instance
        print("Basic text redaction function available")
        print("   Note: Full redaction requires Tinfoil API key")
        
        return True
    except Exception as e:
        print(f"Basic functionality test failed: {e}")
        return False

def test_environment():
    """Test environment setup."""
    print("\nTesting environment...")
    
    # Check Python version
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and 10 <= version.minor <= 12:
        print("Python version is compatible")
    else:
        print("Python version may not be optimal")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Running in virtual environment")
    else:
        print("Not running in virtual environment")
    
    # Check for .env file
    if os.path.exists('.env'):
        print(".env file exists")
    else:
        print(".env file not found")
    
    return True

def main():
    """Main test function."""
    print("SecureAI Installation Test")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\nImport test failed. Installation may be incomplete.")
        return False
    
    # Test environment
    test_environment()
    
    # Test basic functionality
    if not test_basic_functionality():
        print("\nBasic functionality test failed.")
        return False
    
    print("\nAll tests passed! SecureAI is ready to use.")
    print("\nNext steps:")
    print("1. Add your Tinfoil API key to .env file")
    print("2. Run: python src/scripts/llama_multilingual_demo.py")
    print("3. Run: python src/scripts/comprehensive_test_suite.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 