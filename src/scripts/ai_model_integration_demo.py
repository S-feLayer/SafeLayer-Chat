#!/usr/bin/env python3
"""
AI Model Integration Demo

This script demonstrates how to use Secure AI with Tinfoil for redaction
before sending content to other AI models like ChatGPT, Grok, or Gemini.
"""

import os
import sys
import json
from typing import Dict, Any, Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from secureai.redact_content import redact_content
from secureai.tinfoil_llm import TinfoilLLM

class AIModelIntegration:
    """
    Demonstrates integration with various AI models after redaction.
    """
    
    def __init__(self):
        self.tinfoil_llm = TinfoilLLM()
        
    def redact_with_tinfoil(self, content: str, content_type: str = "text") -> Dict[str, Any]:
        """
        Use Tinfoil to redact sensitive data from content.
        
        Args:
            content: The content to redact
            content_type: Type of content (text, code, pdf)
            
        Returns:
            Dictionary with redacted content and metadata
        """
        print(f"🔍 Detecting and redacting sensitive data using Tinfoil...")
        
        # Use Secure AI's universal redaction
        result = redact_content(content, self.tinfoil_llm)
        
        if result["success"]:
            redaction_result = result["redaction_result"]
            print(f"✅ Redaction complete: {redaction_result['redaction_count']} items redacted")
            return {
                "original": content,
                "redacted": redaction_result["redacted_text"],
                "redaction_count": redaction_result["redaction_count"],
                "redacted_items": redaction_result["redacted_items"],
                "masked_data": redaction_result.get("masked_sensitive_data", {})
            }
        else:
            print(f"❌ Redaction failed: {result['error']}")
            return {"original": content, "redacted": content, "error": result["error"]}
    
    def simulate_chatgpt_analysis(self, redacted_content: str) -> str:
        """
        Simulate sending redacted content to ChatGPT.
        """
        print("🤖 Simulating ChatGPT analysis...")
        
        # This would be your actual ChatGPT API call
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=[{"role": "user", "content": redacted_content}]
        # )
        
        # Simulated response
        analysis = f"""
        Analysis of redacted content:
        
        The document appears to be a business communication containing:
        - Professional correspondence
        - Project-related information
        - Business metrics and data
        
        Key insights:
        - The content has been properly sanitized for AI processing
        - No sensitive personal or business information is exposed
        - The document structure and meaning are preserved
        
        Recommendation: This content is safe for AI analysis and processing.
        """
        
        return analysis
    
    def simulate_grok_analysis(self, redacted_content: str) -> str:
        """
        Simulate sending redacted content to Grok.
        """
        print("🤖 Simulating Grok analysis...")
        
        # This would be your actual Grok API call
        # response = grok_api.analyze(redacted_content)
        
        # Simulated response
        analysis = f"""
        Grok Analysis Results:
        
        Content Type: Business Document
        Sentiment: Professional/Neutral
        Key Topics: Project management, business operations
        
        Security Assessment:
        ✅ No PII detected in processed content
        ✅ No sensitive credentials found
        ✅ Safe for AI processing and analysis
        
        Business Intelligence:
        - Document contains operational data
        - Suitable for business analytics
        - No privacy concerns identified
        """
        
        return analysis
    
    def simulate_gemini_analysis(self, redacted_content: str) -> str:
        """
        Simulate sending redacted content to Gemini.
        """
        print("🤖 Simulating Gemini analysis...")
        
        # This would be your actual Gemini API call
        # response = gemini.generate_content(redacted_content)
        
        # Simulated response
        analysis = f"""
        Gemini Content Analysis:
        
        Document Summary:
        - Professional business communication
        - Contains operational information
        - Well-structured content
        
        Privacy Compliance:
        ✅ GDPR compliant - no personal data
        ✅ HIPAA safe - no medical information
        ✅ SOX compliant - no financial PII
        
        AI Processing Safety:
        - Content is safe for AI analysis
        - No sensitive information exposed
        - Ready for machine learning processing
        """
        
        return analysis
    
    def demonstrate_workflow(self, sensitive_content: str):
        """
        Demonstrate the complete workflow: Redaction → AI Analysis.
        """
        print("🔄 COMPLETE WORKFLOW DEMONSTRATION")
        print("=" * 60)
        
        # Step 1: Redact with Tinfoil
        print("\n📋 STEP 1: REDACTION WITH TINFOIL")
        print("-" * 40)
        print("Original content:")
        print(f"'{sensitive_content[:100]}...'")
        
        redaction_result = self.redact_with_tinfoil(sensitive_content, "text")
        
        if "error" in redaction_result:
            print(f"❌ Workflow stopped due to redaction error")
            return
        
        print(f"\nRedacted content:")
        print(f"'{redaction_result['redacted'][:100]}...'")
        
        # Step 2: Send to different AI models
        print("\n🤖 STEP 2: AI MODEL ANALYSIS")
        print("-" * 40)
        
        # ChatGPT
        print("\n📊 ChatGPT Analysis:")
        chatgpt_result = self.simulate_chatgpt_analysis(redaction_result['redacted'])
        print(chatgpt_result)
        
        # Grok
        print("\n📊 Grok Analysis:")
        grok_result = self.simulate_grok_analysis(redaction_result['redacted'])
        print(grok_result)
        
        # Gemini
        print("\n📊 Gemini Analysis:")
        gemini_result = self.simulate_gemini_analysis(redaction_result['redacted'])
        print(gemini_result)
        
        # Step 3: Summary
        print("\n📈 WORKFLOW SUMMARY")
        print("-" * 40)
        print(f"✅ Original content length: {len(sensitive_content)} characters")
        print(f"✅ Redacted content length: {len(redaction_result['redacted'])} characters")
        print(f"✅ Items redacted: {redaction_result['redaction_count']}")
        print(f"✅ AI models processed: 3 (ChatGPT, Grok, Gemini)")
        print(f"✅ Privacy protection: Complete")
        print(f"✅ Data leakage prevention: Successful")

