"""
SecureAI SDK - Universal Privacy Firewall for PDFs, Code Files, and Text Content

A production-ready SDK for automatic detection and redaction of sensitive data
using AI-powered analysis.

Example:
    from secureai_sdk import SecureAI
    
    # Initialize client
    client = SecureAI(api_key="your_tinfoil_api_key")
    
    # Redact PDF
    result = client.redact_pdf("document.pdf")
    
    # Redact code
    result = client.redact_code("source.py")
    
    # Redact text
    result = client.redact_text("sensitive content")
"""

from .client import SecureAI
from .exceptions import SecureAIError, APIError, ValidationError, ProcessingError
from .models import RedactionResult, ProcessingOptions, SupportedFormats

__version__ = "1.0.0"
__author__ = "SecureAI Team"
__email__ = "support@secureai.com"

__all__ = [
    "SecureAI",
    "SecureAIError", 
    "APIError",
    "ValidationError", 
    "ProcessingError",
    "RedactionResult",
    "ProcessingOptions",
    "SupportedFormats"
] 