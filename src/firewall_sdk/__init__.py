"""
Privacy Firewall SDK - Universal Content Protection for PDFs, Code Files, and Text Content

A production-ready SDK for automatic detection and redaction of sensitive data
using AI-powered analysis.

Example:
    from firewall_sdk import PrivacyFirewall
    
    # Initialize client
    client = PrivacyFirewall(api_key="your_tinfoil_api_key")
    
    # Redact PDF
    result = client.redact_pdf("document.pdf")
    
    # Redact code
    result = client.redact_code("source.py")
    
    # Redact text
    result = client.redact_text("sensitive content")
"""

from .client import PrivacyFirewall
from .exceptions import PrivacyFirewallError, APIError, ValidationError, ProcessingError
from .models import RedactionResult, ProcessingOptions, SupportedFormats

__version__ = "1.0.0"
__author__ = "Privacy Firewall Team"
__email__ = "support@privacyfirewall.com"

__all__ = [
    "PrivacyFirewall",
    "PrivacyFirewallError", 
    "APIError",
    "ValidationError", 
    "ProcessingError",
    "RedactionResult",
    "ProcessingOptions",
    "SupportedFormats"
] 