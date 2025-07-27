#!/usr/bin/env python3
"""
SecureAI SDK Usage Examples

This file demonstrates how to use the SecureAI SDK for various redaction scenarios.
Perfect for tutorials and documentation.
"""

import os
from pathlib import Path
from secureai_sdk import SecureAI, ProcessingOptions, SecureAIError

def basic_text_redaction():
    """Basic text redaction example."""
    print("=== Basic Text Redaction ===")
    
    # Initialize client
    client = SecureAI(api_key="your_tinfoil_api_key")
    
    # Text with sensitive information
    sensitive_text = """
    Hello, my name is John Doe and my email is john.doe@company.com.
    You can reach me at 555-123-4567 or visit my website at https://example.com.
    My credit card number is 4111-1111-1111-1111 and my SSN is 123-45-6789.
    """
    
    try:
        # Redact the text
        result = client.redact_text(sensitive_text)
        
        if result.success:
            print("✅ Redaction successful!")
            print(f"📝 Original text: {sensitive_text.strip()}")
            print(f"🔒 Redacted text: {result.redacted_content}")
            print(f"🔍 Detected patterns: {result.detected_patterns}")
        else:
            print(f"❌ Redaction failed: {result.error}")
            
    except SecureAIError as e:
        print(f"❌ Error: {e}")

def pdf_redaction_example():
    """PDF redaction example."""
    print("\n=== PDF Redaction ===")
    
    client = SecureAI(api_key="your_tinfoil_api_key")
    
    # Path to your PDF file
    pdf_path = "document.pdf"
    
    if not Path(pdf_path).exists():
        print(f"⚠️  PDF file not found: {pdf_path}")
        print("   Please place a PDF file in the current directory to test this example.")
        return
    
    try:
        # Redact PDF with custom options
        options = ProcessingOptions(
            aggressive_mode=True,
            sensitivity_level="high",
            include_highlights=True
        )
        
        result = client.redact_pdf(pdf_path, options)
        
        if result.success:
            print("✅ PDF redaction successful!")
            print(f"📄 Original PDF: {pdf_path}")
            print(f"🔒 Redacted PDF: {result.redacted_file_path}")
            print(f"🔍 Highlighted PDF: {result.highlighted_file_path}")
            print(f"🔍 Detected patterns: {result.detected_patterns}")
            print(f"⏱️  Processing time: {result.processing_time:.2f}s")
        else:
            print(f"❌ PDF redaction failed: {result.error}")
            
    except SecureAIError as e:
        print(f"❌ Error: {e}")

def code_redaction_example():
    """Code redaction example."""
    print("\n=== Code Redaction ===")
    
    client = SecureAI(api_key="your_tinfoil_api_key")
    
    # Example code with sensitive data
    sensitive_code = '''
import os

# Database configuration
DB_HOST = "localhost"
DB_USER = "admin"
DB_PASSWORD = "secret_password_123"
DB_NAME = "production_db"

# API keys
API_KEY = "sk-1234567890abcdef"
SECRET_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
EMAIL_USER = "user@gmail.com"
EMAIL_PASSWORD = "email_password_456"

def connect_database():
    """Connect to the database."""
    connection = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    return connection
'''
    
    # Save code to temporary file
    temp_code_file = "temp_sensitive_code.py"
    with open(temp_code_file, "w") as f:
        f.write(sensitive_code)
    
    try:
        # Redact the code file
        result = client.redact_code(temp_code_file)
        
        if result.success:
            print("✅ Code redaction successful!")
            print(f"📄 Original code file: {temp_code_file}")
            print(f"🔒 Redacted code file: {result.redacted_file_path}")
            print(f"🔍 Detected patterns: {result.detected_patterns}")
            
            # Show redacted content
            if result.redacted_file_path and Path(result.redacted_file_path).exists():
                with open(result.redacted_file_path, "r") as f:
                    redacted_content = f.read()
                print(f"🔒 Redacted code:\n{redacted_content}")
        else:
            print(f"❌ Code redaction failed: {result.error}")
            
    except SecureAIError as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up temporary file
        if Path(temp_code_file).exists():
            Path(temp_code_file).unlink()

