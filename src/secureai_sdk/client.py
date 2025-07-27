"""
SecureAI SDK Client

Main client class for interacting with the SecureAI privacy firewall service.
"""

import os
import json
import requests
from typing import Dict, Any, Optional, Union
from pathlib import Path
import logging

from .exceptions import SecureAIError, APIError, ValidationError, ProcessingError
from .models import RedactionResult, ProcessingOptions, SupportedFormats

logger = logging.getLogger(__name__)

class SecureAI:
    """
    SecureAI client for automatic content redaction.
    
    This client provides a simple interface for redacting sensitive data
    from PDFs, code files, and text content using AI-powered detection.
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        base_url: str = "http://localhost:8000",
        timeout: int = 300,
        verify_ssl: bool = True
    ):
        """
        Initialize the SecureAI client.
        
        Args:
            api_key: Tinfoil API key for AI analysis. If not provided, 
                    will try to get from TINFOIL_API_KEY environment variable.
            base_url: Base URL for the SecureAI service
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.api_key = api_key or os.getenv("TINFOIL_API_KEY")
        if not self.api_key:
            raise ValidationError("API key is required. Set TINFOIL_API_KEY environment variable or pass api_key parameter.")
        
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        
        # Set up session headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': f'SecureAI-SDK/1.0.0'
        })
        
        logger.info(f"SecureAI client initialized with base URL: {self.base_url}")
    
    def _make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make HTTP request to the SecureAI service.
        
        Args:
            endpoint: API endpoint
            method: HTTP method
            data: Request data
            
        Returns:
            Response data
            
        Raises:
            APIError: If the request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, timeout=self.timeout, verify=self.verify_ssl)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, timeout=self.timeout, verify=self.verify_ssl)
            else:
                raise ValidationError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise APIError(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {e}")
            raise APIError(f"Invalid response format: {e}")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check the health status of the SecureAI service.
        
        Returns:
            Health status information
        """
        return self._make_request("/health")
    
    def get_supported_formats(self) -> SupportedFormats:
        """
        Get list of supported file formats and content types.
        
        Returns:
            SupportedFormats object with format information
        """
        response = self._make_request("/formats")
        return SupportedFormats(**response)
    
    def redact_text(self, text: str, options: Optional[ProcessingOptions] = None) -> RedactionResult:
        """
        Redact sensitive data from text content.
        
        Args:
            text: Text content to redact
            options: Processing options
            
        Returns:
            RedactionResult with redacted content and metadata
        """
        if not text or not text.strip():
            raise ValidationError("Text content cannot be empty")
        
        data = {
            "text": text,
            "content_type": "text"
        }
        
        if options:
            data.update(options.dict())
        
        response = self._make_request("/redact", method="POST", data=data)
        
        if not response.get("success"):
            raise ProcessingError(response.get("error", "Unknown processing error"))
        
        return RedactionResult(**response)
    
    def redact_file(self, file_path: Union[str, Path], options: Optional[ProcessingOptions] = None) -> RedactionResult:
        """
        Redact sensitive data from a file.
        
        Args:
            file_path: Path to the file to redact
            options: Processing options
            
        Returns:
            RedactionResult with redacted file path and metadata
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise ValidationError(f"File not found: {file_path}")
        
        if not file_path.is_file():
            raise ValidationError(f"Path is not a file: {file_path}")
        
        # Determine content type from file extension
        content_type = self._get_content_type(file_path)
        
        data = {
            "file_path": str(file_path.absolute()),
            "content_type": content_type
        }
        
        if options:
            data.update(options.dict())
        
        response = self._make_request("/redact", method="POST", data=data)
        
        if not response.get("success"):
            raise ProcessingError(response.get("error", "Unknown processing error"))
        
        return RedactionResult(**response)
    
    def redact_pdf(self, file_path: Union[str, Path], options: Optional[ProcessingOptions] = None) -> RedactionResult:
        """
        Redact sensitive data from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            options: Processing options
            
        Returns:
            RedactionResult with redacted PDF path and metadata
        """
        file_path = Path(file_path)
        
        if not file_path.suffix.lower() == '.pdf':
            raise ValidationError(f"File must be a PDF: {file_path}")
        
        return self.redact_file(file_path, options)
    
    def redact_code(self, file_path: Union[str, Path], options: Optional[ProcessingOptions] = None) -> RedactionResult:
        """
        Redact sensitive data from a code file.
        
        Args:
            file_path: Path to the code file
            options: Processing options
            
        Returns:
            RedactionResult with redacted code file path and metadata
        """
        file_path = Path(file_path)
        
        # Check if it's a code file
        code_extensions = {'.py', '.js', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt'}
        if file_path.suffix.lower() not in code_extensions:
            raise ValidationError(f"File must be a code file: {file_path}")
        
        return self.redact_file(file_path, options)
    
    def _get_content_type(self, file_path: Path) -> str:
        """
        Determine content type from file extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Content type string
        """
        ext = file_path.suffix.lower()
        
        if ext == '.pdf':
            return 'pdf'
        elif ext in {'.py', '.js', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt'}:
            return 'code'
        else:
            return 'text'
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get service metrics (if available).
        
        Returns:
            Metrics data
        """
        return self._make_request("/metrics")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.session.close() 