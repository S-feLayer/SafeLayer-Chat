#!/usr/bin/env python3
"""
Secure AI Chat Demo - Real-time PII Protection for LLM Chats

This demo shows how Secure AI works in chat conversations:
- Real-time redaction of user messages before sending to LLM
- Real-time redaction of LLM responses before sending to user
- Entity persistence across the entire conversation
- Different chat scenarios (customer service, technical support, healthcare)
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class MockLLM:
    """Mock LLM for demonstration purposes."""
    
    def __init__(self):
        self.conversation_history = []
    
    def generate_response(self, message: str) -> str:
        """Generate a mock response based on the input."""
        self.conversation_history.append({"role": "user", "content": message})
        
        # Simple response logic for demo
        if "hello" in message.lower() or "hi" in message.lower():
            response = "Hello! I'm here to help you. How can I assist you today?"
        elif "email" in message.lower():
            response = "I can help you with email-related questions. What specific issue are you experiencing?"
        elif "phone" in message.lower():
            response = "I can assist with phone-related inquiries. Please provide more details about your concern."
        elif "project" in message.lower():
            response = "I'd be happy to help with your project. What kind of project are you working on?"
        elif "client" in message.lower():
            response = "I can help you manage client relationships. What specific client issue do you need assistance with?"
        elif "budget" in message.lower():
            response = "I can help you with budget planning and management. What's your budget range and requirements?"
        elif "api" in message.lower():
            response = "I can help you with API integration and troubleshooting. What API are you working with?"
        elif "database" in message.lower():
            response = "I can assist with database-related questions. What database system are you using?"
        else:
            response = "I understand your message. How can I help you further with this?"
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

class SecureAIChatDemo:
    """Demonstration of Secure AI in chat conversations."""
    
    def __init__(self):
        self.llm = MockLLM()
        self.session_id = f"demo_session_{int(time.time())}"
        self.user_id = "demo_user_123"
        self.organization_id = "demo_org_456"
        
        # Initialize Secure AI Shield
        try:
            from secure_AI.ai_privacy_shield import AIPrivacyShield
            self.shield = AIPrivacyShield(enable_persistence=False)  # No Redis/PostgreSQL for demo
            print("✅ Secure AI Shield initialized successfully!")
        except ImportError as e:
            print(f"❌ Error importing Secure AI: {e}")
            print("💡 Make sure you're in the correct directory and dependencies are installed")
            self.shield = None
        except Exception as e:
            print(f"❌ Error initializing Secure AI: {e}")
            self.shield = None
    
    def process_user_message(self, message: str) -> str:
        """Process user message through Secure AI before sending to LLM."""
        if not self.shield:
            return message
        
        print(f"\n🔒 Processing user message through Secure AI...")
        
        # Redact sensitive information
        result = self.shield.redact_content(
            content=message,
            content_type="text",
            session_id=self.session_id,
            user_id=self.user_id,
            organization_id=self.organization_id
        )
        
        print(f"📊 Detected {len(result.detected_entities)} sensitive entities")
        if result.detected_entities:
            print("🔍 Detected entities:")
            for entity in result.detected_entities:
                print(f"   • {entity['type']}: {entity['value']}")
        
        return result.redacted_content
    
    def process_llm_response(self, response: str) -> str:
        """Process LLM response through Secure AI before sending to user."""
        if not self.shield:
            return response
        
        print(f"\n🔒 Processing LLM response through Secure AI...")
        
        # Redact any sensitive information in the response
        result = self.shield.redact_content(
            content=response,
            content_type="text",
            session_id=self.session_id,
            user_id=self.user_id,
            organization_id=self.organization_id
        )
        
        if result.detected_entities:
            print(f"📊 Detected {len(result.detected_entities)} sensitive entities in response")
        
        return result.redacted_content
    
    def chat_round(self, user_message: str) -> Dict[str, str]:
        """Complete chat round with Secure AI protection."""
        print(f"\n{'='*60}")
        print(f"💬 CHAT ROUND - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}")
        
        # Original user message
        print(f"👤 USER (Original): {user_message}")
        
        # Process user message through Secure AI
        protected_user_message = self.process_user_message(user_message)
        print(f"👤 USER (Protected): {protected_user_message}")
        
        # Send to LLM
        print(f"\n🤖 Sending to LLM...")
        llm_response = self.llm.generate_response(protected_user_message)
        print(f"🤖 LLM (Original): {llm_response}")
        
        # Process LLM response through Secure AI
        protected_llm_response = self.process_llm_response(llm_response)
        print(f"🤖 LLM (Protected): {protected_llm_response}")
        
        return {
            "user_original": user_message,
            "user_protected": protected_user_message,
            "llm_original": llm_response,
            "llm_protected": protected_llm_response
        }
    
    def run_customer_service_demo(self):
        """Demonstrate customer service chat scenario."""
        print(f"\n🏢 CUSTOMER SERVICE CHAT DEMO")
        print(f"{'='*60}")
        
        messages = [
            "Hi, I'm John Smith and I need help with my account. My email is john.smith@acme.com and my phone number is 555-123-4567.",
            "I'm having trouble with my credit card ending in 1234. The card number is 4111-1111-1111-1234.",
            "Can you help me reset my password? My username is johnsmith and my SSN is 123-45-6789.",
            "I live at 123 Main Street, New York, NY 10001. Can you update my address?",
            "Thanks for your help! My account number is ACC-789-456-123."
        ]
        
        conversation_history = []
        
        for i, message in enumerate(messages, 1):
            print(f"\n📝 Message {i}/{len(messages)}")
            result = self.chat_round(message)
            conversation_history.append(result)
            
            if i < len(messages):
                input("\n⏸️ Press Enter to continue to next message...")
        
        return conversation_history
    
    def run_technical_support_demo(self):
        """Demonstrate technical support chat scenario."""
        print(f"\n💻 TECHNICAL SUPPORT CHAT DEMO")
        print(f"{'='*60}")
        
        messages = [
            "Hi, I'm debugging an API issue. My API key is sk-1234567890abcdef and the endpoint is https://api.acme.com/v1/users.",
            "The database connection string is postgresql://user:password123@localhost:5432/acme_db. I think there's an authentication problem.",
            "I'm working with our client Sarah Johnson from TechStart Inc. Her email is sarah.j@techstart.com.",
            "The project budget is $50,000 and we need to deliver by March 15th. Can you help me optimize the database queries?",
            "I'm using AWS and my access key is AKIA1234567890ABCDEF. The secret key is wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY."
        ]
        
        conversation_history = []
        
        for i, message in enumerate(messages, 1):
            print(f"\n📝 Message {i}/{len(messages)}")
            result = self.chat_round(message)
            conversation_history.append(result)
            
            if i < len(messages):
                input("\n⏸️ Press Enter to continue to next message...")
        
        return conversation_history
    
    def run_healthcare_demo(self):
        """Demonstrate healthcare chat scenario with PHI protection."""
        print(f"\n🏥 HEALTHCARE CHAT DEMO (PHI Protection)")
        print(f"{'='*60}")
        
        messages = [
            "Patient John Doe, DOB 1985-03-15, SSN 123-45-6789, has been experiencing chest pain for the past week.",
            "The patient's phone number is 555-987-6543 and email is john.doe@email.com. They live at 456 Oak Street, Boston, MA 02101.",
            "Medical record number is MR-789-456-123. The patient has a history of hypertension and diabetes.",
            "Insurance provider is Blue Cross Blue Shield, policy number BCBS-123456789. Coverage expires 12/31/2024.",
            "The patient's emergency contact is Jane Doe, phone 555-111-2222, relationship: spouse."
        ]
        
        conversation_history = []
        
        for i, message in enumerate(messages, 1):
            print(f"\n📝 Message {i}/{len(messages)}")
            result = self.chat_round(message)
            conversation_history.append(result)
            
            if i < len(messages):
                input("\n⏸️ Press Enter to continue to next message...")
        
        return conversation_history
    
    def run_interactive_demo(self):
        """Run an interactive chat demo where user can type messages."""
        print(f"\n🎮 INTERACTIVE CHAT DEMO")
        print(f"{'='*60}")
        print("Type your messages and see Secure AI in action!")
        print("Type 'quit' to exit the demo.")
        print(f"{'='*60}")
        
        conversation_history = []
        message_count = 0
        
        while True:
            message_count += 1
            user_input = input(f"\n👤 Message {message_count}: ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not user_input.strip():
                continue
            
            result = self.chat_round(user_input)
            conversation_history.append(result)
        
        return conversation_history
    
    def show_demo_menu(self):
        """Show demo menu and handle user selection."""
        while True:
            print(f"\n🔒 SECURE AI CHAT DEMO")
            print(f"{'='*40}")
            print("1. Customer Service Demo")
            print("2. Technical Support Demo") 
            print("3. Healthcare Demo (PHI Protection)")
            print("4. Interactive Demo (Type your own messages)")
            print("5. Exit")
            print(f"{'='*40}")
            
            choice = input("Select a demo (1-5): ").strip()
            
            if choice == "1":
                self.run_customer_service_demo()
            elif choice == "2":
                self.run_technical_support_demo()
            elif choice == "3":
                self.run_healthcare_demo()
            elif choice == "4":
                self.run_interactive_demo()
            elif choice == "5":
                print("👋 Thanks for trying Secure AI Chat Demo!")
                break
            else:
                print("❌ Invalid choice. Please select 1-5.")
            
            input("\n⏸️ Press Enter to return to menu...")

def main():
    """Main function to run the chat demo."""
    print("🔒 Secure AI Chat Demo")
    print("Real-time PII Protection for LLM Chats")
    print("=" * 50)
    
    demo = SecureAIChatDemo()
    
    if demo.shield:
        demo.show_demo_menu()
    else:
        print("\n❌ Secure AI Shield not available.")
        print("💡 Please check your installation and dependencies.")

if __name__ == "__main__":
    main() 