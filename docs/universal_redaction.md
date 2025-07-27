# Universal Redaction Guide

Secure AI now supports redaction across multiple content types: PDFs, code files, and text content. This guide covers all the new capabilities and how to use them.

## Overview

The universal redaction system automatically detects the content type and applies appropriate redaction strategies:

- **PDFs**: Page-by-page redaction with visual highlighting
- **Code Files**: Syntax-preserving redaction for 30+ programming languages
- **Text Content**: Real-time redaction for chat messages, emails, and documents

## Supported Content Types

### PDF Documents
- **Extensions**: `.pdf`
- **Features**: 
  - Page-by-page redaction
  - Visual highlighting of sensitive data
  - Creates both redacted and highlighted versions
  - Preserves document structure and formatting

### Code Files
- **Languages**: Python, JavaScript, TypeScript, Java, C++, C#, PHP, Ruby, Go, Rust, Swift, Kotlin, Scala, R, MATLAB, Bash, PowerShell, SQL, HTML, CSS, XML, JSON, YAML, TOML, INI, Config files, Environment files, Dockerfiles
- **Features**:
  - Preserves code syntax and structure
  - Redacts API keys, passwords, personal information
  - Creates redacted file with `_redacted` suffix
  - Maintains code readability

### Text Content
- **Types**: Chat messages, emails, documents, prompts
- **Features**:
  - Real-time redaction
  - Returns redacted text immediately
  - Perfect for sensitive conversations
  - No file creation required

## API Reference

### Main Function: `redact_content()`

```python
from secureai import redact_content
from secureai.tinfoil_llm import TinfoilLLM

tinfoil_llm = TinfoilLLM()

# Universal redaction function
result = redact_content(input_data, tinfoil_llm)
```

#### Parameters

- `input_data`: Can be:
  - **String**: File path or text content
  - **Dictionary**: With keys like `file_path`, `text`, `content_type`
- `tinfoil_llm`: TinfoilLLM instance for AI processing

#### Return Value

```python
{
    "success": bool,
    "content_type": str,  # "pdf", "code", "text", or "unknown"
    "error": str,  # Only present if success=False
    "redaction_summary": dict,  # For PDFs
    "redaction_result": dict,   # For code and text
    "highlighted_path": str     # For PDFs
}
```

### Specialized Functions

#### PDF Redaction
```python
from secureai import redact_pdf

result = redact_pdf("document.pdf", tinfoil_llm)
redaction_summary, highlighted_path = result
```

#### Code Redaction
```python
from secureai import redact_code_file

result = redact_code_file("config.py", tinfoil_llm)
```

#### Text Redaction
```python
from secureai import redact_text

result = redact_text("Hello John, my email is john@example.com", tinfoil_llm)
```

## Usage Examples

### 1. Redacting a PDF Document

```python
from secureai import redact_content
from secureai.tinfoil_llm import TinfoilLLM

tinfoil_llm = TinfoilLLM()

# Method 1: Direct file path
result = redact_content("/path/to/document.pdf", tinfoil_llm)

# Method 2: Dictionary parameters
result = redact_content({
    "file_path": "/path/to/document.pdf",
    "content_type": "pdf"
}, tinfoil_llm)

if result["success"]:
    print(f"Redacted PDF: {result['redaction_summary']['redacted_pdf_path']}")
    print(f"Highlighted PDF: {result['highlighted_path']}")
```

### 2. Redacting a Code File

```python
# Method 1: Direct file path
result = redact_content("/path/to/config.py", tinfoil_llm)

# Method 2: Dictionary parameters
result = redact_content({
    "file_path": "/path/to/.env",
    "content_type": "code"
}, tinfoil_llm)

if result["success"]:
    redacted = result["redaction_result"]
    print(f"Language: {redacted['language']}")
    print(f"Redactions: {redacted['redaction_count']}")
    print(f"Redacted file: {redacted['redacted_file_path']}")
```

### 3. Redacting Text Content

