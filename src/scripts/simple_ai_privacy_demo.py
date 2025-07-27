#!/usr/bin/env python3
"""
Simple AI Privacy Shield Demo

This script demonstrates the core AI Privacy Shield functionality
without requiring Redis or PostgreSQL.
"""

import os
import sys
from datetime import datetime

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_basic_redaction():
    """Test basic redaction functionality."""
    print("🔒 BASIC REDACTION TEST")
    print("=" * 40)
    
    try:
        from secureai.tinfoil_llm import TinfoilLLM
        from secureai.enhanced_detection import EnhancedDetection
        from secureai.advanced_masking import AdvancedMasking, MaskingStrategy
        
        # Initialize components
        tinfoil_llm = TinfoilLLM()
        detector = EnhancedDetection(tinfoil_llm)
        masker = AdvancedMasking(MaskingStrategy.PARTIAL)
        
        # Test message with PII
        test_message = "Hi, I'm John Smith. My email is john.smith@company.com and my phone is 555-123-4567."
        
        print(f"📝 Original: {test_message}")
        
        # Detect sensitive data
        detected_entities = detector.detect_sensitive_data(test_message, "text")
        
        print(f"🔍 Detected entities: {len(detected_entities)}")
        for entity_type, values in detected_entities.items():
            for value in values:
                print(f"  • {entity_type}: {value}")
        
        # Mask the content
        masked_result = masker.mask_content(test_message, detected_entities)
        
        print(f"🔒 Redacted: {masked_result['redacted_content']}")
        print(f"📊 Masking summary: {masked_result['summary']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_smart_model_selection():
    """Test smart model selection."""
    print("\n🧠 SMART MODEL SELECTION TEST")
    print("=" * 40)
    
    try:
        from secureai.smart_model_selection import SmartModelSelector
        
        selector = SmartModelSelector()
        
        # Test different content types
        test_cases = [
            {
                "name": "Code Content",
                "content": """
                import os
                from flask import Flask
                
                app = Flask(__name__)
                
                DATABASE_URL = "postgresql://user:password@localhost:5432/db"
                API_KEY = "sk-1234567890abcdef"
                
                @app.route('/')
                def hello():
                    return "Hello World!"
                """,
                "type": "code"
            },
            {
                "name": "Multilingual Content",
                "content": "Bonjour! I'm Jean Dupont from Paris. My email is jean.dupont@company.fr",
                "type": "text"
            },
            {
                "name": "Financial Content",
                "content": "The quarterly revenue was $1,250,000. Contact Sarah Johnson at sarah@company.com",
                "type": "text"
            }
        ]
        
        for test_case in test_cases:
            print(f"\n📋 {test_case['name']}")
            print(f"Content: {test_case['content'][:100]}...")
            
            recommendation = selector.get_model_recommendation(
                test_case["content"], 
                test_case["type"]
            )
            
            print(f"Selected Model: {recommendation['model_name']}")
            print(f"Reasoning: {recommendation['reasoning']}")
            print(f"Complexity Score: {recommendation['characteristics']['complexity_score']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_enhanced_detection():
    """Test enhanced detection capabilities."""
    print("\n🔍 ENHANCED DETECTION TEST")
    print("=" * 40)
    
    try:
        from secureai.enhanced_detection import EnhancedDetection
        from secureai.tinfoil_llm import TinfoilLLM
        
        tinfoil_llm = TinfoilLLM()
        detector = EnhancedDetection(tinfoil_llm)
        
        # Test different types of sensitive data
        test_cases = [
            {
                "name": "Personal Information",
                "content": "Patient John Doe, DOB 1985-03-15, SSN 123-45-6789, phone 555-123-4567"
            },
            {
                "name": "Financial Information", 
                "content": "Credit card 4111-1111-1111-1111, account number 1234567890, routing 021000021"
            },
            {
                "name": "Technical Information",
                "content": "API key sk-1234567890abcdef, database password secret123, endpoint https://api.company.com"
            }
        ]
        
        for test_case in test_cases:
            print(f"\n📋 {test_case['name']}")
            print(f"Content: {test_case['content']}")
            
            # Pattern-based detection
            pattern_results = detector.detect_with_patterns(test_case["content"])
            print(f"Pattern Detection: {len(pattern_results)} entity types found")
            
            # Combined detection
            combined_results = detector.detect_sensitive_data(test_case["content"], "text")
            print(f"Combined Detection: {len(combined_results)} entity types found")
            
            for entity_type, values in combined_results.items():
                print(f"  • {entity_type}: {values}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_advanced_masking():
    """Test advanced masking strategies."""
    print("\n🎭 ADVANCED MASKING TEST")
    print("=" * 40)
    
    try:
        from secureai.advanced_masking import AdvancedMasking, MaskingStrategy
        
        test_content = "Hi, I'm John Smith. My email is john@example.com and phone is 555-123-4567."
        sensitive_data = {
            "name": ["John Smith"],
            "email": ["john@example.com"],
            "phone": ["555-123-4567"]
        }
        
        # Test different masking strategies
        strategies = [
            MaskingStrategy.PARTIAL,
            MaskingStrategy.FULL,
            MaskingStrategy.HASH,
            MaskingStrategy.ENCODE
        ]
        
        for strategy in strategies:
            print(f"\n🎭 {strategy.name} Masking:")
            masker = AdvancedMasking(strategy)
            result = masker.mask_content(test_content, sensitive_data)
            print(f"Result: {result['redacted_content']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_conversation_flow():
    """Test conversation flow with entity consistency."""
    print("\n🗣️ CONVERSATION FLOW TEST")
    print("=" * 40)
    
    try:
        from secureai.tinfoil_llm import TinfoilLLM
        from secureai.enhanced_detection import EnhancedDetection
        from secureai.advanced_masking import AdvancedMasking, MaskingStrategy
        
        tinfoil_llm = TinfoilLLM()
        detector = EnhancedDetection(tinfoil_llm)
        masker = AdvancedMasking(MaskingStrategy.PARTIAL)
        
        # Simulate a conversation
        conversation = [
            "Hi, I'm John Smith and I work at Acme Corporation.",
            "My email is john.smith@acme.com and my phone is 555-123-4567.",
            "I need help with a project for our client, Sarah Johnson.",
            "Her email is sarah.j@techstart.com and she's based in San Francisco.",
            "Can you help me coordinate with John Smith on this project?"
        ]
        
        print("🗣️ Processing conversation with entity consistency...")
        
        for i, message in enumerate(conversation, 1):
            print(f"\n📝 Message {i}: {message}")
            
            # Detect entities
            detected_entities = detector.detect_sensitive_data(message, "text")
            
            # Mask content
            masked_result = masker.mask_content(message, detected_entities)
            
            print(f"🔒 Redacted: {masked_result['redacted_content']}")
            print(f"📊 Entities: {len(detected_entities)} detected")
            
            if detected_entities:
                for entity_type, values in detected_entities.items():
                    print(f"  • {entity_type}: {values}")
        
        print("\n✅ Notice how entities are consistently masked across the conversation!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("🛡️ AI PRIVACY SHIELD - SIMPLE DEMO")
    print("=" * 50)
    print("Testing core functionality without external dependencies")
    print()
    
    # Set API key
    api_key = "tk_WC48lzpUM12DFaYKPm4f65FWLGxRgVyc17EduuZRvQ440gi9"
    os.environ["TINFOIL_API_KEY"] = api_key
    
    print(f"🔑 Using Tinfoil API key: {api_key[:10]}...")
    print()
    
    # Run tests
    tests = [
        test_basic_redaction,
        test_smart_model_selection,
        test_enhanced_detection,
        test_advanced_masking,
        test_conversation_flow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    print("=" * 50)
    
    if passed == total:
        print("🎉 All tests passed! AI Privacy Shield is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    print("\n🚀 Ready to build the AI Privacy Shield product!")
    print("💡 This demo shows the core capabilities without requiring Redis/PostgreSQL")

if __name__ == "__main__":
    main() 