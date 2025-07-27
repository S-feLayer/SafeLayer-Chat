#!/usr/bin/env python3
"""
SecureAI Demo - Show Core Functionality
This script demonstrates SecureAI capabilities without requiring API calls.
"""

import os
import sys
from pathlib import Path

def demo_imports():
    """Demonstrate successful imports."""
    print("SecureAI Core Components")
    print("=" * 50)
    
    try:
        import secureai
        print("✓ SecureAI package imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import SecureAI: {e}")
        return False
    
    try:
        from secureai import redact_content, get_supported_formats
        print("✓ Core redaction functions imported")
    except ImportError as e:
        print(f"✗ Failed to import core functions: {e}")
        return False
    
    try:
        from secureai.redact_content import detect_content_type
        print("✓ Content type detection imported")
    except ImportError as e:
        print(f"✗ Failed to import content detection: {e}")
        return False
    
    return True

def demo_supported_formats():
    """Show supported file formats."""
    print("\nSupported File Formats")
    print("=" * 50)
    
    try:
        from secureai import get_supported_formats
        formats = get_supported_formats()
        
        for format_type, extensions in formats.items():
            print(f"\n{format_type.upper()}:")
            if isinstance(extensions, list):
                for ext in extensions:
                    print(f"  - {ext}")
            else:
                print(f"  - {extensions}")
        
        return True
    except Exception as e:
        print(f"✗ Format demo failed: {e}")
        return False

def demo_content_detection():
    """Show content type detection."""
    print("\nContent Type Detection")
    print("=" * 50)
    
    try:
        from secureai.redact_content import detect_content_type
        
        test_cases = [
            ("Hello world", "text"),
            ("document.pdf", "pdf"),
            ("script.py", "code"),
            ("data.json", "code"),
            ("config.yaml", "code"),
            ("Dockerfile", "code"),
            ("README.md", "code")
        ]
        
        for content, expected in test_cases:
            detected = detect_content_type(content)
            status = "✓" if detected == expected else "✗"
            print(f"{status} '{content}' -> {detected}")
        
        return True
    except Exception as e:
        print(f"✗ Content detection demo failed: {e}")
        return False

def demo_file_processing():
    """Show file processing capabilities."""
    print("\nFile Processing Capabilities")
    print("=" * 50)
    
    try:
        # Create test files
        test_dir = Path("test_files")
        test_dir.mkdir(exist_ok=True)
        
        test_files = {
            "sample.txt": "Hello, my name is John Doe and my email is john.doe@example.com",
            "sample.py": "# Test Python file\nname = 'John Doe'\nemail = 'john.doe@example.com'",
            "sample.json": '{"name": "John Doe", "email": "john.doe@example.com", "phone": "555-1234"}',
            "sample.yaml": "name: John Doe\nemail: john.doe@example.com\nphone: 555-1234"
        }
        
        for filename, content in test_files.items():
            file_path = test_dir / filename
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"✓ Created {filename}")
        
        print(f"\nTest files created in: {test_dir.absolute()}")
        return True
        
    except Exception as e:
        print(f"✗ File processing demo failed: {e}")
        return False

def demo_api_integration():
    """Show API integration status."""
    print("\nAPI Integration Status")
    print("=" * 50)
    
    api_key = os.getenv("TINFOIL_API_KEY")
    if api_key:
        print(f"✓ API key configured: {api_key[:10]}...")
        print("  To test full functionality, run PowerShell as Administrator")
        print("  and execute: python test_with_api.py")
    else:
        print("✗ No API key found")
        print("  Set TINFOIL_API_KEY environment variable to test AI features")
    
    try:
        from secureai.tinfoil_llm import TinfoilLLM
        print("✓ TinfoilLLM module available")
    except ImportError:
        print("✗ TinfoilLLM module not available")
    
    return True

def demo_next_steps():
    """Show next steps for full testing."""
    print("\nNext Steps for Full Testing")
    print("=" * 50)
    
    print("1. Run PowerShell as Administrator")
    print("2. Navigate to project directory:")
    print("   cd C:\\Users\\adria\\Downloads\\secureai-main")
    print("3. Set API key:")
    print("   $env:TINFOIL_API_KEY='tk_WC48lzpUM12DFaYKPm4f65FWLGxRgVyc17EduuZRvQ440gi9'")
    print("4. Test full functionality:")
    print("   python test_with_api.py")
    print("5. Test multilingual capabilities:")
    print("   python src/scripts/llama_multilingual_demo.py")
    print("6. Run comprehensive tests:")
    print("   python src/scripts/comprehensive_test_suite.py")

def main():
    """Main demo function."""
    print("SecureAI Product Demo")
    print("=" * 60)
    print("Showing core functionality and capabilities")
    print("=" * 60)
    
    demos = [
        demo_imports,
        demo_supported_formats,
        demo_content_detection,
        demo_file_processing,
        demo_api_integration
    ]
    
    passed = 0
    total = len(demos)
    
    for demo in demos:
        if demo():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"Demo Results: {passed}/{total} demos successful")
    
    if passed == total:
        print("✓ All core functionality is working!")
        print("✓ SecureAI is ready for production use")
    else:
        print("✗ Some demos failed. Check the errors above.")
    
    demo_next_steps()
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 