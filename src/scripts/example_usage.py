#!/usr/bin/env python3
"""
Example usage of Secure AI's universal redaction capabilities.
This script demonstrates how to redact PDFs, code files, and text content.
"""

import os
import tempfile
from secureai import redact_content, get_supported_formats
from secureai.tinfoil_llm import TinfoilLLM

def create_example_files():
    """Create example files for demonstration."""
    examples = {}
    
    # Create example text content
    examples['text'] = """
    Hi John Doe,
    
    I wanted to follow up on our conversation about the project. 
    My email is john.smith@company.com and my phone number is 555-123-4567.
    The contract number is CNT-2024-001 and the customer ID is CUST-789.
    
    Best regards,
    Jane Wilson
    jane.wilson@company.com
    """
    
    # Create example code file
    examples['code'] = """
# Configuration file
API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "postgresql://user:password123@localhost:5432/mydb"
SECRET_TOKEN = "secret_token_here"

# User credentials
ADMIN_EMAIL = "admin@company.com"
ADMIN_PASSWORD = "admin123"

# Personal information
USER_NAME = "John Doe"
USER_PHONE = "555-987-6543"
USER_ADDRESS = "123 Main St, City, State 12345"
"""
    
    # Create temporary files
    temp_dir = tempfile.mkdtemp()
    
    # Save code example
    code_file = os.path.join(temp_dir, "config.py")
    with open(code_file, 'w') as f:
        f.write(examples['code'])
    examples['code_file'] = code_file
    
    return examples

def demonstrate_redaction():
    """Demonstrate the redaction capabilities."""
    print("🚀 Secure AI Universal Redaction Demo")
    print("=" * 50)
    
    # Initialize Tinfoil LLM
    try:
        tinfoil_llm = TinfoilLLM()
    except Exception as e:
        print(f"❌ Error initializing Tinfoil LLM: {e}")
        print("Please make sure you have set the TINFOIL_API_KEY environment variable")
        return
    
    # Create example files
    examples = create_example_files()
    
    print("\n📋 Supported Formats:")
    formats = get_supported_formats()
    for content_type, extensions in formats.items():
        print(f"  {content_type}: {', '.join(extensions[:5])}{'...' if len(extensions) > 5 else ''}")
    
    print("\n" + "=" * 50)
    
    # Demo 1: Text redaction
    print("\n💬 Demo 1: Text Content Redaction")
    print("-" * 30)
    print("Original text:")
    print(examples['text'])
    
    result = redact_content(examples['text'], tinfoil_llm)
    if result.get('success'):
        redacted = result['redaction_result']
        print(f"\n✅ Redacted text ({redacted['redaction_count']} redactions):")
        print(redacted['redacted_text'])
        print(f"\n📊 Redacted items:")
        for item in redacted['redacted_items']:
            print(f"  {item['original']} → {item['masked']} ({item['count']} times)")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    print("\n" + "=" * 50)
    
    # Demo 2: Code file redaction
    print("\n💻 Demo 2: Code File Redaction")
    print("-" * 30)
    print("Original code:")
    print(examples['code'])
    
    result = redact_content(examples['code_file'], tinfoil_llm)
    if result.get('success'):
        redacted = result['redaction_result']
        print(f"\n✅ Redacted code ({redacted['redaction_count']} redactions):")
        print(redacted['redacted_code'])
        print(f"\n📁 Redacted file saved to: {redacted['redacted_file_path']}")
        print(f"🔧 Language detected: {redacted['language']}")
        print(f"\n📊 Redacted items:")
        for item in redacted['redacted_items']:
            print(f"  {item['original']} → {item['masked']} ({item['count']} times)")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    print("\n" + "=" * 50)
    
    # Demo 3: Universal redaction with different input types
    print("\n🌐 Demo 3: Universal Redaction")
    print("-" * 30)
    
    # Test with file path
    print("Testing with file path...")
    result = redact_content(examples['code_file'], tinfoil_llm)
    print(f"Content type detected: {result.get('content_type', 'unknown')}")
    
    # Test with text content
    print("\nTesting with text content...")
    result = redact_content(examples['text'], tinfoil_llm)
    print(f"Content type detected: {result.get('content_type', 'unknown')}")
    
    # Test with dictionary parameters
    print("\nTesting with dictionary parameters...")
    params = {
        'text': examples['text'],
        'content_type': 'text'
    }
    result = redact_content(params, tinfoil_llm)
    print(f"Content type detected: {result.get('content_type', 'unknown')}")
    
    print("\n" + "=" * 50)
    print("✅ Demo completed!")
    print("\n💡 Usage Tips:")
    print("  - Use 'redact_content()' for universal redaction")
    print("  - Pass file paths for PDFs and code files")
    print("  - Pass text strings for chat messages and documents")
    print("  - Use dictionary parameters for more control")
    print("  - Check 'success' field in results for errors")

if __name__ == "__main__":
    demonstrate_redaction() 