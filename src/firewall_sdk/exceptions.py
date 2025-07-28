"""
Privacy Firewall SDK Exceptions

Custom exception classes for the Privacy Firewall SDK.
"""

class PrivacyFirewallError(Exception):
    """Base exception for all Privacy Firewall SDK errors."""
    pass

class APIError(PrivacyFirewallError):
    """Raised when there's an error communicating with the Privacy Firewall service."""
    pass

class ValidationError(PrivacyFirewallError):
    """Raised when input validation fails."""
    pass

class ProcessingError(PrivacyFirewallError):
    """Raised when content processing fails."""
    pass

class ConfigurationError(PrivacyFirewallError):
    """Raised when SDK configuration is invalid."""
    pass

class AuthenticationError(PrivacyFirewallError):
    """Raised when authentication fails."""
    pass

class RateLimitError(PrivacyFirewallError):
    """Raised when rate limits are exceeded."""
    pass 