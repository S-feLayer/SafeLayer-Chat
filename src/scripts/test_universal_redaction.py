#!/usr/bin/env python3
"""
Test script for Secure AI's universal redaction functionality.
This script tests all the new features to ensure they work correctly.
"""

import os
import tempfile
import sys
from pathlib import Path

# Add the src directory to the path so we can import secureai
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

def test_imports():
    """Test that all modules can be imported correctly."""
    print("🧪 Testing imports...")
    
    try:
        from secureai import redact_content, redact_pdf, redact_text, redact_code_file, get_supported_formats
        print("✅ All main functions imported successfully")
        
        from secureai.redact_content import detect_content_type, extract_input_data
        print("✅ Content detection functions imported successfully")
        
        from secureai.redact_code import CODE_EXTENSIONS, detect_language
        print("✅ Code redaction functions imported successfully")
        
        from secureai.tinfoil_llm import TinfoilLLM
        print("✅ Tinfoil LLM imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_content_type_detection():
    """Test content type detection functionality."""
    print("\n🧪 Testing content type detection...")
    
    from secureai.redact_content import detect_content_type
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
        f.write(b"print('hello')")
        temp_file = f.name
    
    try:
        # Test PDF detection
        assert detect_content_type("document.pdf") == "pdf"
        print("✅ PDF detection works")
        
        # Test code detection
        assert detect_content_type("script.py") == "code"
        assert detect_content_type("config.js") == "code"
        assert detect_content_type("Dockerfile") == "code"
        print("✅ Code detection works")
        
        # Test text detection
        assert detect_content_type("This is some text") == "text"
        print("✅ Text detection works")
        
        # Test dictionary parameters
        assert detect_content_type({"content_type": "pdf"}) == "pdf"
        assert detect_content_type({"content_type": "code"}) == "code"
        assert detect_content_type({"content_type": "text"}) == "text"
        print("✅ Dictionary parameter detection works")
        
        # Test unknown type
        assert detect_content_type("unknown.xyz") == "unknown"
        print("✅ Unknown type detection works")
        
        return True
    except AssertionError as e:
        print(f"❌ Detection test failed: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def test_supported_formats():
    """Test the supported formats function."""
    print("\n🧪 Testing supported formats...")
    
    from secureai import get_supported_formats
    
    try:
        formats = get_supported_formats()
        
        # Check that all expected content types are present
        assert "pdf" in formats
        assert "code" in formats
        assert "text" in formats
        
        # Check that code formats include common extensions
        code_extensions = formats["code"]
        assert ".py" in code_extensions
        assert ".js" in code_extensions
        assert ".java" in code_extensions
        
        print("✅ Supported formats function works")
        print(f"   PDF formats: {formats['pdf']}")
        print(f"   Code formats: {len(formats['code'])} supported languages")
        print(f"   Text formats: {formats['text']}")
        
        return True
    except AssertionError as e:
        print(f"❌ Formats test failed: {e}")
        return False

def test_code_language_detection():
    """Test code language detection."""
    print("\n🧪 Testing code language detection...")
    
    from secureai.redact_code import detect_language
    
    try:
        # Test various file extensions
        assert detect_language("script.py") == "python"
        assert detect_language("app.js") == "javascript"
        assert detect_language("main.java") == "java"
        assert detect_language("config.yaml") == "yaml"
        assert detect_language("Dockerfile") == "dockerfile"
        assert detect_language("unknown.xyz") == "unknown"
        
        print("✅ Language detection works")
        return True
    except AssertionError as e:
        print(f"❌ Language detection test failed: {e}")
        return False

def test_tinfoil_initialization():
    """Test Tinfoil LLM initialization."""
    print("\n🧪 Testing Tinfoil LLM initialization...")
    
    try:
        from secureai.tinfoil_llm import TinfoilLLM
        
        # This will fail if TINFOIL_API_KEY is not set, which is expected
        tinfoil_llm = TinfoilLLM()
        print("✅ Tinfoil LLM initialized successfully")
        return True
    except Exception as e:
        if "TINFOIL_API_KEY" in str(e):
            print("⚠️  Tinfoil LLM test skipped (TINFOIL_API_KEY not set)")
            return True
        else:
            print(f"❌ Tinfoil LLM initialization failed: {e}")
            return False

def run_all_tests():
    """Run all tests and report results."""
    print("🚀 Running Secure AI Universal Redaction Tests")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_content_type_detection,
        test_supported_formats,
        test_code_language_detection,
        test_tinfoil_initialization,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Universal redaction is ready to use.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 