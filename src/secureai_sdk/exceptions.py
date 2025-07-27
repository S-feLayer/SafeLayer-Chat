"""
SecureAI SDK Exceptions

Custom exception classes for the SecureAI SDK.
"""

class SecureAIError(Exception):
    """Base exception for all SecureAI SDK errors."""
    pass

class APIError(SecureAIError):
    """Raised when there's an error communicating with the SecureAI service."""
    pass

class ValidationError(SecureAIError):
    """Raised when input validation fails."""
    pass

class ProcessingError(SecureAIError):
    """Raised when content processing fails."""
    pass

class ConfigurationError(SecureAIError):
    """Raised when SDK configuration is invalid."""
    pass

class AuthenticationError(SecureAIError):
    """Raised when authentication fails."""
    pass

class RateLimitError(SecureAIError):
    """Raised when rate limits are exceeded."""
    pass 