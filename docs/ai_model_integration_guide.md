 # AI Model Integration Guide

This guide shows how to use Secure AI with Tinfoil for redaction before sending content to other AI models like ChatGPT, Grok, or Gemini.

## 🔄 **Workflow Overview**

```
Sensitive Content → Tinfoil Redaction → Clean Content → Other AI Models
```

### **Why This Approach?**

1. ** Privacy First**: Tinfoil redacts sensitive data before sending to other AI models
2. ** Data Leakage Prevention**: Ensures no PII reaches external AI services
3. ** AI Compatibility**: Works with any AI model (ChatGPT, Grok, Gemini, etc.)
4. ** Compliance**: Meets GDPR, HIPAA, SOX, and other regulatory requirements

##  **Quick Start**

### **Basic Integration Pattern**

```python
from secureai import redact_content
from secureai.tinfoil_llm import TinfoilLLM
import openai  # or any other AI library

# Initialize
tinfoil_llm = TinfoilLLM()

# Step 1: Redact sensitive content with Tinfoil
sensitive_content = "Hi John Doe, my email is john@example.com and phone is 555-123-4567"
redaction_result = redact_content(sensitive_content, tinfoil_llm)

if redaction_result["success"]:
    # Step 2: Send redacted content to other AI models
    redacted_content = redaction_result["redaction_result"]["redacted_text"]
    
    # Now safe to send to any AI model
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": redacted_content}]
    )
    
    print("AI Analysis:", response.choices[0].message.content)
```

## 🤖 **Integration Examples**

### **1. ChatGPT Integration**

```python
import openai
from secureai import redact_content
from secureai.tinfoil_llm import TinfoilLLM

def analyze_with_chatgpt(sensitive_content: str, api_key: str) -> str:
    """
    Analyze sensitive content with ChatGPT after redaction.
    """
    # Initialize
    openai.api_key = api_key
    tinfoil_llm = TinfoilLLM()
    
    # Step 1: Redact with Tinfoil
    redaction_result = redact_content(sensitive_content, tinfoil_llm)
    
    if not redaction_result["success"]:
        return f"Redaction failed: {redaction_result['error']}"
    
    # Step 2: Send to ChatGPT
    redacted_content = redaction_result["redaction_result"]["redacted_text"]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant analyzing business documents."},
                {"role": "user", "content": redacted_content}
            ],
            max_tokens=1000
        )
        
        return {
            "analysis": response.choices[0].message.content,
            "redaction_summary": {
                "items_redacted": redaction_result["redaction_result"]["redaction_count"],
                "original_length": len(sensitive_content),
                "redacted_length": len(redacted_content)
            }
        }
        
    except Exception as e:
        return f"ChatGPT analysis failed: {str(e)}"

# Usage
sensitive_text = """
Hi team,
My name is Sarah Johnson (sarah.johnson@company.com) and my phone is 555-987-6543.
I'm working on project CNT-2024-001 with budget $150,000.
Our API key is sk-1234567890abcdef1234567890abcdef.
"""

result = analyze_with_chatgpt(sensitive_text, "your-openai-api-key")
print(result["analysis"])
```

### **2. Grok Integration**

```python
# Hypothetical Grok API (replace with actual implementation)
import grok_api
from secureai import redact_content
from secureai.tinfoil_llm import TinfoilLLM

def analyze_with_grok(sensitive_content: str, api_key: str) -> str:
    """
    Analyze sensitive content with Grok after redaction.
    """
    # Initialize
    grok_api.api_key = api_key
    tinfoil_llm = TinfoilLLM()
    
    # Step 1: Redact with Tinfoil
    redaction_result = redact_content(sensitive_content, tinfoil_llm)
    
    if not redaction_result["success"]:
        return f"Redaction failed: {redaction_result['error']}"
    
    # Step 2: Send to Grok
    redacted_content = redaction_result["redaction_result"]["redacted_text"]
    
    try:
        response = grok_api.analyze(
            content=redacted_content,
            analysis_type="business_intelligence"
        )
        
        return {
            "analysis": response.analysis,
            "sentiment": response.sentiment,
            "topics": response.topics,
            "redaction_summary": {
                "items_redacted": redaction_result["redaction_result"]["redaction_count"]
            }
        }
        
    except Exception as e:
        return f"Grok analysis failed: {str(e)}"
```

### **3. Gemini Integration**