```python
# Method 1: Direct text
text = "Hi John Doe, my email is john@example.com and phone is 555-123-4567"
result = redact_content(text, tinfoil_llm)

# Method 2: Dictionary parameters
result = redact_content({
    "text": "Hello Jane, my ID is 12345",
    "content_type": "text"
}, tinfoil_llm)

if result["success"]:
    redacted = result["redaction_result"]
    print(f"Redacted text: {redacted['redacted_text']}")
    print(f"Redactions: {redacted['redaction_count']}")
```

### 4. Using with Claude MCP

```python
# In Claude, you can use these commands:

# PDF redaction
"Redact sensitive information from this PDF: /path/to/document.pdf"

# Code redaction
"Redact API keys and passwords from: /path/to/config.py"
"Remove sensitive data from: /path/to/.env"

# Text redaction
"Redact this message: 'Hi John, my email is john@example.com'"
"Remove personal information from this text: [paste text here]"

# Universal redaction
"Redact this content: /path/to/file.txt"
"Process this for sensitive data: [any file path or text]"
```

## Content Type Detection

The system automatically detects content type based on:

1. **Explicit content_type** in dictionary parameters
2. **File extension** for existing files
3. **Content analysis** for text strings

### Detection Logic

```python
def detect_content_type(input_data):
    if isinstance(input_data, dict):
        if 'content_type' in input_data:
            return input_data['content_type']
        # Check for file paths or text content
    
    elif isinstance(input_data, str):
        if os.path.exists(input_data):
            ext = os.path.splitext(input_data.lower())[1]
            if ext == '.pdf':
                return 'pdf'
            elif ext in CODE_EXTENSIONS:
                return 'code'
            else:
                return 'unknown'
        else:
            return 'text'
    
    return 'unknown'
```

## Redaction Strategies

### Masking Patterns

- **Email addresses**: `jo***@ex***.com`
- **Phone numbers**: `55***67`
- **Names and text**: `Jo***`
- **IDs and numbers**: `12***45`

### Sensitive Data Types Detected

- **Personal Information**: Names, emails, phone numbers, addresses
- **Business Data**: Company names, IDs, contract numbers
- **Technical Data**: API keys, passwords, database credentials
- **Dates**: Birth dates, sensitive timestamps

## Error Handling

### Common Errors

```python
# File not found
{
    "success": False,
    "error": "File not found: /path/to/file.txt"
}

# Unsupported content type
{
    "success": False,
    "error": "Unsupported content type: unknown"
}

# Processing error
{
    "success": False,
    "error": "Error processing content: [details]"
}
```

### Best Practices

1. **Always check the `success` field** before accessing results
2. **Handle errors gracefully** in your applications
3. **Validate input** before processing
4. **Use appropriate content types** for better results

## Performance Considerations

- **PDFs**: Processing time depends on number of pages and content
- **Code files**: Fast processing, typically under 1 second
- **Text content**: Very fast, typically under 500ms
- **Large files**: Consider chunking for very large documents

## Security Features

- **Local processing**: Content stays on your machine
- **AI isolation**: Uses Tinfoil's isolated AI platform
- **Reversible masking**: Original data is masked, not deleted
- **No data transmission**: Sensitive data never leaves your system

## Migration from v0.2.0

If you're upgrading from the PDF-only version:

1. **Update imports**:
   ```python
   # Old
   from secureai import redact_pdf
   
   # New
   from secureai import redact_content, redact_pdf
   ```

2. **Update MCP configuration**:
   ```json
   {
     "mcpServers": {
       "universal-redaction": {
         "command": "/path/to/python",
         "args": ["/path/to/mcp_universal_redaction.py"],
         "env": {
           "TINFOIL_API_KEY": "your_api_key"
         }
       }
     }
   }
   ```

3. **Backward compatibility**: All existing PDF functionality remains unchanged

## Troubleshooting

### Common Issues

1. **Tinfoil API Key**: Ensure `TINFOIL_API_KEY` environment variable is set
2. **File permissions**: Check read/write permissions for file operations
3. **Python version**: Ensure Python 3.10-3.12 is used
4. **Dependencies**: Install all required packages

### Getting Help

- Check the [FAQ section](faq.md) for common issues
- Open an issue on GitHub for bugs or feature requests
- Review the example scripts in `src/scripts/` for usage patterns 