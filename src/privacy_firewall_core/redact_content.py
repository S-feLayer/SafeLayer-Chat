import os
from typing import Dict, Any, Union
from .redact_per_pdf import redact_pdf
from .redact_code import redact_code_file, detect_language, CODE_EXTENSIONS
from .redact_text import redact_text


def detect_content_type(input_data: Union[str, Dict]) -> str:
    """
    Detect the type of content to be redacted.
    
    Args:
        input_data: Either a file path (str) or text content (str) or parameters dict
        
    Returns:
        Content type: 'pdf', 'code', 'text', or 'unknown'
    """
    if isinstance(input_data, dict):
        # Check for explicit content type
        if 'content_type' in input_data:
            return input_data['content_type']
        
        # Try to extract file path or text from dict
        for key in ['file_path', 'path', 'filename', 'file']:
            if key in input_data:
                return detect_content_type(input_data[key])
        
        # If it has text content, it's text
        if 'text' in input_data or 'content' in input_data:
            return 'text'
    
    elif isinstance(input_data, str):
        # Check if it's a file path
        if os.path.exists(input_data):
            # Check file extension
            _, ext = os.path.splitext(input_data.lower())
            if ext == '.pdf':
                return 'pdf'
            elif ext in CODE_EXTENSIONS:
                return 'code'
            else:
                return 'unknown'
        else:
            # If it's not a file path, treat as text content
            return 'text'
    
    return 'unknown'


def extract_input_data(input_data: Union[str, Dict]) -> Dict[str, Any]:
    """
    Extract relevant data from input parameters.
    
    Args:
        input_data: Input parameters (string or dict)
        
    Returns:
        Dictionary with extracted data
    """
    if isinstance(input_data, str):
        return {
            'file_path': input_data if os.path.exists(input_data) else None,
            'text': input_data if not os.path.exists(input_data) else None
        }
    elif isinstance(input_data, dict):
        # Extract file path
        file_path = None
        for key in ['file_path', 'path', 'filename', 'file']:
            if key in input_data:
                file_path = input_data[key]
                break
        
        # Extract text content
        text = None
        for key in ['text', 'content', 'message', 'prompt']:
            if key in input_data:
                text = input_data[key]
                break
        
        return {
            'file_path': file_path,
            'text': text,
            'content_type': input_data.get('content_type')
        }
    
    return {}


def redact_content(input_data: Union[str, Dict], tinfoil_llm) -> Dict[str, Any]:
    """
    Universal redaction function that handles PDFs, code files, and text content.
    
    Args:
        input_data: Either a file path (str), text content (str), or parameters dict
        tinfoil_llm: TinfoilLLM instance for AI processing
        
    Returns:
        Dictionary containing redaction results and summary
    """
    # Detect content type
    content_type = detect_content_type(input_data)
    
    # Extract input data
    data = extract_input_data(input_data)
    
    if content_type == 'pdf':
        if not data.get('file_path'):
            return {
                "success": False,
                "error": "No PDF file path provided"
            }
        
        try:
            redaction_summary, highlighted_path = redact_pdf(data['file_path'], tinfoil_llm)
            return {
                "success": True,
                "content_type": "pdf",
                "redaction_summary": redaction_summary,
                "highlighted_path": highlighted_path
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing PDF: {str(e)}"
            }
    
    elif content_type == 'code':
        if not data.get('file_path'):
            return {
                "success": False,
                "error": "No code file path provided"
            }
        
        return redact_code_file(data['file_path'], tinfoil_llm)
    
    elif content_type == 'text':
        if not data.get('text'):
            return {
                "success": False,
                "error": "No text content provided"
            }
        
        return redact_text(data['text'], tinfoil_llm)
    
    else:
        return {
            "success": False,
            "error": f"Unsupported content type: {content_type}. Supported types: pdf, code, text"
        }


def get_supported_formats() -> Dict[str, list]:
    """
    Get list of supported file formats and content types.
    
    Returns:
        Dictionary with supported formats
    """
    return {
        "pdf": [".pdf"],
        "code": list(CODE_EXTENSIONS.keys()),
        "text": ["plain text", "chat messages", "prompts"]
    } 