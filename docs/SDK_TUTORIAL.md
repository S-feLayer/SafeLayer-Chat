# SecureAI SDK Tutorial

Learn how to use the SecureAI SDK to automatically detect and redact sensitive data from PDFs, code files, and text content.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [Error Handling](#error-handling)
6. [Best Practices](#best-practices)
7. [Examples](#examples)

## Installation

### Prerequisites

- Python 3.8 or higher
- Tinfoil API key
- SecureAI service running (or use our hosted service)

### Install the SDK

```bash
# Install from PyPI
pip install secureai-sdk

# Or install from source
git clone https://github.com/secureai/secureai-sdk.git
cd secureai-sdk
pip install -e .
```

### Set up your API key

```bash
# Set environment variable
export TINFOIL_API_KEY="your_tinfoil_api_key_here"

# Or use in your code
import os
os.environ["TINFOIL_API_KEY"] = "your_tinfoil_api_key_here"
```

## Quick Start

```python
from secureai_sdk import SecureAI

# Initialize the client
client = SecureAI(api_key="your_tinfoil_api_key")

# Redact sensitive data from text
result = client.redact_text("My email is john@example.com and phone is 555-123-4567")

if result.success:
    print(f"Redacted text: {result.redacted_content}")
    print(f"Detected patterns: {result.detected_patterns}")
else:
    print(f"Error: {result.error}")
```

## Basic Usage

### Text Redaction

The simplest way to redact sensitive data from text:

```python
from secureai_sdk import SecureAI

client = SecureAI()

# Basic text redaction
text = """
Hello, my name is John Doe and my email is john.doe@company.com.
You can reach me at 555-123-4567 or visit my website at https://example.com.
My credit card number is 4111-1111-1111-1111 and my SSN is 123-45-6789.
"""

result = client.redact_text(text)

if result.success:
    print("Original:", text)
    print("Redacted:", result.redacted_content)
    print("Detected:", result.detected_patterns)
```

### PDF Redaction

Redact sensitive data from PDF files:

```python
from pathlib import Path

# Redact a PDF file
pdf_path = Path("document.pdf")
result = client.redact_pdf(pdf_path)

if result.success:
    print(f"Original PDF: {pdf_path}")
    print(f"Redacted PDF: {result.redacted_file_path}")
    print(f"Highlighted PDF: {result.highlighted_file_path}")
    print(f"Detected patterns: {result.detected_patterns}")
```

### Code Redaction

Redact sensitive data from code files:

```python
# Redact a code file
code_path = Path("config.py")
result = client.redact_code(code_path)

if result.success:
    print(f"Original code: {code_path}")
    print(f"Redacted code: {result.redacted_file_path}")
    print(f"Detected patterns: {result.detected_patterns}")
```

### Universal File Redaction

Automatically detect file type and redact:

```python
# Works with any supported file type
file_path = Path("document.pdf")  # or "config.py" or "data.txt"
result = client.redact_file(file_path)

if result.success:
    print(f"Content type: {result.content_type}")
    print(f"Redacted file: {result.redacted_file_path}")
```

## Advanced Features

### Processing Options

Customize redaction behavior with processing options:

```python
from secureai_sdk import ProcessingOptions

# Create custom processing options
options = ProcessingOptions(
    aggressive_mode=True,           # More thorough redaction
    sensitivity_level="high",       # High sensitivity detection
    preserve_format=True,           # Keep original formatting
    include_highlights=True,        # Include highlighted version
    custom_patterns=[               # Custom regex patterns
        r"CUST-\d{5}",
        r"ORD-\d{5}"
    ]
)

# Use options with redaction
result = client.redact_text(text, options)
```

### Service Health Check

Monitor the health of your SecureAI service:

```python
# Check service health
health = client.health_check()

print(f"Status: {health['status']}")
print(f"Version: {health['version']}")
print(f"Uptime: {health['uptime']:.1f}s")

# Check individual services
for service_name, service_status in health['services'].items():
    print(f"{service_name}: {service_status['status']}")

# Check system resources
system = health['system']
print(f"Memory usage: {system['memory']['percent']:.1f}%")
print(f"CPU usage: {system['cpu']['percent']:.1f}%")
```

### Supported Formats

Get information about supported file formats:

```python
# Get supported formats
formats = client.get_supported_formats()

print("Supported formats:")
for category, format_list in formats.supported_formats.items():
    print(f"\n{category.upper()}:")
    for fmt in format_list:
        print(f"  • {fmt}")

print(f"\nMax file size: {formats.max_file_size}")
print(f"File extensions: {', '.join(formats.file_extensions[:10])}...")
```

### Context Manager Usage

Use the client as a context manager for automatic cleanup:

```python
# Automatic session management
with SecureAI(api_key="your_key") as client:
    result = client.redact_text("sensitive content")
    print(f"Result: {result.redacted_content}")
```

## Error Handling

The SDK provides comprehensive error handling with custom exceptions:

```python
from secureai_sdk import SecureAI, SecureAIError, ValidationError, APIError, ProcessingError

client = SecureAI()

try:
    # This will raise a ValidationError
    result = client.redact_text("")
except ValidationError as e:
    print(f"Validation error: {e}")

try:
    # This will raise an APIError if service is unavailable
    result = client.redact_pdf("nonexistent.pdf")
except APIError as e:
    print(f"API error: {e}")

try:
    # This will raise a ProcessingError if redaction fails
    result = client.redact_text("valid text")
    if not result.success:
        raise ProcessingError(result.error)
except ProcessingError as e:
    print(f"Processing error: {e}")

# Catch all SecureAI errors
try:
    result = client.redact_text("test")
except SecureAIError as e:
    print(f"SecureAI error: {e}")
```

## Best Practices

### 1. API Key Management

```python
# Use environment variables for API keys
import os
from secureai_sdk import SecureAI

# Recommended: Use environment variable
client = SecureAI()  # Automatically uses TINFOIL_API_KEY env var

# Alternative: Pass directly (not recommended for production)
client = SecureAI(api_key="your_key")
```

### 2. Error Handling

```python
# Always handle errors gracefully
try:
    result = client.redact_text(text)
    if result.success:
        # Process successful result
        process_redacted_content(result.redacted_content)
    else:
        # Handle processing failure
        log_error(f"Redaction failed: {result.error}")
except SecureAIError as e:
    # Handle SDK errors
    log_error(f"SDK error: {e}")
```

### 3. File Validation

```python
from pathlib import Path

def safe_redact_file(file_path: str):
    """Safely redact a file with validation."""
    path = Path(file_path)
    
    # Validate file exists
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Validate file size
    if path.stat().st_size > 100 * 1024 * 1024:  # 100MB
        raise ValueError("File too large")
    
    # Redact the file
    return client.redact_file(path)
```

### 4. Batch Processing

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def process_multiple_files(file_paths: list):
    """Process multiple files efficiently."""
    results = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit all files for processing
        future_to_file = {
            executor.submit(client.redact_file, path): path 
            for path in file_paths
        }
        
        # Collect results
        for future in concurrent.futures.as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                result = future.result()
                results.append((file_path, result))
            except Exception as e:
                results.append((file_path, {"error": str(e)}))
    
    return results
```

### 5. Configuration Management

```python
import json
from pathlib import Path

class SecureAIConfig:
    def __init__(self, config_path: str = "secureai_config.json"):
        self.config_path = Path(config_path)
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return self.get_default_config()
    
    def get_default_config(self):
        """Get default configuration."""
        return {
            "api_key": os.getenv("TINFOIL_API_KEY"),
            "base_url": "http://localhost:8000",
            "timeout": 300,
            "default_options": {
                "aggressive_mode": False,
                "sensitivity_level": "medium",
                "preserve_format": True
            }
        }
    
    def get_client(self):
        """Get configured SecureAI client."""
        return SecureAI(
            api_key=self.config["api_key"],
            base_url=self.config["base_url"],
            timeout=self.config["timeout"]
        )

# Usage
config = SecureAIConfig()
client = config.get_client()
```

## Examples

### Example 1: Document Processing Pipeline

```python
from pathlib import Path
from secureai_sdk import SecureAI, ProcessingOptions

def process_documents(directory: str):
    """Process all documents in a directory."""
    client = SecureAI()
    directory_path = Path(directory)
    
    # Get all supported files
    supported_extensions = {'.pdf', '.txt', '.py', '.js', '.java'}
    files = [
        f for f in directory_path.iterdir() 
        if f.is_file() and f.suffix.lower() in supported_extensions
    ]
    
    results = {}
    for file_path in files:
        print(f"Processing {file_path.name}...")
        
        try:
            # Use high sensitivity for documents
            options = ProcessingOptions(
                sensitivity_level="high",
                aggressive_mode=True
            )
            
            result = client.redact_file(file_path, options)
            results[file_path.name] = result
            
            if result.success:
                print(f"✅ {file_path.name}: {len(result.detected_patterns)} patterns detected")
            else:
                print(f"❌ {file_path.name}: {result.error}")
                
        except Exception as e:
            print(f"❌ {file_path.name}: {e}")
            results[file_path.name] = {"error": str(e)}
    
    return results

# Usage
results = process_documents("./documents")
```

### Example 2: Real-time Text Processing

```python
import time
from secureai_sdk import SecureAI

def real_time_redaction():
    """Real-time text redaction for user input."""
    client = SecureAI()
    
    print("Enter text to redact (type 'quit' to exit):")
    
    while True:
        text = input("\n> ")
        
        if text.lower() == 'quit':
            break
        
        if not text.strip():
            continue
        
        try:
            start_time = time.time()
            result = client.redact_text(text)
            processing_time = time.time() - start_time
            
            if result.success:
                print(f"\n🔒 Redacted ({processing_time:.2f}s):")
                print(result.redacted_content)
                
                if result.detected_patterns:
                    print(f"\n🔍 Detected: {', '.join(result.detected_patterns)}")
            else:
                print(f"❌ Error: {result.error}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

# Usage
real_time_redaction()
```

### Example 3: Web Application Integration

```python
from flask import Flask, request, jsonify
from secureai_sdk import SecureAI, ProcessingOptions

app = Flask(__name__)
client = SecureAI()

@app.route('/redact', methods=['POST'])
def redact_content():
    """API endpoint for content redaction."""
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({"error": "Content is required"}), 400
        
        content = data['content']
        content_type = data.get('type', 'text')
        
        # Get processing options from request
        options_data = data.get('options', {})
        options = ProcessingOptions(**options_data) if options_data else None
        
        # Process based on content type
        if content_type == 'text':
            result = client.redact_text(content, options)
        elif content_type == 'file':
            # Handle file upload
            file_path = save_uploaded_file(request.files['file'])
            result = client.redact_file(file_path, options)
        else:
            return jsonify({"error": "Invalid content type"}), 400
        
        # Return result
        return jsonify({
            "success": result.success,
            "redacted_content": result.redacted_content,
            "redacted_file": result.redacted_file_path,
            "detected_patterns": result.detected_patterns,
            "processing_time": result.processing_time
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

## Command Line Interface

The SDK also provides a command-line interface:

```bash
# Redact text
secureai text "My email is john@example.com"

# Redact PDF
secureai pdf document.pdf

# Redact code
secureai code config.py

# Check service health
secureai health

# Get supported formats
secureai formats

# Use custom options
secureai text "sensitive content" --aggressive --sensitivity high

# Output in JSON format
secureai text "sensitive content" --json
```

## Troubleshooting

### Common Issues

1. **API Key Not Set**
   ```python
   # Error: API key is required
   # Solution: Set TINFOIL_API_KEY environment variable
   export TINFOIL_API_KEY="your_key_here"
   ```

2. **Service Unavailable**
   ```python
   # Error: Request failed
   # Solution: Check if SecureAI service is running
   client.health_check()
   ```

3. **File Not Found**
   ```python
   # Error: File not found
   # Solution: Check file path and permissions
   from pathlib import Path
   file_path = Path("document.pdf")
   if file_path.exists():
       result = client.redact_pdf(file_path)
   ```

4. **Large File Processing**
   ```python
   # Error: File too large
   # Solution: Check file size limits
   formats = client.get_supported_formats()
   print(f"Max file size: {formats.max_file_size}")
   ```

### Getting Help

- **Documentation**: [https://docs.secureai.com](https://docs.secureai.com)
- **GitHub Issues**: [https://github.com/secureai/secureai-sdk/issues](https://github.com/secureai/secureai-sdk/issues)
- **Support**: support@secureai.com

---

**Ready to get started?** Install the SDK and try the quick start example above! 