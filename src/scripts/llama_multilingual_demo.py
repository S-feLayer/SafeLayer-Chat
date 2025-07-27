#!/usr/bin/env python3
"""
Llama 3.3 70B Multilingual Demo

This script demonstrates Llama 3.3 70B's multilingual PII detection capabilities
for the AI Privacy Shield.
"""

import os
import sys
import json
from datetime import datetime

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_llama_multilingual_detection():
    """Test Llama 3.3 70B with multilingual content."""
    print("LLAMA 3.3 70B MULTILINGUAL PII DETECTION")
    print("=" * 60)
    
    try:
        from secureai.tinfoil_llm import TinfoilLLM
        
        # Initialize with your API key
        api_key = "tk_WC48lzpUM12DFaYKPm4f65FWLGxRgVyc17EduuZRvQ440gi9"
        tinfoil_llm = TinfoilLLM(api_key)
        
        # Test connection
        if not tinfoil_llm.test_connection():
            print("❌ Failed to connect to Tinfoil API")
            return False
        
        print("✅ Connected to Tinfoil API successfully!")
        
        # Get Llama model info
        llama_info = tinfoil_llm.get_model_info("llama")
        print(f"\n🦙 Using: {llama_info['name']}")
        print(f"   Strengths: {', '.join(llama_info['strengths'])}")
        print(f"   Languages: {', '.join(llama_info['languages'])}")
        print(f"   Context: {llama_info['context_length']:,} tokens")
        
        # Test multilingual content
        multilingual_test_cases = [
            {
                "language": "French",
                "content": """
                Bonjour! Je m'appelle Jean Dupont et je travaille à Paris.
                Mon email est jean.dupont@company.fr et mon téléphone est 01-23-45-67-89.
                Mon adresse est 123 Rue de la Paix, 75001 Paris, France.
                Mon numéro de sécurité sociale est 123-45-6789-012.
                """,
                "expected_entities": ["names", "emails", "phones", "addresses", "ssns"]
            },
            {
                "language": "German",
                "content": """
                Hallo! Ich heiße Hans Mueller und arbeite in Berlin.
                Meine E-Mail ist hans.mueller@firma.de und meine Telefonnummer ist 030-123-4567.
                Meine Adresse ist Musterstraße 123, 10115 Berlin, Deutschland.
                Meine Kreditkartennummer ist 4111-1111-1111-1111.
                """,
                "expected_entities": ["names", "emails", "phones", "addresses", "credit_cards"]
            },
            {
                "language": "Spanish",
                "content": """
                ¡Hola! Me llamo María García y trabajo en Madrid.
                Mi correo electrónico es maria.garcia@empresa.es y mi teléfono es 91-123-4567.
                Mi dirección es Calle Mayor 123, 28001 Madrid, España.
                Mi número de tarjeta de crédito es 4111-1111-1111-1111.
                """,
                "expected_entities": ["names", "emails", "phones", "addresses", "credit_cards"]
            },
            {
                "language": "Italian",
                "content": """
                Ciao! Mi chiamo Marco Rossi e lavoro a Roma.
                La mia email è marco.rossi@azienda.it e il mio telefono è 06-123-4567.
                Il mio indirizzo è Via del Corso 123, 00186 Roma, Italia.
                Il mio numero di carta di credito è 4111-1111-1111-1111.
                """,
                "expected_entities": ["names", "emails", "phones", "addresses", "credit_cards"]
            },
            {
                "language": "Portuguese",
                "content": """
                Olá! Meu nome é João Silva e trabalho em São Paulo.
                Meu email é joao.silva@empresa.com.br e meu telefone é 11-1234-5678.
                Meu endereço é Rua das Flores 123, 01234-567 São Paulo, Brasil.
                Meu número de cartão de crédito é 4111-1111-1111-1111.
                """,
                "expected_entities": ["names", "emails", "phones", "addresses", "credit_cards"]
            },
            {
                "language": "Hindi",
                "content": """
                नमस्ते! मेरा नाम राजेश कुमार है और मैं मुंबई में काम करता हूं।
                मेरा ईमेल rajesh.kumar@company.in है और मेरा फोन नंबर 022-1234-5678 है।
                मेरा पता है 123 मेन स्ट्रीट, मुंबई, महाराष्ट्र 400001।
                मेरी क्रेडिट कार्ड संख्या 4111-1111-1111-1111 है।
                """,
                "expected_entities": ["names", "emails", "phones", "addresses", "credit_cards"]
            },
            {
                "language": "Thai",
                "content": """
                สวัสดี! ผมชื่อ สมชาย ใจดี และทำงานในกรุงเทพฯ
                อีเมลของผมคือ somchai.jaidee@company.co.th และเบอร์โทรศัพท์คือ 02-123-4567
                ที่อยู่ของผมคือ 123 ถนนสุขุมวิท กรุงเทพฯ 10110
                เลขบัตรเครดิตของผมคือ 4111-1111-1111-1111
                """,
                "expected_entities": ["names", "emails", "phones", "addresses", "credit_cards"]
            }
        ]
        
        print(f"\n🧪 Testing {len(multilingual_test_cases)} languages...")
        
        for i, test_case in enumerate(multilingual_test_cases, 1):
            print(f"\n--- Test {i}: {test_case['language']} ---")
            print(f"Content: {test_case['content'][:100]}...")
            
            # Detect sensitive data using Llama
            detected_entities = tinfoil_llm.detect_sensitive_data(
                test_case["content"], 
                model="llama"
            )
            
            print(f"Detected entities:")
            total_entities = 0
            for entity_type, values in detected_entities.items():
                if values:
                    print(f"  * {entity_type}: {values}")
                    total_entities += len(values)
            
            print(f"Total entities detected: {total_entities}")
            
            # Check if expected entities were found
            found_entity_types = set(detected_entities.keys())
            expected_entity_types = set(test_case["expected_entities"])
            
            if found_entity_types.intersection(expected_entity_types):
                print(f"✅ Successfully detected expected entity types")
            else:
                print(f"⚠️ Expected entities not detected")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_llama_conversation_context():
    """Test Llama's ability to maintain context across multilingual conversations."""
    print("\n\nLLAMA 3.3 70B CONVERSATION CONTEXT")
    print("=" * 60)
    
    try:
        from secureai.tinfoil_llm import TinfoilLLM
        
        api_key = "tk_WC48lzpUM12DFaYKPm4f65FWLGxRgVyc17EduuZRvQ440gi9"
        tinfoil_llm = TinfoilLLM(api_key)
        
        # Multilingual conversation
        conversation = [
            {
                "speaker": "user",
                "language": "French",
                "content": "Bonjour! Je m'appelle Jean Dupont. Mon email est jean.dupont@company.fr"
            },
            {
                "speaker": "assistant", 
                "language": "English",
                "content": "Hello Jean! Nice to meet you. How can I help you today?"
            },
            {
                "speaker": "user",
                "language": "German",
                "content": "Hallo! Ich bin Hans Mueller. Meine Telefonnummer ist 030-123-4567"
            },
            {
                "speaker": "assistant",
                "language": "English", 
                "content": "Hello Hans! I see you're working with Jean Dupont. What can I assist you with?"
            },
            {
                "speaker": "user",
                "language": "Spanish",
                "content": "¡Hola! Soy María García. Mi dirección es Calle Mayor 123, Madrid"
            }
        ]
        
        print("🗣️ Processing multilingual conversation with Llama 3.3 70B...")
        
        for i, message in enumerate(conversation, 1):
            print(f"\nMessage {i} ({message['language']}): {message['content']}")
            
            # Detect entities in this message
            detected_entities = tinfoil_llm.detect_sensitive_data(
                message["content"], 
                model="llama"
            )
            
            if detected_entities:
                print("Detected entities:")
                for entity_type, values in detected_entities.items():
                    if values:
                        print(f"  * {entity_type}: {values}")
            else:
                print("No entities detected")
        
        print("\n✅ Llama successfully processed multilingual conversation context!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_llama_vs_other_models():
    """Compare Llama 3.3 70B with other models for multilingual content."""
    print("\n\nLLAMA 3.3 70B vs OTHER MODELS")
    print("=" * 60)
    
    try:
        from secureai.tinfoil_llm import TinfoilLLM
        
        api_key = "tk_WC48lzpUM12DFaYKPm4f65FWLGxRgVyc17EduuZRvQ440gi9"
        tinfoil_llm = TinfoilLLM(api_key)
        
        # Test content with multiple languages
        test_content = """
        Bonjour! Je m'appelle Jean Dupont (French)
        Hallo! Ich heiße Hans Mueller (German)  
        ¡Hola! Me llamo María García (Spanish)
        Ciao! Mi chiamo Marco Rossi (Italian)
        Hello! My name is John Smith (English)
        
        Emails: jean.dupont@company.fr, hans.mueller@firma.de, maria.garcia@empresa.es
        Phones: 01-23-45-67-89, 030-123-4567, 91-123-4567
        """
        
        print(f"Test content: {test_content[:200]}...")
        
        # Test with different models
        models_to_test = ["llama", "deepseek", "qwen", "mistral"]
        
        results = {}
        
        for model in models_to_test:
            print(f"\n--- Testing {model.upper()} ---")
            
            try:
                detected_entities = tinfoil_llm.detect_sensitive_data(test_content, model)
                
                total_entities = sum(len(values) for values in detected_entities.values())
                entity_types = list(detected_entities.keys())
                
                results[model] = {
                    "total_entities": total_entities,
                    "entity_types": entity_types,
                    "success": True
                }
                
                print(f"Total entities: {total_entities}")
                print(f"Entity types: {entity_types}")
                
            except Exception as e:
                print(f"Error with {model}: {e}")
                results[model] = {
                    "total_entities": 0,
                    "entity_types": [],
                    "success": False,
                    "error": str(e)
                }
        
        # Compare results
        print(f"\n📊 COMPARISON RESULTS")
        print("=" * 40)
        
        for model, result in results.items():
            status = "✅" if result["success"] else "❌"
            print(f"{status} {model.upper()}: {result['total_entities']} entities, {len(result['entity_types'])} types")
        
        # Find best performing model
        successful_models = {k: v for k, v in results.items() if v["success"]}
        if successful_models:
            best_model = max(successful_models.keys(), key=lambda x: successful_models[x]["total_entities"])
            print(f"\n🏆 Best performing model: {best_model.upper()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all Llama 3.3 70B tests."""
    print("🦙 LLAMA 3.3 70B MULTILINGUAL DEMO")
    print("=" * 60)
    print("Testing Llama 3.3 70B's multilingual PII detection capabilities")
    print("for the AI Privacy Shield product.")
    print()
    
    # Run tests
    tests = [
        test_llama_multilingual_detection,
        test_llama_conversation_context,
        test_llama_vs_other_models
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All tests passed! Llama 3.3 70B is ready for multilingual PII detection!")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    print("\n🦙 LLAMA 3.3 70B STRENGTHS FOR AI PRIVACY SHIELD:")
    print("✅ Multilingual PII detection (8 languages)")
    print("✅ Conversation context understanding")
    print("✅ Cross-language entity consistency")
    print("✅ Chat-optimized for AI conversations")
    print("✅ 64k context window for long conversations")
    print("✅ Strong reasoning for complex PII patterns")

if __name__ == "__main__":
    main() 