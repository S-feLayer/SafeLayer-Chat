#!/usr/bin/env python3
"""
Simple SecureAI Example
This shows how to use the AI Privacy Shield for basic PII protection.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def simple_redaction_example():
    """Show a simple redaction example."""
    print(" Simple SecureAI Example")
    print("=" * 50)
    
    # Example content with PII
    sensitive_content = """
    Hi, I'm John Smith and I work at Acme Corporation. 
    My email is john.smith@acme.com and my phone is 555-123-4567.
    I need help with a project for our client Sarah Johnson.
    Her email is sarah.j@techstart.com and she's based in San Francisco.
    """
    
    print("Original Content:")
    print("-" * 30)
    print(sensitive_content)
    
    print("\nRedacted Content (Conceptual):")
    print("-" * 30)
    print("""
    Hi, I'm [PERSON_1] and I work at [ORGANIZATION_1]. 
    My email is [EMAIL_1] and my phone is [PHONE_1].
    I need help with a project for our client [PERSON_2].
    Her email is [EMAIL_2] and she's based in [LOCATION_1].
    """)
    
    print("\nKey Features Demonstrated:")
    print("✓ Name detection and redaction")
    print("✓ Email address protection")
    print("✓ Phone number masking")
    print("✓ Organization name protection")
    print("✓ Location information redaction")

def file_processing_example():
    """Show file processing capabilities."""
    print("\n📁 File Processing Example")
    print("=" * 50)
    
    # Create a test file with sensitive data
    test_content = """
    # Configuration file
    DATABASE_URL = "postgresql://user:password123@localhost:5432/db"
    API_KEY = "sk-1234567890abcdef"
    ADMIN_EMAIL = "admin@company.com"
    """
    
    with open("test_config.py", "w") as f:
        f.write(test_content)
    
    print("Created test_config.py with sensitive data")
    print("SecureAI can process this file and redact:")
    print("✓ Database connection strings")
    print("✓ API keys")
    print("✓ Email addresses")
    print("✓ Passwords")

def conversation_example():
    """Show conversation persistence."""
    print("\n Conversation Persistence Example")
    print("=" * 50)
    
    conversation = [
        "User: Hi, I'm John Smith from Acme Corp.",
        "Assistant: Hello John! How can I help you?",
        "User: I need to contact Sarah Johnson at sarah@techstart.com",
        "Assistant: I'll help you reach out to Sarah."
    ]
    
    print("Original Conversation:")
    for msg in conversation:
        print(f"  {msg}")
    
    print("\nRedacted Conversation (with persistence):")
    print("  User: Hi, I'm [PERSON_1] from [ORGANIZATION_1].")
    print("  Assistant: Hello [PERSON_1]! How can I help you?")
    print("  User: I need to contact [PERSON_2] at [EMAIL_1]")
    print("  Assistant: I'll help you reach out to [PERSON_2].")
    
    print("\nNote: [PERSON_1] consistently refers to John Smith")
    print("      [PERSON_2] consistently refers to Sarah Johnson")

def main():
    """Main example function."""
    print("SecureAI Data Loss Prevention - Usage Examples")
    print("=" * 60)
    
    simple_redaction_example()
    file_processing_example()
    conversation_example()
    
    print("\n" + "=" * 60)
    print("To use the full system with AI-powered detection:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Install secureai: pip install git+https://github.com/postralai/secureai@main")
    print("3. Set API key: $env:TINFOIL_API_KEY='your_key'")
    print("4. Run: python3 src/scripts/ai_privacy_shield_demo.py")

if __name__ == "__main__":
    main() 