# Testing Guide for Secure AI

This guide covers how to test the Secure AI universal redaction system effectively, including unit tests, integration tests, performance benchmarks, and manual testing procedures.

## 🧪 Testing Overview

Secure AI includes multiple testing approaches to ensure reliability, performance, and correctness:

1. **Unit Tests**: Test individual components and functions
2. **Integration Tests**: Test complete workflows end-to-end
3. **Performance Benchmarks**: Measure speed and efficiency
4. **Manual Testing**: Interactive testing with real content

## 📋 Prerequisites

Before running tests, ensure you have:

1. **Python Environment**: Python 3.10-3.12
2. **Dependencies**: All required packages installed
3. **Tinfoil API Key**: Set as environment variable `TINFOIL_API_KEY`
4. **Test Data**: Sample files for testing (optional)

### Setting up Tinfoil API Key

```bash
# Set environment variable
export TINFOIL_API_KEY="your_api_key_here"

# Or on Windows
set TINFOIL_API_KEY=your_api_key_here
```

## 🚀 Quick Start Testing

### 1. Basic Functionality Test

Run the basic test suite to verify core functionality:

```bash
cd src/scripts
python test_universal_redaction.py
```

This will test:
- Module imports
- Content type detection
- Supported formats
- Language detection
- Basic redaction functionality

### 2. Comprehensive Test Suite

Run the full test suite with detailed results:

```bash
python comprehensive_test_suite.py
```

This includes:
- All basic tests
- Text redaction tests
- Code redaction tests
- Edge case handling
- Performance validation

### 3. Integration Testing

Test complete workflows:

```bash
python integration_test.py
```

This tests:
- End-to-end workflows
- File processing
- Error handling
- Result validation

### 4. Performance Benchmarking

Measure system performance:

```bash
python performance_benchmark.py
```

This benchmarks:
- Processing speed
- Memory usage
- Scalability
- Efficiency metrics

## 📊 Test Categories

### Unit Tests

Unit tests focus on individual components:

#### Content Type Detection
```python
from secureai.redact_content import detect_content_type

# Test PDF detection
assert detect_content_type("document.pdf") == "pdf"

# Test code detection
assert detect_content_type("script.py") == "code"

# Test text detection
assert detect_content_type("This is text") == "text"
```

#### Language Detection
```python
from secureai.redact_code import detect_language

# Test various file types
assert detect_language("script.py") == "python"
assert detect_language("app.js") == "javascript"
assert detect_language("Main.java") == "java"
```

#### Supported Formats
```python
from secureai import get_supported_formats

formats = get_supported_formats()
assert "pdf" in formats
assert "code" in formats
assert "text" in formats
```

### Integration Tests

Integration tests verify complete workflows:

#### Text Redaction Workflow
```python
from secureai import redact_text
from secureai.tinfoil_llm import TinfoilLLM

tinfoil_llm = TinfoilLLM()
text = "Hello John Doe, my email is john@example.com"

result = redact_text(text, tinfoil_llm)
assert result["success"] == True
assert result["redaction_result"]["redaction_count"] > 0
```

#### Code Redaction Workflow
```python
from secureai import redact_code_file

# Create test file
with open("test_config.py", "w") as f:
    f.write('API_KEY = "sk-test123"')

result = redact_code_file("test_config.py", tinfoil_llm)
assert result["success"] == True
assert result["redaction_result"]["language"] == "python"
```

#### Universal Redaction Workflow
```python
from secureai import redact_content

# Test with text
result = redact_content("Hello John", tinfoil_llm)
assert result["content_type"] == "text"

# Test with file
result = redact_content("test_config.py", tinfoil_llm)
assert result["content_type"] == "code"
```

### Performance Tests

Performance tests measure efficiency:

#### Speed Testing
```python
import time

start_time = time.time()
result = redact_content(large_text, tinfoil_llm)
duration = time.time() - start_time

assert duration < 30  # Should complete within 30 seconds
```

#### Memory Testing
```python
import psutil
process = psutil.Process()

memory_before = process.memory_info().rss
result = redact_content(large_content, tinfoil_llm)
memory_after = process.memory_info().rss

memory_used = memory_after - memory_before
assert memory_used < 500 * 1024 * 1024  # Less than 500MB
```

## 🔍 Manual Testing

### 1. Text Content Testing

Test with various text inputs:

```bash
# Simple text
python -c "
from secureai import redact_text
from secureai.tinfoil_llm import TinfoilLLM
tinfoil_llm = TinfoilLLM()
result = redact_text('Hello John, my email is john@example.com', tinfoil_llm)
print(result)
"
```

### 2. Code File Testing

Test with different code files:

