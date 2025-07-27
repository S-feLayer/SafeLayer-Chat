#!/usr/bin/env python3
"""
Simple Secure AI Chat Demo - Show How PII Protection Works in Chats

This demo shows the concept of how Secure AI works in chat conversations
without requiring the full installation. It demonstrates:
- Real-time redaction of user messages
- Entity persistence across conversations
- Different masking strategies
"""

import re
import time
from datetime import datetime
from typing import Dict, List, Any

class SimpleSecureAI:
    """Simplified version of Secure AI for demonstration."""
    
    def __init__(self):
        # Detection patterns
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[-.\s]?\d{4}[-.\s]?\d{4}[-.\s]?\d{4}\b',
            'api_key': r'\b(sk-|pk-|ghp_|gho_|ghu_|ghs_|ghr_)[a-zA-Z0-9]{20,}\b',
            'name': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Simple name detection
        }
        
        # Entity persistence storage
        self.entity_mappings = {}
        self.entity_counter = 1
    
    def detect_entities(self, text: str) -> List[Dict[str, Any]]:
        """Detect sensitive entities in text."""
        entities = []
        
        for entity_type, pattern in self.patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    'type': entity_type,
                    'value': match,
                    'confidence': 0.9
                })
        
        return entities
    
    def get_or_create_mapping(self, entity_type: str, value: str) -> str:
        """Get existing mapping or create new one for entity persistence."""
        key = f"{entity_type}:{value.lower()}"
        
        if key not in self.entity_mappings:
            if entity_type == 'name':
                masked_value = f"Person {chr(64 + self.entity_counter)}"  # Person A, Person B, etc.
            elif entity_type == 'email':
                username, domain = value.split('@')
                masked_value = f"{username[:2]}**@{domain[:2]}**@{domain.split('.')[-1]}"
            elif entity_type == 'phone':
                digits = re.sub(r'\D', '', value)
                masked_value = f"{digits[:2]}**-**-{digits[-4:]}"
            elif entity_type == 'ssn':
                masked_value = "***-**-****"
            elif entity_type == 'credit_card':
                masked_value = f"****-****-****-{value[-4:]}"
            elif entity_type == 'api_key':
                masked_value = f"{value[:4]}**********{value[-4:]}"
            else:
                masked_value = f"[{entity_type.upper()}]"
            
            self.entity_mappings[key] = masked_value
            self.entity_counter += 1
        
        return self.entity_mappings[key]
    
    def redact_content(self, content: str) -> Dict[str, Any]:
        """Redact sensitive content and return results."""
        entities = self.detect_entities(content)
        redacted_content = content
        
        # Sort entities by length (longest first) to avoid partial replacements
        entities.sort(key=lambda x: len(x['value']), reverse=True)
        
        for entity in entities:
            original_value = entity['value']
            masked_value = self.get_or_create_mapping(entity['type'], original_value)
            redacted_content = redacted_content.replace(original_value, masked_value)
        
        return {
            'original_content': content,
            'redacted_content': redacted_content,
            'detected_entities': entities,
            'entity_mappings': self.entity_mappings.copy()
        }

class MockLLM:
    """Mock LLM for demonstration."""
    
    def generate_response(self, message: str) -> str:
        """Generate a contextual response."""
        if "hello" in message.lower() or "hi" in message.lower():
            return "Hello! I'm here to help you. How can I assist you today?"
        elif "email" in message.lower():
            return "I can help you with email-related questions. What specific issue are you experiencing?"
        elif "phone" in message.lower():
            return "I can assist with phone-related inquiries. Please provide more details."
        elif "project" in message.lower():
            return "I'd be happy to help with your project. What kind of project are you working on?"
        elif "client" in message.lower():
            return "I can help you manage client relationships. What specific client issue do you need assistance with?"
        elif "api" in message.lower():
            return "I can help you with API integration and troubleshooting. What API are you working with?"
        else:
            return "I understand your message. How can I help you further with this?"

