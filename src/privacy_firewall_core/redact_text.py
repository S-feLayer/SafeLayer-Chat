import re
from typing import Dict, List, Any
from .get_sensitive_data import get_sensitive_data, post_process_sensitive_data


def mask_text_content(text: str, sensitive_values: List[str]) -> Dict[str, Any]:
    """
    Redact sensitive data from text content and return masked version with summary.
    
    Args:
        text: The input text to redact
        sensitive_values: List of sensitive values to redact
        
    Returns:
        Dictionary containing redacted text, summary, and masked sensitive data
    """
    redacted_text = text
    redaction_count = 0
    redacted_items = []
    
    # Sort sensitive values by length (longest first) to avoid partial matches
    sorted_values = sorted(sensitive_values, key=len, reverse=True)
    
    for value in sorted_values:
        if value and value.strip():
            # Create a mask for this value
            if '@' in value:  # Email address
                username, domain = value.split('@')
                masked_username = username[:2] + '*' * (len(username) - 2)
                domain_parts = domain.split('.')
                masked_domain = domain_parts[0][:2] + '*' * (len(domain_parts[0]) - 2)
                mask = f"{masked_username}@{masked_domain}.{domain_parts[1]}"
            elif any(c.isdigit() for c in value):  # Phone number or ID
                mask = value[:2] + '*' * (len(value) - 4) + value[-2:]
            else:  # Name or other text
                mask = value[:2] + '*' * (len(value) - 2)
            
            # Replace all occurrences (case-insensitive)
            pattern = re.compile(re.escape(value), re.IGNORECASE)
            matches = pattern.findall(redacted_text)
            if matches:
                redacted_text = pattern.sub(mask, redacted_text)
                redaction_count += len(matches)
                redacted_items.append({
                    "original": value,
                    "masked": mask,
                    "count": len(matches)
                })
    
    return {
        "redacted_text": redacted_text,
        "original_text": text,
        "redaction_count": redaction_count,
        "redacted_items": redacted_items,
        "content_type": "text"
    }


def redact_text(text: str, tinfoil_llm) -> Dict[str, Any]:
    """
    Main function to redact sensitive data from text content.
    
    Args:
        text: The input text to redact
        tinfoil_llm: TinfoilLLM instance for AI processing
        
    Returns:
        Dictionary containing redaction results and summary
    """
    # Get sensitive data using AI
    sensitive_data = get_sensitive_data(text, tinfoil_llm)
    if sensitive_data is None:
        return {
            "success": False,
            "error": "No sensitive data found or error in processing"
        }
    
    # Process sensitive values
    sensitive_values = post_process_sensitive_data(sensitive_data)
    
    # Apply redactions
    redaction_result = mask_text_content(text, sensitive_values)
    
    # Add masked sensitive data summary
    from .redact_per_pdf import mask_sensitive_data
    masked_sensitive_data = mask_sensitive_data(sensitive_data)
    redaction_result["masked_sensitive_data"] = masked_sensitive_data
    
    return {
        "success": True,
        "redaction_result": redaction_result
    } 