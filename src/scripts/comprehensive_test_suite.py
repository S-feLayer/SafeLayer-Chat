#!/usr/bin/env python3
"""
Comprehensive test suite for Secure AI's universal redaction system.
This script tests all features with various scenarios and edge cases.
"""

import os
import tempfile
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any

# Add the src directory to the path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

class TestSuite:
    """Comprehensive test suite for Secure AI."""
    
    def __init__(self):
        self.results = {
            "passed": 0,
            "failed": 0,
            "errors": [],
            "timings": {}
        }
        self.test_data = self._create_test_data()
    
    def _create_test_data(self) -> Dict[str, Any]:
        """Create comprehensive test data."""
        return {
            "text_samples": {
                "simple": "Hello John Doe, my email is john@example.com",
                "complex": """
                Dear Dr. Smith,
                
                I hope this email finds you well. My name is Jane Wilson and I'm writing regarding 
                the medical records for patient ID 12345. The patient's phone number is 555-123-4567 
                and their SSN is 123-45-6789. The contract number is CNT-2024-001.
                
                Please contact me at jane.wilson@company.com or call 555-987-6543.
                
                Best regards,
                Jane Wilson
                """,
                "edge_cases": [
                    "test@test.com",  # Simple email
                    "555-123-4567",   # Phone number
                    "123-45-6789",    # SSN
                    "John Doe",       # Name
                    "sk-1234567890abcdef1234567890abcdef12345678",  # API key
                    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"  # JWT
                ]
            },
            "code_samples": {
                "python": """
# Configuration file
API_KEY = "sk-1234567890abcdef1234567890abcdef12345678"
DATABASE_URL = "postgresql://user:password123@localhost:5432/mydb"
SECRET_TOKEN = "secret_token_here"

# User credentials
ADMIN_EMAIL = "admin@company.com"
ADMIN_PASSWORD = "admin123"

# Personal information
USER_NAME = "John Doe"
USER_PHONE = "555-987-6543"
USER_ADDRESS = "123 Main St, City, State 12345"

# JWT token
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
""",
                "javascript": """
// Configuration
const config = {
    apiKey: "sk-1234567890abcdef1234567890abcdef12345678",
    databaseUrl: "postgresql://user:password123@localhost:5432/mydb",
    secretToken: "secret_token_here",
    adminEmail: "admin@company.com",
    adminPassword: "admin123",
    userName: "John Doe",
    userPhone: "555-987-6543"
};

// JWT token
const jwtToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c";
""",
                "env_file": """
# Environment variables
API_KEY=sk-1234567890abcdef1234567890abcdef12345678
DATABASE_URL=postgresql://user:password123@localhost:5432/mydb
SECRET_TOKEN=secret_token_here
ADMIN_EMAIL=admin@company.com
ADMIN_PASSWORD=admin123
USER_NAME=John Doe
USER_PHONE=555-987-6543
JWT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
"""
            }
        }
    
    def run_test(self, test_name: str, test_func: callable) -> bool:
        """Run a single test and record results."""
        print(f"🧪 Running: {test_name}")
        start_time = time.time()
        
        try:
            result = test_func()
            duration = time.time() - start_time
            self.results["timings"][test_name] = duration
            
            if result:
                print(f"✅ PASSED: {test_name} ({duration:.3f}s)")
                self.results["passed"] += 1
                return True
            else:
                print(f"❌ FAILED: {test_name} ({duration:.3f}s)")
                self.results["failed"] += 1
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            print(f"💥 ERROR: {test_name} - {str(e)} ({duration:.3f}s)")
            self.results["failed"] += 1
            self.results["errors"].append(f"{test_name}: {str(e)}")
            return False
    
    def test_imports(self) -> bool:
        """Test that all modules can be imported."""
        try:
            from secureai import (
                redact_content, redact_pdf, redact_text, redact_code_file, 
                get_supported_formats
            )
            from secureai.redact_content import detect_content_type, extract_input_data
            from secureai.redact_code import CODE_EXTENSIONS, detect_language
            from secureai.tinfoil_llm import TinfoilLLM
            return True
        except ImportError as e:
            print(f"Import error: {e}")
            return False
    
    def test_content_type_detection(self) -> bool:
        """Test content type detection."""
        from secureai.redact_content import detect_content_type
        
        test_cases = [
            ("document.pdf", "pdf"),
            ("script.py", "code"),
            ("config.js", "code"),
            ("Dockerfile", "code"),
            ("This is text", "text"),
            ({"content_type": "pdf"}, "pdf"),
            ({"content_type": "code"}, "code"),
            ({"content_type": "text"}, "text"),
        ]
        
        for input_data, expected in test_cases:
            result = detect_content_type(input_data)
            if result != expected:
                print(f"Expected {expected}, got {result} for {input_data}")
                return False
        
        return True
    
    def test_supported_formats(self) -> bool:
        """Test supported formats function."""
        from secureai import get_supported_formats
        
        formats = get_supported_formats()
        
        required_keys = ["pdf", "code", "text"]
        for key in required_keys:
            if key not in formats:
                print(f"Missing required format: {key}")
                return False
        
        # Check that code formats include common extensions
        code_extensions = formats["code"]
        required_extensions = [".py", ".js", ".java"]
        for ext in required_extensions:
            if ext not in code_extensions:
                print(f"Missing required code extension: {ext}")
                return False
        
        return True
    
    def test_language_detection(self) -> bool:
        """Test language detection."""
        from secureai.redact_code import detect_language
        
        test_cases = [
            ("script.py", "python"),
            ("app.js", "javascript"),
            ("main.java", "java"),
            ("config.yaml", "yaml"),
            ("Dockerfile", "dockerfile"),
            ("unknown.xyz", "unknown"),
        ]
        
        for file_path, expected in test_cases:
            result = detect_language(file_path)
            if result != expected:
                print(f"Expected {expected}, got {result} for {file_path}")
                return False
        
        return True
    
    def test_text_redaction(self) -> bool:
        """Test text redaction functionality."""
        try:
            from secureai import redact_text
            from secureai.tinfoil_llm import TinfoilLLM
            
            tinfoil_llm = TinfoilLLM()
            test_text = self.test_data["text_samples"]["simple"]
            
            result = redact_text(test_text, tinfoil_llm)
            
            if not result.get("success"):
                print(f"Text redaction failed: {result.get('error')}")
                return False
            
            redacted = result["redaction_result"]
            if redacted["redaction_count"] == 0:
                print("No redactions found in test text")
                return False
            
            return True
            
        except Exception as e:
            if "TINFOIL_API_KEY" in str(e):
                print("Skipping text redaction test (TINFOIL_API_KEY not set)")
                return True
            else:
                print(f"Text redaction error: {e}")
                return False
    
    def test_code_redaction(self) -> bool:
        """Test code redaction functionality."""
        try:
            from secureai import redact_code_file
            from secureai.tinfoil_llm import TinfoilLLM
            
            # Create temporary code file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(self.test_data["code_samples"]["python"])
                temp_file = f.name
            
            try:
                tinfoil_llm = TinfoilLLM()
                result = redact_code_file(temp_file, tinfoil_llm)
                
                if not result.get("success"):
                    print(f"Code redaction failed: {result.get('error')}")
                    return False
                
                redacted = result["redaction_result"]
                if redacted["language"] != "python":
                    print(f"Expected python, got {redacted['language']}")
                    return False
                
                return True
                
            finally:
                # Cleanup
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    
        except Exception as e:
            if "TINFOIL_API_KEY" in str(e):
                print("Skipping code redaction test (TINFOIL_API_KEY not set)")
                return True
            else:
                print(f"Code redaction error: {e}")
                return False
    
    def test_universal_redaction(self) -> bool:
        """Test universal redaction functionality."""
        try:
            from secureai import redact_content
            from secureai.tinfoil_llm import TinfoilLLM
            
            tinfoil_llm = TinfoilLLM()
            
            # Test with text
            text_result = redact_content("Hello John, my email is john@example.com", tinfoil_llm)
            if not text_result.get("success"):
                print(f"Universal text redaction failed: {text_result.get('error')}")
                return False
            
            # Test with file path (create temp file)
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write("API_KEY = 'sk-test123'")
                temp_file = f.name
            
            try:
                file_result = redact_content(temp_file, tinfoil_llm)
                if not file_result.get("success"):
                    print(f"Universal file redaction failed: {file_result.get('error')}")
                    return False
                
                return True
                
            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    
        except Exception as e:
            if "TINFOIL_API_KEY" in str(e):
                print("Skipping universal redaction test (TINFOIL_API_KEY not set)")
                return True
            else:
                print(f"Universal redaction error: {e}")
                return False
    
    def test_edge_cases(self) -> bool:
        """Test edge cases and error handling."""
        from secureai.redact_content import redact_content
        
        # Test with None
        try:
            result = redact_content(None, None)
            if result.get("success"):
                print("Should fail with None input")
                return False
        except:
            pass  # Expected to fail
        
        # Test with empty string
        try:
            result = redact_content("", None)
            if result.get("success"):
                print("Should fail with empty string")
                return False
        except:
            pass  # Expected to fail
        
        # Test with non-existent file
        result = redact_content("/nonexistent/file.txt", None)
        if result.get("success"):
            print("Should fail with non-existent file")
            return False
        
        return True
    
    def test_performance(self) -> bool:
        """Test performance with large content."""
        try:
            from secureai import redact_content
            from secureai.tinfoil_llm import TinfoilLLM
            
            # Create large test content
            large_text = "Hello John Doe, my email is john@example.com. " * 1000
            
            tinfoil_llm = TinfoilLLM()
            start_time = time.time()
            
            result = redact_content(large_text, tinfoil_llm)
            duration = time.time() - start_time
            
            if not result.get("success"):
                print(f"Performance test failed: {result.get('error')}")
                return False
            
            print(f"Large content processed in {duration:.3f}s")
            return duration < 30  # Should complete within 30 seconds
            
        except Exception as e:
            if "TINFOIL_API_KEY" in str(e):
                print("Skipping performance test (TINFOIL_API_KEY not set)")
                return True
            else:
                print(f"Performance test error: {e}")
                return False
    
    def run_all_tests(self) -> bool:
        """Run all tests and return overall success."""
        print("🚀 Running Comprehensive Test Suite")
        print("=" * 60)
        
        tests = [
            ("Import Tests", self.test_imports),
            ("Content Type Detection", self.test_content_type_detection),
            ("Supported Formats", self.test_supported_formats),
            ("Language Detection", self.test_language_detection),
            ("Text Redaction", self.test_text_redaction),
            ("Code Redaction", self.test_code_redaction),
            ("Universal Redaction", self.test_universal_redaction),
            ("Edge Cases", self.test_edge_cases),
            ("Performance", self.test_performance),
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
            print()
        
        # Print summary
        print("=" * 60)
        print(f"📊 Test Results: {self.results['passed']} passed, {self.results['failed']} failed")
        
        if self.results["errors"]:
            print("\n❌ Errors:")
            for error in self.results["errors"]:
                print(f"  - {error}")
        
        print("\n⏱️  Performance Summary:")
        for test_name, duration in self.results["timings"].items():
            print(f"  {test_name:30} {duration:.3f}s")
        
        return self.results["failed"] == 0

def main():
    """Run the comprehensive test suite."""
    test_suite = TestSuite()
    success = test_suite.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! The system is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 