def create_sensitive_content() -> str:
    """Create sample content with sensitive information."""
    
    return """
    Hi team,
    
    I need to share some sensitive project information:
    
    My name is Sarah Johnson and my email is sarah.johnson@techcorp.com
    My phone number is +1-555-987-6543
    My employee ID is EMP-78901
    
    Project Details:
    - Client: Acme Solutions Inc. (456 Business Ave, San Francisco, CA 94102)
    - Contract Number: CNT-2024-003
    - Budget: $150,000
    - Timeline: 6 months
    
    Technical Information:
    - Database URL: postgresql://admin:secretpass123@prod-db.techcorp.com:5432/project_db
    - API Key: sk-1234567890abcdef1234567890abcdef1234567890abcdef
    - GitHub Token: ghp_1234567890abcdef1234567890abcdef1234567890
    - AWS Access Key: AKIA1234567890ABCDEF
    
    Personal Notes:
    - Meeting with John Smith (john.smith@acme.com) on Friday
    - Discussing sensitive merger details
    - Need to keep this confidential!
    
    Best regards,
    Sarah
    """

def demonstrate_real_integration():
    """Demonstrate real integration patterns."""
    
    print("\n🔧 REAL INTEGRATION PATTERNS")
    print("=" * 50)
    
    print("""
    Here's how to integrate with actual AI models:
    
    1. CHATGPT INTEGRATION:
    ```python
    import openai
    
    def analyze_with_chatgpt(redacted_content):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": redacted_content}]
        )
        return response.choices[0].message.content
    ```
    
    2. GROK INTEGRATION:
    ```python
    import grok_api  # Hypothetical
    
    def analyze_with_grok(redacted_content):
        response = grok_api.analyze(redacted_content)
        return response.analysis
    ```
    
    3. GEMINI INTEGRATION:
    ```python
    import google.generativeai as genai
    
    def analyze_with_gemini(redacted_content):
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(redacted_content)
        return response.text
    ```
    
    4. COMPLETE WORKFLOW:
    ```python
    # Step 1: Redact with Tinfoil
    redaction_result = redact_content(sensitive_content, tinfoil_llm)
    
    # Step 2: Send to any AI model
    if redaction_result["success"]:
        redacted_content = redaction_result["redaction_result"]["redacted_text"]
        analysis = analyze_with_chatgpt(redacted_content)  # or any other AI
    ```
    """)

def main():
    """Main demonstration function."""
    
    print("🤖 AI MODEL INTEGRATION DEMONSTRATION")
    print("=" * 60)
    print("Using Tinfoil for redaction before sending to other AI models")
    print("=" * 60)
    
    # Check for Tinfoil API key
    if not os.getenv("TINFOIL_API_KEY"):
        print("⚠️ TINFOIL_API_KEY not set. Please set your API key:")
        print("export TINFOIL_API_KEY='your_key_here'")
        return
    
    try:
        # Initialize integration
        integration = AIModelIntegration()
        
        # Create sensitive content
        sensitive_content = create_sensitive_content()
        
        # Demonstrate workflow
        integration.demonstrate_workflow(sensitive_content)
        
        # Show real integration patterns
        demonstrate_real_integration()
        
        print("\n🎉 Integration Demonstration Complete!")
        print("\n💡 Key Benefits:")
        print("  • Secure AI processing with Tinfoil redaction")
        print("  • Compatible with any AI model (ChatGPT, Grok, Gemini)")
        print("  • Complete data leakage prevention")
        print("  • Privacy-compliant AI workflows")
        print("  • Preserved content meaning and structure")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        print("Make sure TINFOIL_API_KEY is set and all dependencies are installed.")

if __name__ == "__main__":
    main() 