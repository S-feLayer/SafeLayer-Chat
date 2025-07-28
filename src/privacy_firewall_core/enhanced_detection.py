import re
import json
from typing import Dict, List, Any, Optional
from .tinfoil_llm import TinfoilLLM

class EnhancedDetection:
    """
    Enhanced sensitive data detection with multiple strategies.
    """
    
    def __init__(self, tinfoil_llm: TinfoilLLM):
        self.tinfoil_llm = tinfoil_llm
        
        # Predefined patterns for common sensitive data
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[-.\s]?\d{4}[-.\s]?\d{4}[-.\s]?\d{4}\b',
            'api_key': r'\b(sk-|pk-|ghp_|gho_|ghu_|ghs_|ghr_)[a-zA-Z0-9]{20,}\b',
            'jwt_token': r'\beyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*\b',
            'uuid': r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b',
            'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            'mac_address': r'\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b',
            'database_url': r'\b(postgresql|mysql|mongodb|redis)://[^\s]+\b',
            'aws_key': r'\bAKIA[0-9A-Z]{16}\b',
            'private_key': r'-----BEGIN (RSA |DSA |EC )?PRIVATE KEY-----',
            'public_key': r'-----BEGIN (RSA |DSA |EC )?PUBLIC KEY-----',
        }
    
    def detect_with_patterns(self, text: str) -> Dict[str, List[str]]:
        """
        Detect sensitive data using regex patterns.
        """
        detected = {}
        
        for data_type, pattern in self.patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                detected[data_type] = list(set(matches))
        
        return detected
    
    def detect_with_ai(self, text: str, content_type: str = "general") -> Dict[str, List[str]]:
        """
        Detect sensitive data using AI with content-specific prompts.
        """
        prompts = {
            "code": """Analyze this code and extract sensitive information in JSON format:
{
    "api_keys": [],
    "passwords": [],
    "database_credentials": [],
    "private_keys": [],
    "access_tokens": [],
    "personal_info": [],
    "company_secrets": [],
    "environment_variables": [],
    "config_secrets": []
}

Only return valid JSON. Code:
""",
            "pdf": """Extract sensitive information from this document text:
{
    "personal_names": [],
    "emails": [],
    "phone_numbers": [],
    "addresses": [],
    "social_security_numbers": [],
    "credit_card_numbers": [],
    "account_numbers": [],
    "contract_numbers": [],
    "company_names": [],
    "dates_of_birth": []
}

Only return valid JSON. Text:
""",
            "text": """Extract sensitive information from this text:
{
    "personal_names": [],
    "emails": [],
    "phone_numbers": [],
    "addresses": [],
    "social_security_numbers": [],
    "credit_card_numbers": [],
    "account_numbers": [],
    "contract_numbers": [],
    "company_names": [],
    "dates_of_birth": [],
    "api_keys": [],
    "passwords": []
}

Only return valid JSON. Text:
""",
            "general": """Extract all sensitive information from this content:
{
    "personal_names": [],
    "emails": [],
    "phone_numbers": [],
    "addresses": [],
    "social_security_numbers": [],
    "credit_card_numbers": [],
    "account_numbers": [],
    "contract_numbers": [],
    "company_names": [],
    "dates_of_birth": [],
    "api_keys": [],
    "passwords": [],
    "database_credentials": [],
    "private_keys": [],
    "access_tokens": []
}

Only return valid JSON. Content:
"""
        }
        
        prompt = prompts.get(content_type, prompts["general"])
        full_prompt = prompt + text
        
        try:
            response = self.tinfoil_llm.get_tinfoil_response(full_prompt, model="deepseek")
            response = response.replace("```json", "").replace("```", "").strip()
            return json.loads(response)
        except (json.JSONDecodeError, Exception) as e:
            print(f"AI detection failed: {e}")
            return {}
    
    def detect_sensitive_data(self, text: str, content_type: str = "general") -> Dict[str, List[str]]:
        """
        Combined detection using both patterns and AI.
        """
        # Pattern-based detection
        pattern_results = self.detect_with_patterns(text)
        
        # AI-based detection
        ai_results = self.detect_with_ai(text, content_type)
        
        # Combine results
        combined = {}
        
        # Add pattern results
        for key, values in pattern_results.items():
            combined[key] = values
        
        # Add AI results, avoiding duplicates
        for key, values in ai_results.items():
            if key in combined:
                # Merge and remove duplicates
                existing = set(combined[key])
                new_values = [v for v in values if v not in existing]
                combined[key].extend(new_values)
            else:
                combined[key] = values
        
        return combined
    
    def validate_detection(self, detected_data: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Validate and filter detected sensitive data.
        """
        validated = {}
        
        for data_type, values in detected_data.items():
            if not values:
                continue
                
            # Filter out empty or invalid values
            filtered_values = []
            for value in values:
                if value and isinstance(value, str) and len(value.strip()) > 0:
                    # Additional validation based on type
                    if self._validate_value(data_type, value):
                        filtered_values.append(value.strip())
            
            if filtered_values:
                validated[data_type] = filtered_values
        
        return validated
    
    def _validate_value(self, data_type: str, value: str) -> bool:
        """
        Validate a specific value based on its type.
        """
        if data_type == 'email':
            return '@' in value and '.' in value
        elif data_type == 'phone':
            return any(c.isdigit() for c in value) and len(value) >= 10
        elif data_type == 'api_key':
            return len(value) > 10
        elif data_type == 'personal_names':
            return len(value) > 1 and not value.isdigit()
        else:
            return len(value) > 0 