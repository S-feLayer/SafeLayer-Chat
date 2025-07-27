# AI Privacy Shield - Secure AI MCP Integration Guide

## Overview
This guide explains how to integrate Secure AI MCP into your AI Privacy Shield product.

## Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/postralai/secureai.git
cd secureai

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your TINFOIL_API_KEY
```

### 2. Basic Usage
```python
from secureai import redact_text, redact_content

# Redact text content
result = redact_text("Hello, my email is john.doe@example.com")
print(result["redacted_text"])

# Redact file content
result = redact_content("path/to/sensitive/file.pdf")
print(result["redacted_file_path"])
```

### 3. MCP Server Integration
```python
# Start MCP server
python src/secureai/mcp_universal_redaction.py

# Configure Claude Desktop
# Add to claude_desktop_config.json:
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

## API Reference

### Text Redaction
```python
redact_text(text: str, use_ai: bool = True) -> dict
```

### File Redaction
```python
redact_content(file_path: str, tinfoil_llm=None) -> dict
```

### PDF Redaction
```python
redact_pdf(pdf_path: str, output_path: str = None) -> dict
```

## Configuration

### Environment Variables
- `TINFOIL_API_KEY`: Your Tinfoil API key
- `SECUREAI_ENV`: Environment (development/production)
- `SECUREAI_LOG_LEVEL`: Logging level
- `SECUREAI_CACHE_DIR`: Cache directory

### Production Settings
- Enable logging to file
- Set up monitoring with Prometheus
- Configure rate limiting
- Set up health checks

## Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Metrics
```bash
curl http://localhost:8000/metrics
```

### Logs
```bash
tail -f logs/secureai.log
```

## Troubleshooting

### Common Issues
1. **Permission Errors**: Run as administrator on Windows
2. **API Key Issues**: Verify Tinfoil API key is valid
3. **Memory Issues**: Process large files in chunks
4. **Performance Issues**: Use regex-only mode for high volume

### Support
- Check logs in `logs/secureai.log`
- Review monitoring metrics
- Contact support team
