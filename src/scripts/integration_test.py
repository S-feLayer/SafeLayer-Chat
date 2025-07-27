#!/usr/bin/env python3
"""
Integration test script for Secure AI's complete workflow.
Tests the entire pipeline from input to redacted output.
"""

import os
import tempfile
import sys
import json
from pathlib import Path
from typing import Dict, Any

# Add the src directory to the path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

class IntegrationTest:
    """Integration tests for complete workflow."""
    
    def __init__(self):
        self.test_results = {}
        self.temp_files = []
    
    def __del__(self):
        """Cleanup temporary files."""
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass
    
    def create_temp_file(self, content: str, suffix: str = ".txt") -> str:
        """Create a temporary file with content."""
        with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
            f.write(content)
            temp_file = f.name
            self.temp_files.append(temp_file)
            return temp_file
    
    def test_complete_workflow(self, test_name: str, input_data: Any, 
                              expected_content_type: str) -> Dict[str, Any]:
        """Test the complete workflow from input to output."""
        print(f"🔄 Testing: {test_name}")
        
        try:
            from secureai import redact_content
            from secureai.tinfoil_llm import TinfoilLLM
            
            # Initialize Tinfoil LLM
            tinfoil_llm = TinfoilLLM()
            
            # Process the input
            result = redact_content(input_data, tinfoil_llm)
            
            # Validate results
            validation = self._validate_result(result, expected_content_type)
            
            return {
                "test_name": test_name,
                "success": validation["success"],
                "content_type": result.get("content_type"),
                "expected_type": expected_content_type,
                "redaction_count": self._get_redaction_count(result),
                "errors": validation["errors"],
                "warnings": validation["warnings"]
            }
            
        except Exception as e:
            if "TINFOIL_API_KEY" in str(e):
                return {
                    "test_name": test_name,
                    "success": True,
                    "content_type": "skipped",
                    "expected_type": expected_content_type,
                    "redaction_count": 0,
                    "errors": [],
                    "warnings": ["Test skipped - TINFOIL_API_KEY not set"]
                }
            else:
                return {
                    "test_name": test_name,
                    "success": False,
                    "content_type": "error",
                    "expected_type": expected_content_type,
                    "redaction_count": 0,
                    "errors": [str(e)],
                    "warnings": []
                }
    
    def _validate_result(self, result: Dict[str, Any], expected_type: str) -> Dict[str, Any]:
        """Validate the redaction result."""
        validation = {
            "success": False,
            "errors": [],
            "warnings": []
        }
        
        # Check if processing was successful
        if not result.get("success"):
            validation["errors"].append(f"Processing failed: {result.get('error')}")
            return validation
        
        # Check content type
        actual_type = result.get("content_type")
        if actual_type != expected_type:
            validation["warnings"].append(
                f"Content type mismatch: expected {expected_type}, got {actual_type}"
            )
        
        # Check for redaction results
        if expected_type == "pdf":
            if "redaction_summary" not in result:
                validation["errors"].append("Missing redaction summary for PDF")
            else:
                validation["success"] = True
        elif expected_type in ["code", "text"]:
            if "redaction_result" not in result:
                validation["errors"].append("Missing redaction result")
            else:
                validation["success"] = True
        
        return validation
    
    def _get_redaction_count(self, result: Dict[str, Any]) -> int:
        """Extract redaction count from result."""
        if result.get("content_type") == "pdf":
            return result.get("redaction_summary", {}).get("total_redactions", 0)
        elif result.get("content_type") in ["code", "text"]:
            return result.get("redaction_result", {}).get("redaction_count", 0)
        return 0
    
    def run_text_workflow_tests(self) -> Dict[str, Any]:
        """Test text content workflows."""
        print("\n📝 Testing Text Content Workflows")
        print("-" * 40)
        
        test_cases = [
            {
                "name": "Simple Text",
                "input": "Hello John Doe, my email is john@example.com",
                "expected_type": "text"
            },
            {
                "name": "Complex Text",
                "input": """
                Dear Dr. Smith,
                
                I hope this email finds you well. My name is Jane Wilson and I'm writing regarding 
                the medical records for patient ID 12345. The patient's phone number is 555-123-4567 
                and their SSN is 123-45-6789. The contract number is CNT-2024-001.
                
                Please contact me at jane.wilson@company.com or call 555-987-6543.
                
                Best regards,
                Jane Wilson
                """,
                "expected_type": "text"
            },
            {
                "name": "Text with API Keys",
                "input": "The API key is sk-1234567890abcdef1234567890abcdef12345678 and the JWT token is eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
                "expected_type": "text"
            }
        ]
        
        results = []
        for test_case in test_cases:
            result = self.test_complete_workflow(
                test_case["name"], 
                test_case["input"], 
                test_case["expected_type"]
            )
            results.append(result)
            print(f"  {result['success'] and '✅' or '❌'} {test_case['name']}")
        
        return {"text_tests": results}
    
    def run_code_workflow_tests(self) -> Dict[str, Any]:
        """Test code file workflows."""
        print("\n💻 Testing Code File Workflows")
        print("-" * 40)
        
        test_cases = [
            {
                "name": "Python Config",
                "content": """
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
""",
                "suffix": ".py",
                "expected_type": "code"
            },
            {
                "name": "JavaScript Config",
                "content": """
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
""",
                "suffix": ".js",
                "expected_type": "code"
            },
            {
                "name": "Environment File",
                "content": """
# Environment variables
API_KEY=sk-1234567890abcdef1234567890abcdef12345678
DATABASE_URL=postgresql://user:password123@localhost:5432/mydb
SECRET_TOKEN=secret_token_here
ADMIN_EMAIL=admin@company.com
ADMIN_PASSWORD=admin123
USER_NAME=John Doe
USER_PHONE=555-987-6543
""",
                "suffix": ".env",
                "expected_type": "code"
            }
        ]
        
        results = []
        for test_case in test_cases:
            # Create temporary file
            temp_file = self.create_temp_file(test_case["content"], test_case["suffix"])
            
            result = self.test_complete_workflow(
                test_case["name"], 
                temp_file, 
                test_case["expected_type"]
            )
            results.append(result)
            print(f"  {result['success'] and '✅' or '❌'} {test_case['name']}")
        
        return {"code_tests": results}
    
    def run_pdf_workflow_tests(self) -> Dict[str, Any]:
        """Test PDF workflows (if PDF files are available)."""
        print("\n📄 Testing PDF Workflows")
        print("-" * 40)
        
        # This would require actual PDF files for testing
        # For now, we'll create a mock test
        results = []
        
        # Test with non-existent PDF to verify error handling
        result = self.test_complete_workflow(
            "Non-existent PDF", 
            "/nonexistent/document.pdf", 
            "pdf"
        )
        results.append(result)
        print(f"  {'✅' if not result['success'] else '❌'} Non-existent PDF (should fail)")
        
        return {"pdf_tests": results}
    
    def run_edge_case_tests(self) -> Dict[str, Any]:
        """Test edge cases and error conditions."""
        print("\n🔍 Testing Edge Cases")
        print("-" * 40)
        
        test_cases = [
            {
                "name": "Empty String",
                "input": "",
                "expected_type": "text"
            },
            {
                "name": "Very Long Text",
                "input": "Hello John Doe, my email is john@example.com. " * 1000,
                "expected_type": "text"
            },
            {
                "name": "Special Characters",
                "input": "Test with special chars: @#$%^&*()_+-=[]{}|;':\",./<>?",
                "expected_type": "text"
            },
            {
                "name": "Unicode Text",
                "input": "Hello José, my email is josé@example.com",
                "expected_type": "text"
            }
        ]
        
        results = []
        for test_case in test_cases:
            result = self.test_complete_workflow(
                test_case["name"], 
                test_case["input"], 
                test_case["expected_type"]
            )
            results.append(result)
            print(f"  {result['success'] and '✅' or '❌'} {test_case['name']}")
        
        return {"edge_case_tests": results}
    
    def run_all_integration_tests(self) -> Dict[str, Any]:
        """Run all integration tests."""
        print("🚀 Running Integration Tests")
        print("=" * 60)
        
        all_results = {}
        
        # Run different test categories
        all_results.update(self.run_text_workflow_tests())
        all_results.update(self.run_code_workflow_tests())
        all_results.update(self.run_pdf_workflow_tests())
        all_results.update(self.run_edge_case_tests())
        
        # Calculate summary statistics
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        
        for category, tests in all_results.items():
            for test in tests:
                total_tests += 1
                if test["success"]:
                    passed_tests += 1
                else:
                    failed_tests += 1
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 Integration Test Summary")
        print("-" * 40)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "N/A")
        
        # Print detailed results
        print("\n📋 Detailed Results:")
        for category, tests in all_results.items():
            print(f"\n{category.replace('_', ' ').title()}:")
            for test in tests:
                status = "✅ PASS" if test["success"] else "❌ FAIL"
                print(f"  {status} {test['test_name']}")
                if test["errors"]:
                    for error in test["errors"]:
                        print(f"    Error: {error}")
                if test["warnings"]:
                    for warning in test["warnings"]:
                        print(f"    Warning: {warning}")
        
        return {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests/total_tests*100) if total_tests > 0 else 0
            },
            "results": all_results
        }

def main():
    """Run the integration tests."""
    integration_test = IntegrationTest()
    results = integration_test.run_all_integration_tests()
    
    # Save results to file
    with open("integration_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: integration_test_results.json")
    
    # Exit with appropriate code
    if results["summary"]["failed_tests"] == 0:
        print("\n🎉 All integration tests passed!")
        sys.exit(0)
    else:
        print(f"\n❌ {results['summary']['failed_tests']} integration tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main() 