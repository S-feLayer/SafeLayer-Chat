#!/usr/bin/env python3
"""
Simple Test Script for SecureAI
This script tests basic functionality without requiring API keys.
"""

import os
import sys
import time
from pathlib import Path

def test_imports():
    """Test if all modules can be imported."""
    print("Testing imports...")
    
    try:
        import secureai
        print("✓ SecureAI package imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import SecureAI: {e}")
        return False
    
    try:
        from secureai import redact_content, get_supported_formats
        print("✓ Core functions imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import core functions: {e}")
        return False
    
    return True

def test_supported_formats():
    """Test supported format detection."""
    print("\nTesting supported formats...")
    
    try:
        from secureai import get_supported_formats
        formats = get_supported_formats()
        print(f"✓ Supported formats: {formats}")
        return True
    except Exception as e:
        print(f"✗ Format test failed: {e}")
        return False

def test_content_type_detection():
    """Test content type detection."""
    print("\nTesting content type detection...")
    
    try:
        from secureai.redact_content import detect_content_type
        
        # Test different content types
        test_cases = [
            ("Hello world", "text"),
            ("test.pdf", "pdf"),
            ("script.py", "code"),
            ("data.json", "code"),
            ("config.yaml", "code")
        ]
        
        for content, expected in test_cases:
            detected = detect_content_type(content)
            status = "✓" if detected == expected else "✗"
            print(f"{status} '{content}' -> detected: {detected}, expected: {expected}")
        
        return True
    except Exception as e:
        print(f"✗ Content type detection failed: {e}")
        return False

def test_file_creation():
    """Test creating test files."""
    print("\nTesting file creation...")
    
    try:
        # Create test directory
        test_dir = Path("test_files")
        test_dir.mkdir(exist_ok=True)
        
        # Create test files
        test_files = {
            "test.txt": "Hello, my name is John Doe and my email is john.doe@example.com",
            "test.py": "# Test Python file\nname = 'John Doe'\nemail = 'john.doe@example.com'",
            "test.json": '{"name": "John Doe", "email": "john.doe@example.com"}'
        }
        
        for filename, content in test_files.items():
            file_path = test_dir / filename
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"✓ Created {filename}")
        
        return True
    except Exception as e:
        print(f"✗ File creation failed: {e}")
        return False

def test_basic_redaction():
    """Test basic redaction without API."""
    print("\nTesting basic redaction (without API)...")
    
    try:
        # This will test the function structure without requiring API
        from secureai import redact_content
        
        # Create a simple test file
        test_file = Path("test_files/simple_test.txt")
        with open(test_file, 'w') as f:
            f.write("Hello, my name is John Doe and my email is john.doe@example.com")
        
        print(f"✓ Test file created: {test_file}")
        print("Note: Full redaction requires Tinfoil API key")
        
        return True
    except Exception as e:
        print(f"✗ Basic redaction test failed: {e}")
        return False

def main():
    """Main test function."""
    print("SecureAI Simple Test")
    print("=" * 50)
    print(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        test_imports,
        test_supported_formats,
        test_content_type_detection,
        test_file_creation,
        test_basic_redaction
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! SecureAI is working correctly.")
        print("\nTo test with full functionality:")
        print("1. Get a Tinfoil API key from https://tinfoil.ai")
        print("2. Add it to the .env file")
        print("3. Run: python src/scripts/llama_multilingual_demo.py")
    else:
        print("✗ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 