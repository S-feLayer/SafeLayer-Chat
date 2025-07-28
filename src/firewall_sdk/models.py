"""
SecureAI SDK Models

Pydantic models for type safety and data validation.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ProcessingOptions(BaseModel):
    """Options for content processing."""
    
    aggressive_mode: bool = Field(default=False, description="Enable aggressive redaction mode")
    preserve_format: bool = Field(default=True, description="Preserve original formatting")
    include_highlights: bool = Field(default=True, description="Include highlighted version")
    custom_patterns: Optional[List[str]] = Field(default=None, description="Custom regex patterns")
    sensitivity_level: str = Field(default="medium", description="Sensitivity level: low, medium, high")
    
    class Config:
        extra = "forbid"

class RedactionResult(BaseModel):
    """Result of content redaction."""
    
    success: bool = Field(description="Whether the redaction was successful")
    content_type: str = Field(description="Type of content processed")
    processing_time: Optional[float] = Field(default=None, description="Processing time in seconds")
    redacted_content: Optional[str] = Field(default=None, description="Redacted text content")
    redacted_file_path: Optional[str] = Field(default=None, description="Path to redacted file")
    highlighted_file_path: Optional[str] = Field(default=None, description="Path to highlighted file")
    detected_patterns: Optional[List[str]] = Field(default=None, description="Detected sensitive patterns")
    redaction_summary: Optional[Dict[str, Any]] = Field(default=None, description="Detailed redaction summary")
    error: Optional[str] = Field(default=None, description="Error message if processing failed")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Processing timestamp")
    
    class Config:
        extra = "allow"

class SupportedFormats(BaseModel):
    """Supported file formats and content types."""
    
    success: bool = Field(description="Whether the request was successful")
    supported_formats: Dict[str, List[str]] = Field(description="Supported formats by category")
    file_extensions: List[str] = Field(description="Supported file extensions")
    content_types: List[str] = Field(description="Supported content types")
    max_file_size: str = Field(description="Maximum file size")
    
    class Config:
        extra = "allow"

class HealthStatus(BaseModel):
    """Health status of the SecureAI service."""
    
    status: str = Field(description="Overall health status")
    timestamp: str = Field(description="Health check timestamp")
    version: str = Field(description="Service version")
    uptime: float = Field(description="Service uptime in seconds")
    services: Dict[str, Dict[str, Any]] = Field(description="Individual service status")
    system: Dict[str, Any] = Field(description="System resource information")
    dependencies: Dict[str, Dict[str, Any]] = Field(description="External dependency status")
    
    class Config:
        extra = "allow" 