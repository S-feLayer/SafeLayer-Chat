#!/usr/bin/env python3
"""
Tinfoil LLM Integration

This module provides integration with Tinfoil AI models for redaction tasks.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from tinfoil import TinfoilAI

logger = logging.getLogger(__name__)

class TinfoilLLM:
    """
    Tinfoil LLM client for redaction tasks.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("TINFOIL_API_KEY")
        if not self.api_key:
            raise ValueError("Tinfoil API key is required. Set TINFOIL_API_KEY environment variable or pass api_key parameter.")
        
        self.client = TinfoilAI(api_key=self.api_key)
        
        # Available models and their characteristics
        self.available_models = {
            "deepseek": {
                "name": "DeepSeek R1 70B",
                "model_id": "deepseek-r1-70b",
                "strengths": ["reasoning", "context_understanding", "pattern_detection"],
                "best_for": ["general_redaction", "complex_documents", "mixed_content"],
                "context_length": 64000,
                "languages": ["English"]
            },
            "llama": {
                "name": "Llama 3.3 70B",
                "model_id": "llama3-3-70b",
                "strengths": ["multilingual", "reasoning", "chat_optimized"],
                "best_for": ["multilingual_content", "international_documents", "conversational_text"],
                "context_length": 64000,
                "languages": ["English", "German", "French", "Italian", "Portuguese", "Hindi", "Spanish", "Thai"]
            },
            "qwen": {
                "name": "Qwen 2.5 72B",
                "model_id": "qwen2-5-72b",
                "strengths": ["programming", "mathematical_reasoning", "long_context"],
                "best_for": ["code_files", "technical_documents", "financial_documents", "long_documents"],
                "context_length": 128000,
                "languages": ["English", "Chinese"]
            },
            "mistral": {
                "name": "Mistral Small 3.1 24B",
                "model_id": "mistral-small-3-1",
                "strengths": ["efficiency", "cost_effective", "fast_processing"],
                "best_for": ["simple_redaction", "budget_constrained", "high_volume"],
                "context_length": 128000,
                "languages": ["English", "French", "German", "Italian", "Spanish"]
            }
        }
    
    def get_tinfoil_response(self, prompt: str, model: str = "deepseek") -> str:
        """
        Get response from Tinfoil LLM.
        
        Args:
            prompt: The prompt to send to the model
            model: Model to use (deepseek, llama, qwen, mistral)
        
        Returns:
            Model response as string
        """
        try:
            # Validate model
            if model not in self.available_models:
                raise ValueError(f"Unknown model: {model}. Available models: {list(self.available_models.keys())}")
            
            model_info = self.available_models[model]
            model_id = model_info["model_id"]
            
            logger.info(f"Using {model_info['name']} for redaction task")
            
            # Create chat completion
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=model_id,
                temperature=0.1,  # Low temperature for consistent results
                max_tokens=4000   # Reasonable limit for redaction tasks
            )
            
            response = chat_completion.choices[0].message.content
            logger.info(f"Received response from {model_info['name']}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting response from Tinfoil: {e}")
            raise
    
    def detect_sensitive_data(self, content: str, model: str = "deepseek") -> Dict[str, List[str]]:
        """
        Detect sensitive data in content using Tinfoil LLM.
        
        Args:
            content: Content to analyze
            model: Model to use for detection
        
        Returns:
            Dictionary mapping entity types to detected values
        """
        prompt = f"""
        Analyze the following content and identify all personally identifiable information (PII) and sensitive data.
        
        Content to analyze:
        {content}
        
        Please identify and extract the following types of sensitive information:
        1. Names (full names, first names, last names)
        2. Email addresses
        3. Phone numbers
        4. Social Security Numbers (SSN)
        5. Credit card numbers
        6. API keys and tokens
        7. Passwords and credentials
        8. Addresses
        9. Dates of birth
        10. Financial information (account numbers, routing numbers)
        11. Medical information
        12. Any other personally identifiable information
        
        Return your response as a JSON object with the following format:
        {{
            "names": ["list of names"],
            "emails": ["list of email addresses"],
            "phones": ["list of phone numbers"],
            "ssns": ["list of SSNs"],
            "credit_cards": ["list of credit card numbers"],
            "api_keys": ["list of API keys"],
            "passwords": ["list of passwords"],
            "addresses": ["list of addresses"],
            "dates_of_birth": ["list of dates of birth"],
            "financial": ["list of financial information"],
            "medical": ["list of medical information"],
            "other": ["list of other PII"]
        }}
        
        Only include categories that have detected values. If no sensitive data is found, return an empty JSON object {{}}.
        """
        
        try:
            response = self.get_tinfoil_response(prompt, model)
            
            # Parse JSON response
            try:
                detected_data = json.loads(response)
                logger.info(f"Detected {sum(len(v) for v in detected_data.values())} sensitive entities")
                return detected_data
            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON response, attempting to extract manually")
                return self._extract_entities_manually(response)
                
        except Exception as e:
            logger.error(f"Error detecting sensitive data: {e}")
            return {}
    
    def _extract_entities_manually(self, response: str) -> Dict[str, List[str]]:
        """
        Manually extract entities from non-JSON response.
        """
        # This is a fallback method if JSON parsing fails
        entities = {}
        
        # Simple pattern matching for common entity types
        import re
        
        # Extract emails
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response)
        if emails:
            entities["emails"] = emails
        
        # Extract phone numbers
        phones = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', response)
        if phones:
            entities["phones"] = phones
        
        # Extract names (simple pattern)
        names = re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', response)
        if names:
            entities["names"] = names
        
        return entities
    
    def get_model_info(self, model: str) -> Dict[str, Any]:
        """
        Get information about a specific model.
        
        Args:
            model: Model identifier
        
        Returns:
            Model information dictionary
        """
        if model not in self.available_models:
            raise ValueError(f"Unknown model: {model}")
        
        return self.available_models[model]
    
    def list_available_models(self) -> Dict[str, Dict[str, Any]]:
        """
        List all available models and their characteristics.
        
        Returns:
            Dictionary of available models
        """
        return self.available_models
    
    def recommend_model(self, content: str, content_type: str = "text") -> str:
        """
        Recommend the best model for a given content type.
        
        Args:
            content: Content to analyze
            content_type: Type of content (text, code, multilingual, etc.)
        
        Returns:
            Recommended model identifier
        """
        # Check for multilingual content
        non_english_chars = len([c for c in content if ord(c) > 127])
        if non_english_chars > len(content) * 0.1:  # More than 10% non-ASCII
            return "llama"  # Llama 3.3 70B for multilingual
        
        # Check for code content
        if content_type == "code" or any(keyword in content.lower() for keyword in ["import ", "def ", "function ", "class ", "api_key", "password"]):
            return "qwen"  # Qwen 2.5 72B for code and technical content
        
        # Check for financial content
        if any(keyword in content.lower() for keyword in ["$", "revenue", "budget", "profit", "account", "bank"]):
            return "qwen"  # Qwen 2.5 72B for financial content
        
        # Default to DeepSeek for general content
        return "deepseek"
    
    def test_connection(self) -> bool:
        """
        Test the connection to Tinfoil API.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            response = self.get_tinfoil_response("Hello, this is a test message.", "deepseek")
            return len(response) > 0
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

# Example usage
if __name__ == "__main__":
    # Initialize with API key
    api_key = "tk_WC48lzpUM12DFaYKPm4f65FWLGxRgVyc17EduuZRvQ440gi9"
    tinfoil_llm = TinfoilLLM(api_key)
    
    # Test connection
    if tinfoil_llm.test_connection():
        print("✅ Tinfoil connection successful!")
        
        # List available models
        print("\nAvailable models:")
        for model_id, info in tinfoil_llm.list_available_models().items():
            print(f"  * {model_id}: {info['name']} - {info['strengths']}")
        
        # Test multilingual content with Llama
        multilingual_content = """
        Bonjour! Je m'appelle Jean Dupont et je travaille à Paris.
        Mon email est jean.dupont@company.fr et mon téléphone est 01-23-45-67-89.
        Hello! My name is John Smith and I work in New York.
        My email is john.smith@company.com and my phone is 555-123-4567.
        """
        
        print(f"\nTesting Llama 3.3 70B with multilingual content:")
        detected = tinfoil_llm.detect_sensitive_data(multilingual_content, "llama")
        
        for entity_type, values in detected.items():
            if values:
                print(f"  * {entity_type}: {values}")
    else:
        print("❌ Tinfoil connection failed!")
