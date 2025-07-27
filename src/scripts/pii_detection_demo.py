#!/usr/bin/env python3
"""
PII Detection Demonstration Script

This script demonstrates Secure AI's comprehensive PII detection capabilities
for preventing data leakage across different content types.
"""

import os
import sys
from typing import Dict, List, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from secureai.enhanced_detection import EnhancedDetection
from secureai.tinfoil_llm import TinfoilLLM

def create_test_content() -> Dict[str, str]:
    """Create test content with various types of PII."""
    
    return {
        "pdf_text": """
        CONTRACT AGREEMENT
        
        This agreement is between John Doe (john.doe@acme.com, phone: 555-123-4567)
        and Acme Corporation (123 Main Street, New York, NY 10001).
        
        Customer ID: CUST-12345
        Contract Number: CNT-2024-001
        Social Security Number: 123-45-6789
        Credit Card: 4111-1111-1111-1111
        
        Birth Date: January 15, 1990
        Account Number: 9876543210
        """,
        
        "code_file": """
        # Configuration file with sensitive data
        import os
        
        # Database credentials
        DATABASE_URL = "postgresql://user:password123@localhost:5432/mydb"
        
        # API Keys
        OPENAI_API_KEY = "sk-1234567890abcdef1234567890abcdef1234567890abcdef"
        GITHUB_TOKEN = "ghp_1234567890abcdef1234567890abcdef1234567890"
        
        # AWS Credentials
        AWS_ACCESS_KEY = "AKIA1234567890ABCDEF"
        AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
        
        # JWT Token
        AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        
        # Personal Information
        USER_EMAIL = "john.doe@company.com"
        USER_PHONE = "555-987-6543"
        
        # Private Key
        PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
        MIIEpAIBAAKCAQEA1234567890abcdef...
        -----END RSA PRIVATE KEY-----'''
        
        # Environment Variables
        os.environ['SECRET_PASSWORD'] = 'super_secret_password_123'
        os.environ['DATABASE_PASSWORD'] = 'db_password_456'
        """,
        
        "chat_message": """
        Hi team! I need to share some sensitive information:
        
        My name is Jane Smith and my email is jane.smith@techcorp.com
        My phone number is +1-555-987-6543
        My employee ID is EMP-78901
        
        I'm working on the project with contract number CNT-2024-002
        The client is Tech Solutions Inc. located at 456 Business Ave, San Francisco, CA 94102
        
        Please keep this confidential!
        """
    }

def demonstrate_pattern_detection(detector: EnhancedDetection, content: Dict[str, str]):
    """Demonstrate pattern-based PII detection."""
    
    print("🔍 PATTERN-BASED PII DETECTION")
    print("=" * 50)
    
    for content_type, text in content.items():
        print(f"\n📋 {content_type.upper().replace('_', ' ')}:")
        print("-" * 30)
        
        detected = detector.detect_with_patterns(text)
        
        if detected:
            for data_type, values in detected.items():
                print(f"  🔴 {data_type.upper()}:")
                for value in values:
                    print(f"    • {value}")
        else:
            print("  ✅ No pattern-based PII detected")

def demonstrate_ai_detection(detector: EnhancedDetection, content: Dict[str, str]):
    """Demonstrate AI-powered PII detection."""
    
    print("\n🤖 AI-POWERED PII DETECTION")
    print("=" * 50)
    
    for content_type, text in content.items():
        print(f"\n📋 {content_type.upper().replace('_', ' ')}:")
        print("-" * 30)
        
        try:
            # Map content types to AI detection types
            ai_content_type = "code" if "code" in content_type else "text"
            detected = detector.detect_with_ai(text, ai_content_type)
            
            if detected:
                for data_type, values in detected.items():
                    if values:  # Only show non-empty results
                        print(f"  🔴 {data_type.upper()}:")
                        for value in values:
                            print(f"    • {value}")
            else:
                print("  ✅ No AI-detected PII")
                
        except Exception as e:
            print(f"  ⚠️ AI detection failed: {e}")

