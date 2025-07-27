# PII Detection Guide

Secure AI provides comprehensive **PII (Personally Identifiable Information) detection** to prevent data leakage across all supported content types.

## 🛡️ **Data Leakage Prevention**

Secure AI acts as a **privacy firewall** that automatically detects and redacts sensitive information before it can be accidentally shared with AI models or other systems.

### **Why PII Detection Matters**

- **🔒 Privacy Protection**: Prevents accidental exposure of personal information
- **📋 Compliance**: Helps meet GDPR, HIPAA, SOX, and other regulatory requirements
- **🏢 Business Security**: Protects company secrets, API keys, and credentials
- **👤 Personal Safety**: Safeguards individual privacy in digital communications

## 🔍 **Detection Capabilities**

### **1. Pattern-Based Detection (Regex)**

Fast, rule-based detection for known PII formats:

#### **Personal Information**
- **📧 Email Addresses**: `john.doe@company.com`
- **📞 Phone Numbers**: `+1-555-123-4567`, `(555) 123-4567`
- **🆔 Social Security Numbers**: `123-45-6789`
- **💳 Credit Card Numbers**: `4111-1111-1111-1111`
- **🆔 UUIDs**: `550e8400-e29b-41d4-a716-446655440000`

#### **Technical Credentials**
- **🔑 API Keys**: `sk-1234567890abcdef...`, `ghp_1234567890...`
- **🎫 JWT Tokens**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- **☁️ AWS Keys**: `AKIA1234567890ABCDEF`
- **🔐 Private Keys**: `-----BEGIN RSA PRIVATE KEY-----`
- **🗄️ Database URLs**: `postgresql://user:pass@host:port/db`

#### **Network Information**
- **🌐 IP Addresses**: `192.168.1.1`
- **🔗 MAC Addresses**: `00:1B:44:11:3A:B7`

### **2. AI-Powered Detection**

Context-aware detection using Tinfoil's isolated AI (Llama 3.3 70B):

#### **PDF Documents**
```json
{
    "personal_names": ["John Doe", "Jane Smith"],
    "emails": ["john.doe@acme.com"],
    "phone_numbers": ["555-123-4567"],
    "addresses": ["123 Main Street, New York, NY 10001"],
    "social_security_numbers": ["123-45-6789"],
    "credit_card_numbers": ["4111-1111-1111-1111"],
    "account_numbers": ["9876543210"],
    "contract_numbers": ["CNT-2024-001"],
    "company_names": ["Acme Corporation"],
    "dates_of_birth": ["January 15, 1990"]
}
```

#### **Code Files**
```json
{
    "api_keys": ["sk-1234567890abcdef..."],
    "passwords": ["password123", "super_secret_password"],
    "database_credentials": ["postgresql://user:pass@localhost:5432/mydb"],
    "private_keys": ["-----BEGIN RSA PRIVATE KEY-----"],
    "access_tokens": ["ghp_1234567890abcdef..."],
    "personal_info": ["john.doe@company.com"],
    "company_secrets": ["internal_api_key"],
    "environment_variables": ["SECRET_PASSWORD"],
    "config_secrets": ["database_password"]
}
```

#### **Text Content**
```json
{
    "personal_names": ["Jane Smith"],
    "emails": ["jane.smith@techcorp.com"],
    "phone_numbers": ["+1-555-987-6543"],
    "addresses": ["456 Business Ave, San Francisco, CA 94102"],
    "social_security_numbers": [],
    "credit_card_numbers": [],
    "account_numbers": [],
    "contract_numbers": ["CNT-2024-002"],
    "company_names": ["Tech Solutions Inc."],
    "dates_of_birth": [],
    "api_keys": [],
    "passwords": []
}
```

## 🚀 **Usage Examples**

### **Basic PII Detection**

```python
from secureai.enhanced_detection import EnhancedDetection
from secureai.tinfoil_llm import TinfoilLLM

# Initialize
tinfoil_llm = TinfoilLLM()
detector = EnhancedDetection(tinfoil_llm)

# Detect PII in text
text = "Hi John Doe, my email is john@example.com and phone is 555-123-4567"
detected = detector.detect_sensitive_data(text, "text")

print("Detected PII:")
for data_type, values in detected.items():
    if values:
        print(f"  {data_type}: {values}")
```

### **Content-Specific Detection**

```python
# PDF content
pdf_text = """
CONTRACT AGREEMENT
Between John Doe (john.doe@acme.com) and Acme Corporation.
Customer ID: CUST-12345
Social Security Number: 123-45-6789
"""
pdf_pii = detector.detect_sensitive_data(pdf_text, "pdf")

# Code content
code_text = """
API_KEY = "sk-1234567890abcdef1234567890abcdef"
DATABASE_URL = "postgresql://user:password@localhost:5432/db"
"""
code_pii = detector.detect_sensitive_data(code_text, "code")
```

### **Pattern-Only Detection**

```python
# Fast pattern-based detection (no AI required)
patterns_only = detector.detect_with_patterns(text)
print("Pattern-based PII:", patterns_only)
```

### **AI-Only Detection**

```python
# AI-powered detection (requires Tinfoil API key)
ai_only = detector.detect_with_ai(text, "text")
print("AI-detected PII:", ai_only)
```

## 🎯 **Detection Strategies**

### **1. Combined Detection (Recommended)**

Uses both pattern matching and AI for maximum coverage:

```python
# Best for comprehensive detection
detected = detector.detect_sensitive_data(text, content_type)
```

**Benefits:**
- ✅ Maximum PII coverage
- ✅ Handles both structured and unstructured data
- ✅ Context-aware detection
- ✅ Validates and filters results

### **2. Pattern-Only Detection**

Fast detection for known formats:

```python
# Fast, no API calls required
detected = detector.detect_with_patterns(text)
```

**Benefits:**
- ⚡ Very fast processing
- 🔒 No external API calls
- 💰 No additional costs
- 🎯 High accuracy for known formats

### **3. AI-Only Detection**

Context-aware detection for complex scenarios:

```python
# Context-aware detection
detected = detector.detect_with_ai(text, content_type)
```

**Benefits:**
- 🧠 Context-aware detection
- 🔍 Finds unstructured PII
- 🎯 Handles edge cases
- 📊 Detailed categorization

## ✅ **Validation and Filtering**

The system automatically validates detected PII:

```python
# Raw detection
raw_detected = detector.detect_sensitive_data(text, "text")

# Validated detection (filters out false positives)
validated = detector.validate_detection(raw_detected)
```

**Validation includes:**
- ✅ Removes empty or invalid values
- ✅ Filters based on data type rules
- ✅ Ensures minimum length requirements
- ✅ Validates format compliance

## 🔧 **Customization**

### **Adding Custom Patterns**

```python
# Add custom regex patterns
detector.patterns['custom_id'] = r'\bCUST-\d{5}\b'
detector.patterns['employee_id'] = r'\bEMP-\d{5}\b'

# Detect with custom patterns
detected = detector.detect_with_patterns(text)
```

### **Custom Validation Rules**

```python
# Extend validation for custom data types
def custom_validation(detector, data_type, value):
    if data_type == 'custom_id':
        return value.startswith('CUST-') and len(value) == 10
    return True

# Use in validation
validated = detector.validate_detection(detected)
```

## 📊 **Detection Performance**

### **Speed Comparison**

| Method | Speed | Accuracy | Coverage |
|--------|-------|----------|----------|
| Pattern-only | ⚡⚡⚡⚡⚡ | High | Medium |
| AI-only | ⚡⚡ | Very High | High |
| Combined | ⚡⚡⚡ | Very High | Very High |

### **Content Type Performance**

| Content Type | Pattern Speed | AI Speed | Combined Speed |
|--------------|---------------|----------|----------------|
| Text (short) | < 10ms | 500-1000ms | 500-1000ms |
| Text (long) | < 50ms | 1000-2000ms | 1000-2000ms |
| Code files | < 20ms | 500-1500ms | 500-1500ms |
| PDF text | < 100ms | 1000-3000ms | 1000-3000ms |

## 🛡️ **Security Features**

### **Data Protection**

- **🔒 Local Processing**: All detection happens on your machine
- **🌐 Isolated AI**: Uses Tinfoil's secure enclaves
- **🚫 No Data Transmission**: Sensitive data never leaves your system
- **🔄 Reversible**: Original data is preserved, only masked

### **Privacy Compliance**

- **📋 GDPR**: Protects personal data processing
- **🏥 HIPAA**: Safeguards medical information
- **💼 SOX**: Secures financial data
- **🔐 SOC 2**: Maintains data security standards

## 🚨 **Best Practices**

### **1. Always Use Combined Detection**

```python
# Recommended approach
detected = detector.detect_sensitive_data(content, content_type)
```

### **2. Validate Results**

```python
# Always validate detected PII
validated = detector.validate_detection(detected)
```

### **3. Handle Errors Gracefully**

```python
try:
    detected = detector.detect_sensitive_data(text, "text")
except Exception as e:
    print(f"Detection failed: {e}")
    # Fall back to pattern-only detection
    detected = detector.detect_with_patterns(text)
```

### **4. Monitor Detection Quality**

```python
# Track detection performance
raw_count = len(detector.detect_with_patterns(text))
ai_count = len(detector.detect_with_ai(text, "text"))
combined_count = len(detector.detect_sensitive_data(text, "text"))

print(f"Pattern: {raw_count}, AI: {ai_count}, Combined: {combined_count}")
```

## 🔍 **Troubleshooting**

### **Common Issues**

1. **No PII Detected**
   - Check if content contains actual PII
   - Verify Tinfoil API key is set
   - Try pattern-only detection first

2. **False Positives**
   - Use validation to filter results
   - Review detected patterns
   - Adjust custom patterns if needed

3. **Slow Detection**
   - Use pattern-only for large files
   - Consider chunking content
   - Check network connectivity for AI calls

### **Debug Mode**

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run detection with debug output
detected = detector.detect_sensitive_data(text, "text")
```

## 📈 **Advanced Usage**

### **Batch Processing**

```python
def batch_detect_pii(content_list, content_type="text"):
    results = []
    for content in content_list:
        detected = detector.detect_sensitive_data(content, content_type)
        validated = detector.validate_detection(detected)
        results.append(validated)
    return results
```

### **Real-time Detection**

```python
def monitor_text_input(text):
    # Quick pattern check first
    patterns = detector.detect_with_patterns(text)
    if patterns:
        # Full detection if patterns found
        full_detection = detector.detect_sensitive_data(text, "text")
        return full_detection
    return {}
```

This comprehensive PII detection system ensures that sensitive information is automatically identified and protected, preventing accidental data leakage across all your content processing workflows. 