class SimpleChatDemo:
    """Simple chat demonstration."""
    
    def __init__(self):
        self.secure_ai = SimpleSecureAI()
        self.llm = MockLLM()
        self.session_id = f"demo_{int(time.time())}"
    
    def chat_round(self, user_message: str) -> Dict[str, str]:
        """Complete chat round with protection."""
        print(f"\n{'='*60}")
        print(f"💬 CHAT ROUND - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}")
        
        # Original user message
        print(f"👤 USER (Original): {user_message}")
        
        # Process through Secure AI
        print(f"\n🔒 Processing through Secure AI...")
        result = self.secure_ai.redact_content(user_message)
        
        print(f"📊 Detected {len(result['detected_entities'])} sensitive entities")
        if result['detected_entities']:
            print("🔍 Detected entities:")
            for entity in result['detected_entities']:
                print(f"   • {entity['type']}: {entity['value']}")
        
        protected_message = result['redacted_content']
        print(f"👤 USER (Protected): {protected_message}")
        
        # Send to LLM
        print(f"\n🤖 Sending to LLM...")
        llm_response = self.llm.generate_response(protected_message)
        print(f"🤖 LLM Response: {llm_response}")
        
        return {
            "user_original": user_message,
            "user_protected": protected_message,
            "llm_response": llm_response
        }
    
    def run_customer_service_demo(self):
        """Customer service scenario."""
        print(f"\n🏢 CUSTOMER SERVICE DEMO")
        print(f"{'='*60}")
        
        messages = [
            "Hi, I'm John Smith and I need help with my account. My email is john.smith@acme.com and my phone number is 555-123-4567.",
            "I'm having trouble with my credit card ending in 1234. The card number is 4111-1111-1111-1234.",
            "Can you help me reset my password? My username is johnsmith and my SSN is 123-45-6789.",
            "I live at 123 Main Street, New York, NY 10001. Can you update my address?",
            "Thanks for your help! My account number is ACC-789-456-123."
        ]
        
        for i, message in enumerate(messages, 1):
            print(f"\n📝 Message {i}/{len(messages)}")
            self.chat_round(message)
            
            if i < len(messages):
                input("\n⏸️ Press Enter to continue...")
    
    def run_technical_demo(self):
        """Technical support scenario."""
        print(f"\n💻 TECHNICAL SUPPORT DEMO")
        print(f"{'='*60}")
        
        messages = [
            "Hi, I'm debugging an API issue. My API key is sk-1234567890abcdef and the endpoint is https://api.acme.com/v1/users.",
            "The database connection string is postgresql://user:password123@localhost:5432/acme_db. I think there's an authentication problem.",
            "I'm working with our client Sarah Johnson from TechStart Inc. Her email is sarah.j@techstart.com.",
            "The project budget is $50,000 and we need to deliver by March 15th. Can you help me optimize the database queries?",
            "I'm using AWS and my access key is AKIA1234567890ABCDEF. The secret key is wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY."
        ]
        
        for i, message in enumerate(messages, 1):
            print(f"\n📝 Message {i}/{len(messages)}")
            self.chat_round(message)
            
            if i < len(messages):
                input("\n⏸️ Press Enter to continue...")
    
    def run_healthcare_demo(self):
        """Healthcare scenario with PHI protection."""
        print(f"\n🏥 HEALTHCARE DEMO (PHI Protection)")
        print(f"{'='*60}")
        
        messages = [
            "Patient John Doe, DOB 1985-03-15, SSN 123-45-6789, has been experiencing chest pain for the past week.",
            "The patient's phone number is 555-987-6543 and email is john.doe@email.com. They live at 456 Oak Street, Boston, MA 02101.",
            "Medical record number is MR-789-456-123. The patient has a history of hypertension and diabetes.",
            "Insurance provider is Blue Cross Blue Shield, policy number BCBS-123456789. Coverage expires 12/31/2024.",
            "The patient's emergency contact is Jane Doe, phone 555-111-2222, relationship: spouse."
        ]
        
        for i, message in enumerate(messages, 1):
            print(f"\n📝 Message {i}/{len(messages)}")
            self.chat_round(message)
            
            if i < len(messages):
                input("\n⏸️ Press Enter to continue...")
    
    def run_interactive_demo(self):
        """Interactive demo where user types messages."""
        print(f"\n🎮 INTERACTIVE DEMO")
        print(f"{'='*60}")
        print("Type your messages and see Secure AI in action!")
        print("Type 'quit' to exit.")
        print(f"{'='*60}")
        
        message_count = 0
        while True:
            message_count += 1
            user_input = input(f"\n👤 Message {message_count}: ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not user_input.strip():
                continue
            
            self.chat_round(user_input)
    
    def show_entity_persistence(self):
        """Show how entity persistence works."""
        print(f"\n🔄 ENTITY PERSISTENCE DEMONSTRATION")
        print(f"{'='*60}")
        
        messages = [
            "Hi, I'm John Smith.",
            "Can you help John Smith with the project?",
            "John Smith's email is john@acme.com.",
            "I also need to contact Sarah Johnson.",
            "Sarah Johnson works with John Smith.",
            "Both John Smith and Sarah Johnson are on the team."
        ]
        
        print("Notice how 'John Smith' and 'Sarah Johnson' get consistent masking!")
        print()
        
        for i, message in enumerate(messages, 1):
            print(f"📝 Message {i}: {message}")
            result = self.secure_ai.redact_content(message)
            print(f"🔒 Redacted: {result['redacted_content']}")
            print("-" * 40)
            
            if i < len(messages):
                input("Press Enter to continue...")
    
    def show_demo_menu(self):
        """Show demo menu."""
        while True:
            print(f"\n🔒 SIMPLE SECURE AI CHAT DEMO")
            print(f"{'='*40}")
            print("1. Customer Service Demo")
            print("2. Technical Support Demo")
            print("3. Healthcare Demo (PHI Protection)")
            print("4. Entity Persistence Demo")
            print("5. Interactive Demo (Type your own messages)")
            print("6. Exit")
            print(f"{'='*40}")
            
            choice = input("Select a demo (1-6): ").strip()
            
            if choice == "1":
                self.run_customer_service_demo()
            elif choice == "2":
                self.run_technical_demo()
            elif choice == "3":
                self.run_healthcare_demo()
            elif choice == "4":
                self.show_entity_persistence()
            elif choice == "5":
                self.run_interactive_demo()
            elif choice == "6":
                print("👋 Thanks for trying the demo!")
                break
            else:
                print("❌ Invalid choice. Please select 1-6.")
            
            input("\n⏸️ Press Enter to return to menu...")

def main():
    """Main function."""
    print("🔒 Simple Secure AI Chat Demo")
    print("Real-time PII Protection for LLM Chats")
    print("=" * 50)
    
    demo = SimpleChatDemo()
    demo.show_demo_menu()

if __name__ == "__main__":
    main() 