```python
import google.generativeai as genai
from secureai import redact_content
from secureai.tinfoil_llm import TinfoilLLM

def analyze_with_gemini(sensitive_content: str, api_key: str) -> str:
    """
    Analyze sensitive content with Gemini after redaction.
    """
    # Initialize
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    tinfoil_llm = TinfoilLLM()
    
    # Step 1: Redact with Tinfoil
    redaction_result = redact_content(sensitive_content, tinfoil_llm)
    
    if not redaction_result["success"]:
        return f"Redaction failed: {redaction_result['error']}"
    
    # Step 2: Send to Gemini
    redacted_content = redaction_result["redaction_result"]["redacted_text"]
    
    try:
        response = model.generate_content(
            f"Analyze this business document: {redacted_content}"
        )
        
        return {
            "analysis": response.text,
            "redaction_summary": {
                "items_redacted": redaction_result["redaction_result"]["redaction_count"],
                "safety_score": "high"  # Content is now safe
            }
        }
        
    except Exception as e:
        return f"Gemini analysis failed: {str(e)}"
```

### **4. Claude Integration**

```python
import anthropic
from secureai import redact_content
from secureai.tinfoil_llm import TinfoilLLM

def analyze_with_claude(sensitive_content: str, api_key: str) -> str:
    """
    Analyze sensitive content with Claude after redaction.
    """
    # Initialize
    client = anthropic.Anthropic(api_key=api_key)
    tinfoil_llm = TinfoilLLM()
    
    # Step 1: Redact with Tinfoil
    redaction_result = redact_content(sensitive_content, tinfoil_llm)
    
    if not redaction_result["success"]:
        return f"Redaction failed: {redaction_result['error']}"
    
    # Step 2: Send to Claude
    redacted_content = redaction_result["redaction_result"]["redacted_text"]
    
    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this business document: {redacted_content}"
                }
            ]
        )
        
        return {
            "analysis": response.content[0].text,
            "redaction_summary": {
                "items_redacted": redaction_result["redaction_result"]["redaction_count"]
            }
        }
        
    except Exception as e:
        return f"Claude analysis failed: {str(e)}"
```

## 🔧 **Advanced Integration Patterns**

### **Multi-Model Analysis**

```python
def multi_model_analysis(sensitive_content: str, api_keys: dict) -> dict:
    """
    Analyze content with multiple AI models after redaction.
    """
    tinfoil_llm = TinfoilLLM()
    
    # Step 1: Redact once with Tinfoil
    redaction_result = redact_content(sensitive_content, tinfoil_llm)
    
    if not redaction_result["success"]:
        return {"error": f"Redaction failed: {redaction_result['error']}"}
    
    redacted_content = redaction_result["redaction_result"]["redacted_text"]
    results = {}
    
    # Step 2: Send to multiple AI models
    if "openai" in api_keys:
        results["chatgpt"] = analyze_with_chatgpt(redacted_content, api_keys["openai"])
    
    if "gemini" in api_keys:
        results["gemini"] = analyze_with_gemini(redacted_content, api_keys["gemini"])
    
    if "claude" in api_keys:
        results["claude"] = analyze_with_claude(redacted_content, api_keys["claude"])
    
    results["redaction_summary"] = {
        "items_redacted": redaction_result["redaction_result"]["redaction_count"],
        "original_length": len(sensitive_content),
        "redacted_length": len(redacted_content)
    }
    
    return results

# Usage
api_keys = {
    "openai": "your-openai-key",
    "gemini": "your-gemini-key",
    "claude": "your-claude-key"
}

results = multi_model_analysis(sensitive_content, api_keys)
```

### **Batch Processing**

```python
def batch_ai_analysis(content_list: list, ai_model: str, api_key: str) -> list:
    """
    Process multiple documents with AI analysis after redaction.
    """
    tinfoil_llm = TinfoilLLM()
    results = []
    
    for content in content_list:
        # Redact each document
        redaction_result = redact_content(content, tinfoil_llm)
        
        if redaction_result["success"]:
            redacted_content = redaction_result["redaction_result"]["redacted_text"]
            
            # Analyze with specified AI model
            if ai_model == "chatgpt":
                analysis = analyze_with_chatgpt(redacted_content, api_key)
            elif ai_model == "gemini":
                analysis = analyze_with_gemini(redacted_content, api_key)
            elif ai_model == "claude":
                analysis = analyze_with_claude(redacted_content, api_key)
            else:
                analysis = {"error": f"Unknown AI model: {ai_model}"}
            
            results.append({
                "original": content,
                "redacted": redacted_content,
                "analysis": analysis,
                "redaction_count": redaction_result["redaction_result"]["redaction_count"]
            })
        else:
            results.append({
                "original": content,
                "error": redaction_result["error"]
            })
    
    return results
```

### **Real-time Processing**