def demonstrate_combined_detection(detector: EnhancedDetection, content: Dict[str, str]):
    """Demonstrate combined pattern + AI detection."""
    
    print("\n🔄 COMBINED DETECTION (Pattern + AI)")
    print("=" * 50)
    
    for content_type, text in content.items():
        print(f"\n📋 {content_type.upper().replace('_', ' ')}:")
        print("-" * 30)
        
        try:
            # Map content types to detection types
            detection_type = "code" if "code" in content_type else "text"
            detected = detector.detect_sensitive_data(text, detection_type)
            
            if detected:
                for data_type, values in detected.items():
                    if values:  # Only show non-empty results
                        print(f"  🔴 {data_type.upper()}:")
                        for value in values:
                            print(f"    • {value}")
            else:
                print("  ✅ No PII detected")
                
        except Exception as e:
            print(f"  ⚠️ Combined detection failed: {e}")

def demonstrate_validation(detector: EnhancedDetection, content: Dict[str, str]):
    """Demonstrate PII validation and filtering."""
    
    print("\n✅ PII VALIDATION AND FILTERING")
    print("=" * 50)
    
    for content_type, text in content.items():
        print(f"\n📋 {content_type.upper().replace('_', ' ')}:")
        print("-" * 30)
        
        try:
            detection_type = "code" if "code" in content_type else "text"
            detected = detector.detect_sensitive_data(text, detection_type)
            validated = detector.validate_detection(detected)
            
            print(f"  📊 Raw detections: {len(detected)} types")
            print(f"  ✅ Validated detections: {len(validated)} types")
            
            if validated:
                for data_type, values in validated.items():
                    print(f"  🔴 {data_type.upper()}: {len(values)} items")
                    
        except Exception as e:
            print(f"  ⚠️ Validation failed: {e}")

def demonstrate_data_leakage_prevention():
    """Demonstrate how the system prevents data leakage."""
    
    print("\n🛡️ DATA LEAKAGE PREVENTION")
    print("=" * 50)
    
    print("""
    Secure AI prevents data leakage through multiple layers:
    
    1. 🔍 COMPREHENSIVE DETECTION
       • Pattern-based detection for known PII formats
       • AI-powered detection for contextual PII
       • Content-specific detection strategies
    
    2. 🎯 ACCURATE IDENTIFICATION
       • Validates detected PII before processing
       • Filters out false positives
       • Combines multiple detection methods
    
    3. 🔒 SECURE PROCESSING
       • Local processing - data never leaves your machine
       • Isolated AI - uses Tinfoil's secure enclaves
       • Reversible masking - original data is preserved
    
    4. 📊 COMPLETE REPORTING
       • Detailed redaction summaries
       • Masked data previews
       • Audit trails of what was redacted
    
    5. 🚀 UNIVERSAL COVERAGE
       • PDFs: Legal documents, medical records, contracts
       • Code: API keys, passwords, credentials
       • Text: Chat messages, emails, documents
    """)

def main():
    """Main demonstration function."""
    
    print("🛡️ SECUREAI PII DETECTION DEMONSTRATION")
    print("=" * 60)
    print("Comprehensive PII detection to prevent data leakage")
    print("=" * 60)
    
    # Check for Tinfoil API key
    if not os.getenv("TINFOIL_API_KEY"):
        print("⚠️ TINFOIL_API_KEY not set. AI detection will be limited.")
        print("Set your API key: export TINFOIL_API_KEY='your_key_here'")
        return
    
    try:
        # Initialize components
        tinfoil_llm = TinfoilLLM()
        detector = EnhancedDetection(tinfoil_llm)
        
        # Create test content
        content = create_test_content()
        
        # Run demonstrations
        demonstrate_pattern_detection(detector, content)
        demonstrate_ai_detection(detector, content)
        demonstrate_combined_detection(detector, content)
        demonstrate_validation(detector, content)
        demonstrate_data_leakage_prevention()
        
        print("\n🎉 PII Detection Demonstration Complete!")
        print("\n💡 Key Benefits:")
        print("  • Prevents accidental data leakage")
        print("  • Comprehensive PII coverage")
        print("  • Secure, local processing")
        print("  • Multiple detection strategies")
        print("  • Content-specific optimization")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        print("Make sure TINFOIL_API_KEY is set and all dependencies are installed.")

if __name__ == "__main__":
    main() 