```bash
# Create test files
echo 'API_KEY = "sk-test123"' > test_config.py
echo 'const config = { apiKey: "sk-test456" };' > test_config.js

# Test Python file
python -c "
from secureai import redact_code_file
from secureai.tinfoil_llm import TinfoilLLM
tinfoil_llm = TinfoilLLM()
result = redact_code_file('test_config.py', tinfoil_llm)
print(result)
"
```

### 3. PDF Testing

Test with PDF files (if available):

```bash
# Test PDF redaction
python -c "
from secureai import redact_pdf
from secureai.tinfoil_llm import TinfoilLLM
tinfoil_llm = TinfoilLLM()
result = redact_pdf('test_document.pdf', tinfoil_llm)
print(result)
"
```

## 🐛 Debugging Tests

### Common Issues

#### 1. Tinfoil API Key Not Set
```
Error: TINFOIL_API_KEY environment variable not set
```
**Solution**: Set the environment variable:
```bash
export TINFOIL_API_KEY="your_api_key_here"
```

#### 2. Import Errors
```
ImportError: No module named 'secureai'
```
**Solution**: Ensure you're in the correct directory:
```bash
cd src/scripts
python -c "import sys; sys.path.insert(0, '..'); import secureai"
```

#### 3. File Permission Errors
```
PermissionError: [Errno 13] Permission denied
```
**Solution**: Check file permissions and ensure write access to test directories.

#### 4. Memory Issues
```
MemoryError: Unable to allocate memory
```
**Solution**: Reduce test content size or increase system memory.

### Debug Mode

Enable debug output for detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run tests with debug output
from secureai import redact_content
result = redact_content(test_data, tinfoil_llm)
```

## 📈 Performance Testing

### Benchmarking Guidelines

1. **Baseline Testing**: Run benchmarks on a clean system
2. **Multiple Iterations**: Run each test multiple times for accuracy
3. **Resource Monitoring**: Monitor CPU, memory, and disk usage
4. **Scalability Testing**: Test with different content sizes

### Performance Metrics

- **Processing Speed**: Time per MB of content
- **Memory Efficiency**: MB used per MB processed
- **Throughput**: MB processed per second
- **Latency**: Time to first result

### Expected Performance

| Content Type | Size | Expected Time | Memory Usage |
|--------------|------|---------------|--------------|
| Text | 1KB | < 1s | < 50MB |
| Text | 1MB | < 10s | < 200MB |
| Code | 1KB | < 2s | < 100MB |
| Code | 1MB | < 15s | < 300MB |
| PDF | 1MB | < 30s | < 500MB |

## 🔧 Continuous Integration

### Automated Testing

Set up CI/CD pipeline:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        cd src/scripts
        python test_universal_redaction.py
        python comprehensive_test_suite.py
      env:
        TINFOIL_API_KEY: ${{ secrets.TINFOIL_API_KEY }}
```

### Test Coverage

Monitor test coverage:

```bash
pip install coverage
coverage run -m pytest tests/
coverage report
coverage html  # Generate HTML report
```

## 📋 Test Checklist

### Before Release

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Performance benchmarks meet targets
- [ ] Manual testing completed
- [ ] Error handling tested
- [ ] Edge cases covered
- [ ] Documentation updated
- [ ] Security testing completed

### Regular Testing

- [ ] Run basic tests daily
- [ ] Run full test suite weekly
- [ ] Performance benchmarks monthly
- [ ] Security audit quarterly

## 🚨 Troubleshooting

### Test Failures

1. **Check Environment**: Verify Python version and dependencies
2. **Verify API Key**: Ensure Tinfoil API key is valid and set
3. **Check Logs**: Review error messages and debug output
4. **Isolate Issues**: Run individual tests to identify problems
5. **Update Dependencies**: Ensure all packages are up to date

### Performance Issues

1. **Monitor Resources**: Check CPU, memory, and disk usage
2. **Optimize Content**: Reduce test content size
3. **Check Network**: Verify API connectivity
4. **System Resources**: Ensure adequate system resources

### Security Testing

1. **Input Validation**: Test with malicious inputs
2. **Output Validation**: Verify redaction effectiveness
3. **API Security**: Test API key handling
4. **Data Privacy**: Ensure sensitive data is properly masked

## 📞 Getting Help

If you encounter issues:

1. **Check Documentation**: Review this guide and other docs
2. **Search Issues**: Look for similar problems in GitHub issues
3. **Run Debug Mode**: Enable detailed logging
4. **Create Minimal Test**: Reproduce issue with minimal code
5. **Report Bug**: Create detailed bug report with steps to reproduce

## 🎯 Best Practices

1. **Test Early, Test Often**: Run tests frequently during development
2. **Automate Everything**: Use CI/CD for automated testing
3. **Monitor Performance**: Track performance metrics over time
4. **Document Issues**: Keep detailed records of problems and solutions
5. **Update Tests**: Maintain tests as features evolve
6. **Security First**: Always test security aspects
7. **User Feedback**: Incorporate real-world usage feedback 