def advanced_options_example():
    """Advanced processing options example."""
    print("\n=== Advanced Options ===")
    
    client = SecureAI(api_key="your_tinfoil_api_key")
    
    # Text with various sensitive data
    text = """
    Customer ID: CUST-12345
    Order Number: ORD-67890
    Email: customer@example.com
    Phone: (555) 123-4567
    Address: 123 Main St, Anytown, USA 12345
    """
    
    # Custom processing options
    options = ProcessingOptions(
        aggressive_mode=True,
        sensitivity_level="high",
        preserve_format=True,
        include_highlights=True,
        custom_patterns=[
            r"CUST-\d{5}",
            r"ORD-\d{5}"
        ]
    )
    
    try:
        result = client.redact_text(text, options)
        
        if result.success:
            print("✅ Advanced redaction successful!")
            print(f"📝 Original: {text.strip()}")
            print(f"🔒 Redacted: {result.redacted_content}")
            print(f"🔍 Patterns: {result.detected_patterns}")
            print(f"⚙️  Options used: aggressive={options.aggressive_mode}, sensitivity={options.sensitivity_level}")
        else:
            print(f"❌ Advanced redaction failed: {result.error}")
            
    except SecureAIError as e:
        print(f"❌ Error: {e}")

def service_health_check():
    """Service health check example."""
    print("\n=== Service Health Check ===")
    
    client = SecureAI(api_key="your_tinfoil_api_key")
    
    try:
        # Check service health
        health = client.health_check()
        
        print(f"🏥 Service Status: {health.get('status', 'unknown')}")
        print(f"📊 Version: {health.get('version', 'unknown')}")
        print(f"🕒 Uptime: {health.get('uptime', 0):.1f}s")
        
        # Check individual services
        services = health.get('services', {})
        for service_name, service_status in services.items():
            status = service_status.get('status', 'unknown')
            print(f"  🔧 {service_name}: {status}")
        
        # Check system resources
        system = health.get('system', {})
        if 'memory' in system:
            memory = system['memory']
            print(f"💾 Memory Usage: {memory.get('percent', 0):.1f}%")
        
        if 'cpu' in system:
            cpu = system['cpu']
            print(f"🖥️  CPU Usage: {cpu.get('percent', 0):.1f}%")
            
    except SecureAIError as e:
        print(f"❌ Health check failed: {e}")

def supported_formats_example():
    """Get supported formats example."""
    print("\n=== Supported Formats ===")
    
    client = SecureAI(api_key="your_tinfoil_api_key")
    
    try:
        formats = client.get_supported_formats()
        
        print("📋 Supported Formats:")
        for category, format_list in formats.supported_formats.items():
            print(f"\n{category.upper()}:")
            for fmt in format_list:
                print(f"  • {fmt}")
        
        print(f"\n📏 Maximum file size: {formats.max_file_size}")
        print(f"📄 Supported file extensions: {', '.join(formats.file_extensions[:10])}...")
        
    except SecureAIError as e:
        print(f"❌ Failed to get formats: {e}")

def error_handling_example():
    """Error handling example."""
    print("\n=== Error Handling ===")
    
    # Example with invalid API key
    try:
        client = SecureAI(api_key="invalid_key")
        result = client.redact_text("test content")
    except SecureAIError as e:
        print(f"✅ Properly caught error: {e}")
    
    # Example with invalid file
    try:
        client = SecureAI(api_key="your_tinfoil_api_key")
        result = client.redact_pdf("nonexistent_file.pdf")
    except SecureAIError as e:
        print(f"✅ Properly caught file error: {e}")
    
    # Example with empty text
    try:
        client = SecureAI(api_key="your_tinfoil_api_key")
        result = client.redact_text("")
    except SecureAIError as e:
        print(f"✅ Properly caught validation error: {e}")

def context_manager_example():
    """Context manager usage example."""
    print("\n=== Context Manager Usage ===")
    
    # Using the client as a context manager
    with SecureAI(api_key="your_tinfoil_api_key") as client:
        try:
            result = client.redact_text("My email is test@example.com")
            if result.success:
                print("✅ Context manager redaction successful!")
                print(f"🔒 Result: {result.redacted_content}")
        except SecureAIError as e:
            print(f"❌ Error: {e}")

def main():
    """Run all examples."""
    print("🚀 SecureAI SDK Examples")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.getenv("TINFOIL_API_KEY")
    if not api_key:
        print("⚠️  TINFOIL_API_KEY environment variable not set.")
        print("   Please set it before running examples:")
        print("   export TINFOIL_API_KEY='your_api_key_here'")
        print()
    
    # Run examples
    basic_text_redaction()
    pdf_redaction_example()
    code_redaction_example()
    advanced_options_example()
    service_health_check()
    supported_formats_example()
    error_handling_example()
    context_manager_example()
    
    print("\n" + "=" * 50)
    print("✅ All examples completed!")

if __name__ == "__main__":
    main() 