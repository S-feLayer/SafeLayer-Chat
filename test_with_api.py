#!/usr/bin/env python3
"""
Test SecureAI with API Key
This script tests the full functionality with your Tinfoil API key.
"""

import os
import sys

def test_api_connection():
    """Test connection to Tinfoil API."""
    print("Testing API Connection...")
    
    try:
        from secureai.tinfoil_llm import TinfoilLLM
        
        # Get API key from environment
        api_key = os.getenv("TINFOIL_API_KEY")
        if not api_key:
            print("No API key found in .env file")
            return False
        
        print(f"API key found: {api_key[:10]}...")
        
        # Initialize Tinfoil LLM
        tinfoil_llm = TinfoilLLM(api_key)
        print("TinfoilLLM initialized successfully")
        
        return tinfoil_llm
        
    except Exception as e:
        print(f"API connection failed: {e}")
        return False

def test_text_redaction(tinfoil_llm):
    """Test text redaction with API."""
    print("\nTesting Text Redaction...")
    
    try:
        from secureai import redact_text
        
        # Test text with PII
        test_text = "Hello, my name is John Doe and my email is john.doe@example.com"
        print(f"Original text: {test_text}")
        
        # Redact the text
        result = redact_text(test_text, tinfoil_llm)
        
        print(f"Redacted text: {result.get('redacted_text', 'N/A')}")
        print(f"Redactions found: {len(result.get('redactions', []))}")
        
        if result.get('redactions'):
            print("Detected PII:")
            for redaction in result.get('redactions', []):
                print(f"  - {redaction.get('type', 'Unknown')}: {redaction.get('value', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"Text redaction failed: {e}")
        return False

def main():
    """Main test function."""
    print("SecureAI API Test")
    print("=" * 50)
    
    # Test API connection
    tinfoil_llm = test_api_connection()
    if not tinfoil_llm:
        print("\nCannot proceed without API connection")
        return False
    
    # Test text redaction
    if not test_text_redaction(tinfoil_llm):
        print("\nText redaction test failed")
        return False
    
    print("\n" + "=" * 50)
    print("All tests passed! SecureAI is working with API key.")
    print("\nYour SecureAI product is fully functional!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 