```python
import asyncio
import aiohttp
from secureai import redact_content
from secureai.tinfoil_llm import TinfoilLLM

async def real_time_ai_analysis(sensitive_content: str, ai_endpoint: str, api_key: str):
    """
    Real-time AI analysis with redaction.
    """
    tinfoil_llm = TinfoilLLM()
    
    # Step 1: Redact
    redaction_result = redact_content(sensitive_content, tinfoil_llm)
    
    if not redaction_result["success"]:
        return {"error": f"Redaction failed: {redaction_result['error']}"}
    
    redacted_content = redaction_result["redaction_result"]["redacted_text"]
    
    # Step 2: Async AI analysis
    async with aiohttp.ClientSession() as session:
        async with session.post(
            ai_endpoint,
            json={"content": redacted_content},
            headers={"Authorization": f"Bearer {api_key}"}
        ) as response:
            analysis = await response.json()
    
    return {
        "analysis": analysis,
        "redaction_summary": {
            "items_redacted": redaction_result["redaction_result"]["redaction_count"]
        }
    }
```

## 🛡️ **Security Best Practices**

### **1. API Key Management**

```python
import os
from dotenv import load_dotenv

# Load API keys from environment variables
load_dotenv()

api_keys = {
    "tinfoil": os.getenv("TINFOIL_API_KEY"),
    "openai": os.getenv("OPENAI_API_KEY"),
    "gemini": os.getenv("GEMINI_API_KEY"),
    "claude": os.getenv("CLAUDE_API_KEY")
}
```

### **2. Content Validation**

```python
def validate_content_for_ai(content: str) -> bool:
    """
    Validate that content is safe for AI processing.
    """
    # Check if content has been redacted
    if "***" in content or "[REDACTED]" in content:
        return True
    
    # Additional validation logic
    sensitive_patterns = [
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        r'\bsk-[a-zA-Z0-9]{20,}\b',  # API keys
    ]
    
    import re
    for pattern in sensitive_patterns:
        if re.search(pattern, content):
            return False
    
    return True
```

### **3. Audit Logging**

```python
import logging
from datetime import datetime

def log_ai_analysis(original_content: str, redacted_content: str, ai_model: str, analysis_result: dict):
    """
    Log AI analysis for audit purposes.
    """
    logging.info(f"""
    AI Analysis Log:
    Timestamp: {datetime.now()}
    AI Model: {ai_model}
    Original Length: {len(original_content)}
    Redacted Length: {len(redacted_content)}
    Analysis Success: {analysis_result.get('success', False)}
    """)
```

## 📊 **Performance Optimization**

### **1. Caching Redacted Content**

```python
import hashlib
import json
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_redaction(content_hash: str, content: str, tinfoil_llm):
    """
    Cache redaction results for repeated content.
    """
    return redact_content(content, tinfoil_llm)

def optimized_ai_analysis(content: str, ai_model: str, api_key: str):
    """
    Optimized analysis with caching.
    """
    tinfoil_llm = TinfoilLLM()
    
    # Create content hash for caching
    content_hash = hashlib.md5(content.encode()).hexdigest()
    
    # Get cached or new redaction
    redaction_result = cached_redaction(content_hash, content, tinfoil_llm)
    
    if redaction_result["success"]:
        # Proceed with AI analysis
        return analyze_with_model(redaction_result["redaction_result"]["redacted_text"], ai_model, api_key)
```

### **2. Parallel Processing**

```python
import concurrent.futures
from secureai import redact_content
from secureai.tinfoil_llm import TinfoilLLM

def parallel_ai_analysis(content_list: list, ai_models: list, api_keys: dict):
    """
    Process multiple documents with multiple AI models in parallel.
    """
    tinfoil_llm = TinfoilLLM()
    
    def process_single(content):
        # Redact content
        redaction_result = redact_content(content, tinfoil_llm)
        
        if not redaction_result["success"]:
            return {"error": redaction_result["error"]}
        
        redacted_content = redaction_result["redaction_result"]["redacted_text"]
        
        # Analyze with all AI models
        results = {}
        for model in ai_models:
            if model in api_keys:
                results[model] = analyze_with_model(redacted_content, model, api_keys[model])
        
        return results
    
    # Process in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_single, content_list))
    
    return results
```

## 🔍 **Troubleshooting**

### **Common Issues**

1. **Redaction Fails**
   - Check Tinfoil API key
   - Verify content format
   - Check network connectivity

2. **AI Model Errors**
   - Verify AI model API keys
   - Check rate limits
   - Validate content length

3. **Performance Issues**
   - Use caching for repeated content
   - Implement parallel processing
   - Consider content chunking

### **Debug Mode**

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug output
result = analyze_with_chatgpt(sensitive_content, api_key)
```

This integration approach ensures that sensitive data is always protected while enabling powerful AI analysis capabilities across multiple platforms. 