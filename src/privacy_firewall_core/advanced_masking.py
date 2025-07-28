import re
import hashlib
import base64
from typing import Dict, List, Any, Optional, Callable
from enum import Enum

class MaskingStrategy(Enum):
    """Different masking strategies available."""
    PARTIAL = "partial"  # Keep first/last few characters
    FULL = "full"        # Replace with asterisks
    HASH = "hash"        # Replace with hash
    ENCODE = "encode"    # Base64 encode
    CUSTOM = "custom"    # Custom function

class AdvancedMasking:
    """
    Advanced masking strategies for sensitive data.
    """
    
    def __init__(self, strategy: MaskingStrategy = MaskingStrategy.PARTIAL):
        self.strategy = strategy
        self.custom_functions = {}
        
    def set_custom_function(self, data_type: str, func: Callable[[str], str]):
        """Set a custom masking function for a specific data type."""
        self.custom_functions[data_type] = func
    
    def mask_value(self, value: str, data_type: str = "general") -> str:
        """
        Mask a single value using the specified strategy.
        """
        if not value or not isinstance(value, str):
            return value
        
        # Use custom function if available
        if data_type in self.custom_functions:
            return self.custom_functions[data_type](value)
        
        # Apply strategy-based masking
        if self.strategy == MaskingStrategy.PARTIAL:
            return self._mask_partial(value, data_type)
        elif self.strategy == MaskingStrategy.FULL:
            return self._mask_full(value)
        elif self.strategy == MaskingStrategy.HASH:
            return self._mask_hash(value)
        elif self.strategy == MaskingStrategy.ENCODE:
            return self._mask_encode(value)
        else:
            return self._mask_partial(value, data_type)
    
    def _mask_partial(self, value: str, data_type: str) -> str:
        """Partial masking - keep some characters visible."""
        if data_type == 'email':
            return self._mask_email(value)
        elif data_type in ['phone', 'ssn', 'credit_card']:
            return self._mask_numeric(value)
        elif data_type in ['api_key', 'jwt_token', 'private_key']:
            return self._mask_secret(value)
        else:
            return self._mask_general(value)
    
    def _mask_email(self, email: str) -> str:
        """Mask email address."""
        if '@' not in email:
            return self._mask_general(email)
        
        username, domain = email.split('@', 1)
        domain_parts = domain.split('.')
        
        # Mask username
        if len(username) <= 2:
            masked_username = username
        else:
            masked_username = username[:2] + '*' * (len(username) - 2)
        
        # Mask domain
        if len(domain_parts) >= 2:
            if len(domain_parts[0]) <= 2:
                masked_domain = domain_parts[0]
            else:
                masked_domain = domain_parts[0][:2] + '*' * (len(domain_parts[0]) - 2)
            masked_domain += '.' + '.'.join(domain_parts[1:])
        else:
            masked_domain = domain
        
        return f"{masked_username}@{masked_domain}"
    
    def _mask_numeric(self, value: str) -> str:
        """Mask numeric values like phone numbers, SSNs, credit cards."""
        # Remove non-digits
        digits = re.sub(r'\D', '', value)
        
        if len(digits) <= 4:
            return '*' * len(value)
        
        # Keep first 2 and last 2 digits
        return digits[:2] + '*' * (len(digits) - 4) + digits[-2:]
    
    def _mask_secret(self, value: str) -> str:
        """Mask secrets like API keys, tokens."""
        if len(value) <= 8:
            return '*' * len(value)
        
        # Keep first 4 and last 4 characters
        return value[:4] + '*' * (len(value) - 8) + value[-4:]
    
    def _mask_general(self, value: str) -> str:
        """General masking for text values."""
        if len(value) <= 2:
            return value
        
        # Keep first 2 characters
        return value[:2] + '*' * (len(value) - 2)
    
    def _mask_full(self, value: str) -> str:
        """Full masking - replace with asterisks."""
        return '*' * len(value)
    
    def _mask_hash(self, value: str) -> str:
        """Hash-based masking."""
        hash_obj = hashlib.sha256(value.encode())
        return f"[HASH:{hash_obj.hexdigest()[:8]}]"
    
    def _mask_encode(self, value: str) -> str:
        """Base64 encoding masking."""
        encoded = base64.b64encode(value.encode()).decode()
        return f"[ENCODED:{encoded[:10]}...]"
    
    def mask_content(self, content: str, sensitive_data: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Mask sensitive data in content and return results.
        """
        masked_content = content
        redaction_count = 0
        redacted_items = []
        
        # Sort by length (longest first) to avoid partial matches
        all_values = []
        for data_type, values in sensitive_data.items():
            for value in values:
                all_values.append((value, data_type))
        
        all_values.sort(key=lambda x: len(x[0]), reverse=True)
        
        for value, data_type in all_values:
            if not value or not value.strip():
                continue
            
            # Create mask
            mask = self.mask_value(value, data_type)
            
            # Replace all occurrences (case-insensitive)
            pattern = re.compile(re.escape(value), re.IGNORECASE)
            matches = pattern.findall(masked_content)
            
            if matches:
                masked_content = pattern.sub(mask, masked_content)
                redaction_count += len(matches)
                redacted_items.append({
                    "original": value,
                    "masked": mask,
                    "data_type": data_type,
                    "count": len(matches)
                })
        
        return {
            "masked_content": masked_content,
            "original_content": content,
            "redaction_count": redaction_count,
            "redacted_items": redacted_items,
            "strategy": self.strategy.value
        }

class ContextualMasking(AdvancedMasking):
    """
    Context-aware masking that considers the surrounding context.
    """
    
    def __init__(self, strategy: MaskingStrategy = MaskingStrategy.PARTIAL):
        super().__init__(strategy)
        self.context_rules = {
            'code': {
                'variable_names': lambda x: x if len(x) <= 3 else x[:3] + '*',
                'string_literals': lambda x: '"***"',
                'comments': lambda x: '// ***',
            },
            'text': {
                'names': lambda x: x[0] + '*' * (len(x) - 1) if len(x) > 1 else x,
                'addresses': lambda x: '[ADDRESS REDACTED]',
                'dates': lambda x: '[DATE REDACTED]',
            }
        }
    
    def mask_with_context(self, content: str, sensitive_data: Dict[str, List[str]], 
                         context_type: str = "general") -> Dict[str, Any]:
        """
        Mask content considering the context type.
        """
        # Apply context-specific rules
        if context_type in self.context_rules:
            for data_type, rule_func in self.context_rules[context_type].items():
                self.set_custom_function(data_type, rule_func)
        
        return self.mask_content(content, sensitive_data) 