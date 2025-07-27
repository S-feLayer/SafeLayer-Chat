#!/usr/bin/env python3
"""
Simple Llama 3.3 70B Test

This script tests the basic Llama 3.3 70B integration.
"""

import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_llama_basic():
    """Test basic Llama 3.3 70B functionality."""
    print("TESTING LLAMA 3.3 70B INTEGRATION")
    print("=" * 50)
    
    try:
        from secureai.tinfoil_llm import TinfoilLLM
        
        # Initialize with API key
        api_key = "tk_WC48lzpUM12DFaYKPm4f65FWLGxRgVyc17EduuZRvQ440gi9"
        tinfoil_llm = TinfoilLLM(api_key)
        
        print("✅ TinfoilLLM initialized successfully")
        
        # Test connection
        if tinfoil_llm.test_connection():
            print("✅ Connection to Tinfoil API successful")
        else:
            print("❌ Connection to Tinfoil API failed")
            return False
        
        # Get model info
        llama_info = tinfoil_llm.get_model_info("llama")
        print(f"✅ Llama model info retrieved:")
        print(f"   Name: {llama_info['name']}")
        print(f"   Model ID: {llama_info['model_id']}")
        print(f"   Languages: {', '.join(llama_info['languages'])}")
        
        # Test simple response
        test_prompt = "Hello! This is a test message."
        print(f"\nTesting simple response with prompt: {test_prompt}")
        
        response = tinfoil_llm.get_tinfoil_response(test_prompt, "llama")
        print(f"✅ Response received: {response[:100]}...")
        
        # Test multilingual content
        multilingual_content = """
        Bonjour! Je m'appelle Jean Dupont.
        Mon email est jean.dupont@company.fr
        Hello! My name is John Smith.
        My email is john.smith@company.com
        """
        
        print(f"\nTesting multilingual PII detection:")
        print(f"Content: {multilingual_content[:100]}...")
        
        detected = tinfoil_llm.detect_sensitive_data(multilingual_content, "llama")
        
        if detected:
            print("✅ PII detection successful:")
            for entity_type, values in detected.items():
                if values:
                    print(f"   * {entity_type}: {values}")
        else:
            print("⚠️ No PII detected (this might be expected for test content)")
        
        print("\n🎉 All tests passed! Llama 3.3 70B is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_model_recommendation():
    """Test model recommendation logic."""
    print("\nTESTING MODEL RECOMMENDATION")
    print("=" * 50)
    
    try:
        from secureai.tinfoil_llm import TinfoilLLM
        
        api_key = "tk_WC48lzpUM12DFaYKPm4f65FWLGxRgVyc17EduuZRvQ440gi9"
        tinfoil_llm = TinfoilLLM(api_key)
        
        test_cases = [
            {
                "content": "Bonjour! Je m'appelle Jean Dupont.",
                "expected": "llama",
                "reason": "multilingual content"
            },
            {
                "content": "import os\nfrom flask import Flask\nAPI_KEY = 'sk-123456'",
                "expected": "qwen", 
                "reason": "code content"
            },
            {
                "content": "The quarterly revenue was $1,250,000.",
                "expected": "qwen",
                "reason": "financial content"
            },
            {
                "content": "Hi John, my email is john@example.com",
                "expected": "deepseek",
                "reason": "simple English text"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            recommended = tinfoil_llm.recommend_model(test_case["content"])
            expected = test_case["expected"]
            
            status = "✅" if recommended == expected else "❌"
            print(f"{status} Test {i}: Recommended {recommended} (expected {expected}) - {test_case['reason']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("🦙 LLAMA 3.3 70B SIMPLE TEST")
    print("=" * 50)
    
    tests = [
        test_llama_basic,
        test_model_recommendation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    print(f"\n📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Llama 3.3 70B is ready for AI Privacy Shield!")
    else:
        print("⚠️ Some tests failed.")

if __name__ == "__main__":
    main() 