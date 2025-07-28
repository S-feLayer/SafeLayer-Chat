import os
import re
from typing import Dict, List, Any, Tuple
from .get_sensitive_data import get_sensitive_data, post_process_sensitive_data


# Common code file extensions
CODE_EXTENSIONS = {
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.java': 'java',
    '.cpp': 'cpp',
    '.c': 'c',
    '.cs': 'csharp',
    '.php': 'php',
    '.rb': 'ruby',
    '.go': 'go',
    '.rs': 'rust',
    '.swift': 'swift',
    '.kt': 'kotlin',
    '.scala': 'scala',
    '.r': 'r',
    '.m': 'matlab',
    '.sh': 'bash',
    '.ps1': 'powershell',
    '.sql': 'sql',
    '.html': 'html',
    '.css': 'css',
    '.xml': 'xml',
    '.json': 'json',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.toml': 'toml',
    '.ini': 'ini',
    '.cfg': 'config',
    '.conf': 'config',
    '.env': 'env',
    '.dockerfile': 'dockerfile',
    '.docker': 'dockerfile'
}


def detect_language(file_path: str) -> str:
    """
    Detect the programming language based on file extension.
    
    Args:
        file_path: Path to the code file
        
    Returns:
        Language identifier string
    """
    _, ext = os.path.splitext(file_path.lower())
    return CODE_EXTENSIONS.get(ext, 'unknown')


def read_code_file(file_path: str) -> str:
    """
    Read a code file and return its content.
    
    Args:
        file_path: Path to the code file
        
    Returns:
        File content as string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Could not read file {file_path}: {str(e)}")


def mask_code_content(code: str, sensitive_values: List[str], language: str) -> Dict[str, Any]:
    """
    Redact sensitive data from code content while preserving code structure.
    
    Args:
        code: The input code to redact
        sensitive_values: List of sensitive values to redact
        language: Programming language identifier
        
    Returns:
        Dictionary containing redacted code, summary, and masked sensitive data
    """
    redacted_code = code
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
            matches = pattern.findall(redacted_code)
            if matches:
                redacted_code = pattern.sub(mask, redacted_code)
                redaction_count += len(matches)
                redacted_items.append({
                    "original": value,
                    "masked": mask,
                    "count": len(matches)
                })
    
    return {
        "redacted_code": redacted_code,
        "original_code": code,
        "redaction_count": redaction_count,
        "redacted_items": redacted_items,
        "language": language,
        "content_type": "code"
    }


def save_redacted_code(original_path: str, redacted_code: str) -> str:
    """
    Save redacted code to a new file.
    
    Args:
        original_path: Path to the original code file
        redacted_code: The redacted code content
        
    Returns:
        Path to the saved redacted file
    """
    try:
        # Create redacted file path
        base_path, ext = os.path.splitext(original_path)
        redacted_path = f"{base_path}_redacted{ext}"
        
        # Save redacted code
        with open(redacted_path, 'w', encoding='utf-8') as f:
            f.write(redacted_code)
        
        return redacted_path
    except Exception as e:
        raise Exception(f"Could not save redacted file: {str(e)}")


def redact_code_file(file_path: str, tinfoil_llm) -> Dict[str, Any]:
    """
    Main function to redact sensitive data from a code file.
    
    Args:
        file_path: Path to the code file to redact
        tinfoil_llm: TinfoilLLM instance for AI processing
        
    Returns:
        Dictionary containing redaction results and summary
    """
    # Check if file exists
    if not os.path.exists(file_path):
        return {
            "success": False,
            "error": f"File not found: {file_path}"
        }
    
    # Detect language
    language = detect_language(file_path)
    if language == 'unknown':
        return {
            "success": False,
            "error": f"Unsupported file type: {file_path}"
        }
    
    try:
        # Read code file
        code_content = read_code_file(file_path)
        
        # Get sensitive data using AI
        sensitive_data = get_sensitive_data(code_content, tinfoil_llm)
        if sensitive_data is None:
            return {
                "success": False,
                "error": "No sensitive data found or error in processing"
            }
        
        # Process sensitive values
        sensitive_values = post_process_sensitive_data(sensitive_data)
        
        # Apply redactions
        redaction_result = mask_code_content(code_content, sensitive_values, language)
        
        # Save redacted file
        redacted_file_path = save_redacted_code(file_path, redaction_result["redacted_code"])
        redaction_result["redacted_file_path"] = redacted_file_path
        
        # Add masked sensitive data summary
        from .redact_per_pdf import mask_sensitive_data
        masked_sensitive_data = mask_sensitive_data(sensitive_data)
        redaction_result["masked_sensitive_data"] = masked_sensitive_data
        
        return {
            "success": True,
            "redaction_result": redaction_result
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error processing code file: {str(e)}"
        } 