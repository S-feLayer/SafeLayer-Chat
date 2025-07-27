#!/usr/bin/env python3
"""
AI Privacy Shield Demo

This script demonstrates the AI Privacy Shield product capabilities:
- Real-time PII detection and redaction
- Continuous entity persistence
- Context preservation across conversations
- Enterprise security features
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def create_demo_conversation() -> List[Dict[str, str]]:
    """Create a realistic conversation with PII for demonstration."""
    return [
        {
            "speaker": "user",
            "content": "Hi, I'm John Smith and I work at Acme Corporation. My email is john.smith@acme.com and my phone number is 555-123-4567.",
            "timestamp": "2024-01-15T10:00:00Z"
        },
        {
            "speaker": "assistant", 
            "content": "Hello John! I can help you with your work at Acme Corporation. What can I assist you with today?",
            "timestamp": "2024-01-15T10:00:01Z"
        },
        {
            "speaker": "user",
            "content": "I need help with a project for our client, Sarah Johnson from TechStart Inc. Her email is sarah.j@techstart.com and she's based in San Francisco, CA.",
            "timestamp": "2024-01-15T10:02:00Z"
        },
        {
            "speaker": "assistant",
            "content": "I'd be happy to help with the project for Sarah Johnson from TechStart Inc. What specific aspects of the project do you need assistance with?",
            "timestamp": "2024-01-15T10:02:01Z"
        },
        {
            "speaker": "user",
            "content": "Sarah mentioned that the budget is $50,000 and we need to deliver by March 15th. Can you help me create a project plan?",
            "timestamp": "2024-01-15T10:03:00Z"
        },
        {
            "speaker": "assistant",
            "content": "Absolutely! For the $50,000 budget project with TechStart Inc., I can help create a comprehensive project plan. Let me break this down into phases.",
            "timestamp": "2024-01-15T10:03:01Z"
        },
        {
            "speaker": "user",
            "content": "Great! Also, I need to coordinate with our team lead, Mike Chen. His email is mike.chen@acme.com and he's in our New York office.",
            "timestamp": "2024-01-15T10:04:00Z"
        },
        {
            "speaker": "assistant",
            "content": "Perfect! I'll include Mike Chen from the New York office in the project plan. This will ensure proper coordination across teams.",
            "timestamp": "2024-01-15T10:04:01Z"
        }
    ]

def create_technical_conversation() -> List[Dict[str, str]]:
    """Create a technical conversation with code and API keys."""
    return [
        {
            "speaker": "user",
            "content": "I'm debugging an issue with our API. The endpoint is https://api.acme.com/v1/users and I'm using the API key sk-1234567890abcdef. Can you help?",
            "timestamp": "2024-01-15T11:00:00Z"
        },
        {
            "speaker": "assistant",
            "content": "I can help you debug the API issue. Let me analyze the endpoint and API key configuration.",
            "timestamp": "2024-01-15T11:00:01Z"
        },
        {
            "speaker": "user", 
            "content": "The database connection string is postgresql://user:password123@localhost:5432/acme_db. I think the issue might be in the authentication.",
            "timestamp": "2024-01-15T11:01:00Z"
        },
        {
            "speaker": "assistant",
            "content": "I see the issue. The database connection string contains sensitive credentials. Let me help you secure this properly.",
            "timestamp": "2024-01-15T11:01:01Z"
        }
    ]

def create_healthcare_conversation() -> List[Dict[str, str]]:
    """Create a healthcare conversation with PHI (Protected Health Information)."""
    return [
        {
            "speaker": "user",
            "content": "Patient John Doe, DOB 1985-03-15, SSN 123-45-6789, has been experiencing chest pain for the past week.",
            "timestamp": "2024-01-15T12:00:00Z"
        },
        {
            "speaker": "assistant",
            "content": "I understand you're concerned about the patient's chest pain. Let me help you document this properly.",
            "timestamp": "2024-01-15T12:00:01Z"
        },
        {
            "speaker": "user",
            "content": "The patient's address is 123 Main St, Boston, MA 02101 and their phone is 617-555-0123. They have a history of hypertension.",
            "timestamp": "2024-01-15T12:01:00Z"
        },
        {
            "speaker": "assistant",
            "content": "I've noted the patient's contact information and medical history. Let's proceed with the assessment.",
            "timestamp": "2024-01-15T12:01:01Z"
        }
    ]

def demonstrate_basic_redaction():
    """Demonstrate basic redaction without persistence."""
    print("🔒 BASIC REDACTION DEMONSTRATION")
    print("=" * 50)
    
    try:
        from secureai.ai_privacy_shield import AIPrivacyShield
        
        # Initialize shield without persistence for basic demo
        shield = AIPrivacyShield(enable_persistence=False)
        
        test_message = "Hi, I'm John Smith. My email is john@example.com and phone is 555-123-4567."
        
        print(f"📝 Original: {test_message}")
        
        result = shield.redact_content(test_message, "text")
        
        print(f"🔒 Redacted: {result.redacted_content}")
        print(f"📊 Entities detected: {len(result.detected_entities)}")
        print(f"⚡ Processing time: {result.processing_time_ms:.2f}ms")
        print(f"🤖 Model used: {result.model_used}")
        
        if result.detected_entities:
            print("\n🔍 Detected entities:")
            for entity in result.detected_entities:
                print(f"  • {entity['type']}: {entity['value']}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Error: {e}")

def demonstrate_entity_persistence():
    """Demonstrate continuous entity persistence."""
    print("\n🔄 ENTITY PERSISTENCE DEMONSTRATION")
    print("=" * 50)
    
    try:
        from secureai.ai_privacy_shield import AIPrivacyShield
        
        # Initialize shield with persistence
        shield = AIPrivacyShield(enable_persistence=True)
        
        session_id = "demo_session_123"
        user_id = "user_456"
        
        conversation = create_demo_conversation()
        
        print("🗣️ Processing conversation with entity persistence...")
        print()
        
        for i, message in enumerate(conversation, 1):
            if message["speaker"] == "user":  # Only process user messages
                print(f"📝 Message {i}: {message['content']}")
                
                result = shield.redact_content(
                    message["content"], 
                    "text", 
                    session_id, 
                    user_id
                )
                
                print(f"🔒 Redacted: {result.redacted_content}")
                print(f"📊 Entities: {len(result.detected_entities)}")
                
                if result.entity_mappings:
                    print("🔄 Entity mappings:")
                    for mapping in result.entity_mappings:
                        print(f"  • {mapping.original_value} → {mapping.masked_value}")
                
                print("-" * 40)
        
        print("✅ Notice how 'John Smith' stays 'Person X' throughout the conversation!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 This demo requires Redis and PostgreSQL for full functionality")

def demonstrate_technical_redaction():
    """Demonstrate redaction of technical content."""
    print("\n💻 TECHNICAL CONTENT REDACTION")
    print("=" * 50)
    
    try:
        from secureai.ai_privacy_shield import AIPrivacyShield
        
        shield = AIPrivacyShield(enable_persistence=True)
        
        technical_conversation = create_technical_conversation()
        
        for message in technical_conversation:
            if message["speaker"] == "user":
                print(f"📝 Original: {message['content']}")
                
                result = shield.redact_content(message["content"], "text")
                
                print(f"🔒 Redacted: {result.redacted_content}")
                print(f"📊 Technical entities: {len(result.detected_entities)}")
                print("-" * 40)
        
    except Exception as e:
        print(f"❌ Error: {e}")

def demonstrate_healthcare_compliance():
    """Demonstrate healthcare compliance redaction."""
    print("\n🏥 HEALTHCARE COMPLIANCE REDACTION")
    print("=" * 50)
    
    try:
        from secureai.ai_privacy_shield import AIPrivacyShield
        
        shield = AIPrivacyShield(enable_persistence=True)
        
        healthcare_conversation = create_healthcare_conversation()
        
        for message in healthcare_conversation:
            if message["speaker"] == "user":
                print(f"📝 Original: {message['content']}")
                
                result = shield.redact_content(message["content"], "text")
                
                print(f"🔒 Redacted: {result.redacted_content}")
                print(f"📊 PHI entities: {len(result.detected_entities)}")
                print("-" * 40)
        
    except Exception as e:
        print(f"❌ Error: {e}")

def demonstrate_enterprise_api():
    """Demonstrate enterprise API usage."""
    print("\n🏢 ENTERPRISE API DEMONSTRATION")
    print("=" * 50)
    
    try:
        from secureai.ai_privacy_shield import EnterprisePrivacyAPI
        
        # Initialize enterprise API
        api = EnterprisePrivacyAPI(
            tinfoil_api_key=os.getenv("TINFOIL_API_KEY"),
            redis_url=os.getenv("REDIS_URL"),
            postgres_url=os.getenv("POSTGRES_URL")
        )
        
        # Single message redaction
        message = "Hi, I'm Alice Johnson from TechCorp. My email is alice@techcorp.com."
        
        print("📝 Single message redaction:")
        result = api.redact_message(message, "session_123", "user_456", "org_789")
        print(f"Original: {message}")
        print(f"Redacted: {result['redacted_message']}")
        print(f"Entities: {result['entities_detected']}")
        print(f"Time: {result['processing_time_ms']:.2f}ms")
        
        # Conversation redaction
        print("\n🗣️ Conversation redaction:")
        conversation = [
            {"content": "Hi, I'm Bob Smith from Acme Inc."},
            {"content": "My colleague Alice Johnson will join us."},
            {"content": "Her email is alice@acme.com"}
        ]
        
        results = api.redact_conversation(conversation, "session_123", "user_456", "org_789")
        
        for i, result in enumerate(results, 1):
            print(f"Message {i}:")
            print(f"  Original: {result['original_message']}")
            print(f"  Redacted: {result['redacted_message']}")
            print(f"  Entities: {result['entities_detected']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 This demo requires proper environment variables")

def demonstrate_performance_metrics():
    """Demonstrate performance and scalability metrics."""
    print("\n⚡ PERFORMANCE METRICS")
    print("=" * 50)
    
    try:
        from secureai.ai_privacy_shield import AIPrivacyShield
        import time
        
        shield = AIPrivacyShield(enable_persistence=False)
        
        # Test different content sizes
        test_cases = [
            ("Small", "Hi, I'm John. Email: john@example.com"),
            ("Medium", "Hi, I'm John Smith from Acme Corp. My email is john.smith@acme.com and phone is 555-123-4567. I work with Sarah Johnson from TechStart Inc."),
            ("Large", "Hi, I'm John Smith from Acme Corporation. My email is john.smith@acme.com and phone is 555-123-4567. I work with Sarah Johnson from TechStart Inc. Her email is sarah.j@techstart.com. We also have Mike Chen from New York office, email mike.chen@acme.com. The project budget is $50,000 and we need to deliver by March 15th.") * 3
        ]
        
        print("📊 Performance by content size:")
        print(f"{'Size':<10} {'Length':<8} {'Time (ms)':<12} {'Entities':<10}")
        print("-" * 45)
        
        for size, content in test_cases:
            start_time = time.time()
            result = shield.redact_content(content, "text")
            end_time = time.time()
            
            processing_time = (end_time - start_time) * 1000
            
            print(f"{size:<10} {len(content):<8} {processing_time:<12.2f} {len(result.detected_entities):<10}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def demonstrate_compliance_features():
    """Demonstrate compliance and audit features."""
    print("\n📋 COMPLIANCE & AUDIT FEATURES")
    print("=" * 50)
    
    try:
        from secureai.ai_privacy_shield import AIPrivacyShield
        
        shield = AIPrivacyShield(enable_persistence=True)
        
        # Simulate audit trail
        session_id = "audit_session_123"
        user_id = "user_audit_456"
        org_id = "org_audit_789"
        
        messages = [
            "Patient John Doe, SSN 123-45-6789, has chest pain",
            "Contact Dr. Sarah Johnson at sarah.j@hospital.com",
            "Patient's address: 123 Main St, Boston, MA"
        ]
        
        print("📝 Processing messages for audit trail...")
        
        for i, message in enumerate(messages, 1):
            result = shield.redact_content(message, "text", session_id, user_id, org_id)
            
            print(f"\nMessage {i}:")
            print(f"  Original: {message}")
            print(f"  Redacted: {result.redacted_content}")
            print(f"  Entities: {len(result.detected_entities)}")
            print(f"  Model: {result.model_used}")
            print(f"  Timestamp: {result.redaction_summary['timestamp']}")
        
        # Export audit trail
        print(f"\n📋 Audit trail exported:")
        audit_data = shield.export_entity_mappings(session_id)
        print(f"  Format: JSON")
        print(f"  Session: {session_id}")
        print(f"  User: {user_id}")
        print(f"  Organization: {org_id}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all demonstrations."""
    print("🛡️ AI PRIVACY SHIELD - PRODUCT DEMONSTRATION")
    print("=" * 60)
    print("This demo showcases the AI Privacy Shield product capabilities")
    print("for enterprise PII protection in AI applications.")
    print()
    
    # Run demonstrations
    demonstrate_basic_redaction()
    demonstrate_entity_persistence()
    demonstrate_technical_redaction()
    demonstrate_healthcare_compliance()
    demonstrate_enterprise_api()
    demonstrate_performance_metrics()
    demonstrate_compliance_features()
    
    print("\n" + "=" * 60)
    print("🎯 PRODUCT SUMMARY")
    print("=" * 60)
    print("✅ Real-time PII detection and redaction")
    print("✅ Continuous entity persistence")
    print("✅ Context preservation across conversations")
    print("✅ Enterprise security and compliance")
    print("✅ High-performance processing")
    print("✅ Audit trails and reporting")
    print()
    print("🚀 Ready for enterprise deployment!")
    print("💡 Contact us for pricing and implementation details")

if __name__ == "__main__":
    main() 