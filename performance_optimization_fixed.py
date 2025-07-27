#!/usr/bin/env python3
"""
Performance Optimization Script for SecureAI MCP

This script helps optimize SecureAI for specific use cases by:
1. Testing different configurations
2. Benchmarking performance
3. Optimizing for specific content types
4. Fine-tuning for production deployment
"""

import os
import sys
import time
import json
import psutil
from datetime import datetime
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_basic_redaction_performance():
    """Test basic redaction performance without AI."""
    print("Testing Basic Redaction Performance")
    print("=" * 50)
    
    try:
        from secureai import redact_text
        
        # Test data
        test_cases = [
            {
                "name": "Simple Text",
                "content": "Hello, my name is John Doe and my email is john.doe@example.com",
                "expected_entities": ["name", "email"]
            },
            {
                "name": "Code with API Keys",
                "content": """
                const apiKey = "sk-1234567890abcdef";
                const password = "secret123";
                const config = {
                    database: "prod_db",
                    user: "admin"
                };
                """,
                "expected_entities": ["api_key", "password", "database", "user"]
            },
            {
                "name": "Large Document",
                "content": "This is a large document. " * 1000 + "My email is test@example.com",
                "expected_entities": ["email"]
            }
        ]
        
        results = []
        for test_case in test_cases:
            start_time = time.time()
            result = redact_text(test_case["content"], use_ai=False)
            end_time = time.time()
            
            processing_time = end_time - start_time
            text_length = len(test_case["content"])
            chars_per_second = text_length / processing_time if processing_time > 0 else 0
            
            results.append({
                "test_name": test_case["name"],
                "processing_time": processing_time,
                "text_length": text_length,
                "chars_per_second": chars_per_second,
                "redactions_found": len(result.get("redactions", []))
            })
            
            print(f"{test_case['name']}: {processing_time:.3f}s ({chars_per_second:.0f} chars/s)")
        
        return results
        
    except Exception as e:
        print(f"Basic redaction test failed: {e}")
        return []

def test_memory_usage():
    """Test memory usage during processing."""
    print("\nTesting Memory Usage")
    print("=" * 50)
    
    try:
        from secureai import redact_text
        
        # Get initial memory usage
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Process large content
        large_content = "This is test content with sensitive data. " * 10000
        large_content += "Email: test@example.com, Phone: 555-123-4567"
        
        start_time = time.time()
        result = redact_text(large_content, use_ai=False)
        end_time = time.time()
        
        # Get final memory usage
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"Initial memory: {initial_memory:.1f} MB")
        print(f"Final memory: {final_memory:.1f} MB")
        print(f"Memory increase: {memory_increase:.1f} MB")
        print(f"Processing time: {end_time - start_time:.3f}s")
        
        return {
            "initial_memory_mb": initial_memory,
            "final_memory_mb": final_memory,
            "memory_increase_mb": memory_increase,
            "processing_time": end_time - start_time
        }
        
    except Exception as e:
        print(f"Memory usage test failed: {e}")
        return {}

def test_concurrent_processing():
    """Test concurrent processing capabilities."""
    print("\nTesting Concurrent Processing")
    print("=" * 50)
    
    try:
        from secureai import redact_text
        import threading
        
        def process_text(text_id, content):
            start_time = time.time()
            result = redact_text(content, use_ai=False)
            end_time = time.time()
            return {
                "thread_id": text_id,
                "processing_time": end_time - start_time,
                "redactions": len(result.get("redactions", []))
            }
        
        # Test data
        test_contents = [
            f"Thread {i}: Hello, my name is User{i} and my email is user{i}@example.com"
            for i in range(5)
        ]
        
        # Process concurrently
        threads = []
        results = []
        
        start_time = time.time()
        for i, content in enumerate(test_contents):
            thread = threading.Thread(
                target=lambda i=i, content=content: results.append(process_text(i, content))
            )
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"Total processing time: {total_time:.3f}s")
        for result in results:
            print(f"Thread {result['thread_id']}: {result['processing_time']:.3f}s")
        
        return {
            "total_time": total_time,
            "thread_results": results,
            "average_time": sum(r["processing_time"] for r in results) / len(results)
        }
        
    except Exception as e:
        print(f"Concurrent processing test failed: {e}")
        return {}

def test_file_processing():
    """Test file processing performance."""
    print("\nTesting File Processing")
    print("=" * 50)
    
    try:
        from secureai import redact_content
        
        # Create test files
        test_files = []
        test_dir = Path("test_files")
        test_dir.mkdir(exist_ok=True)
        
        # Create different types of test files
        file_types = [
            ("text.txt", "This is a text file with sensitive data.\nEmail: test@example.com\nPhone: 555-123-4567"),
            ("code.py", """
import os
api_key = "sk-1234567890abcdef"
password = "secret123"
database_url = "postgresql://user:pass@localhost/db"
            """),
            ("config.json", """
{
    "database": {
        "host": "localhost",
        "user": "admin",
        "password": "secret123"
    },
    "api": {
        "key": "sk-1234567890abcdef"
    }
}
            """)
        ]
        
        for filename, content in file_types:
            file_path = test_dir / filename
            with open(file_path, 'w') as f:
                f.write(content)
            test_files.append(file_path)
        
        results = []
        for file_path in test_files:
            start_time = time.time()
            result = redact_content(str(file_path), tinfoil_llm=None)
            end_time = time.time()
            
            processing_time = end_time - start_time
            file_size = file_path.stat().st_size
            
            results.append({
                "filename": file_path.name,
                "processing_time": processing_time,
                "file_size_bytes": file_size,
                "bytes_per_second": file_size / processing_time if processing_time > 0 else 0,
                "redactions_found": len(result.get("redactions", []))
            })
            
            print(f"{file_path.name}: {processing_time:.3f}s ({file_size} bytes)")
        
        return results
        
    except Exception as e:
        print(f"File processing test failed: {e}")
        return []

def generate_optimization_report(results):
    """Generate optimization recommendations."""
    print("\nPerformance Optimization Report")
    print("=" * 50)
    
    # Basic redaction performance
    if results.get("basic_redaction"):
        basic_results = results["basic_redaction"]
        if basic_results:
            avg_chars_per_second = sum(r["chars_per_second"] for r in basic_results) / len(basic_results)
            print(f"Average processing speed: {avg_chars_per_second:.0f} characters/second")
            
            if avg_chars_per_second < 10000:
                print("Consider optimizing regex patterns for better performance")
            else:
                print("Basic redaction performance is good")
    
    # Memory usage
    if results.get("memory_usage"):
        memory_data = results["memory_usage"]
        if memory_data.get("memory_increase_mb", 0) > 100:
            print("High memory usage detected. Consider processing in smaller chunks")
        else:
            print("Memory usage is acceptable")
    
    # Concurrent processing
    if results.get("concurrent_processing"):
        concurrent_data = results["concurrent_processing"]
        if concurrent_data.get("total_time", 0) > concurrent_data.get("average_time", 0) * 2:
            print("Concurrent processing shows overhead. Consider sequential processing for small files")
        else:
            print("Concurrent processing is efficient")
    
    # File processing
    if results.get("file_processing"):
        file_results = results["file_processing"]
        if file_results:
            avg_bytes_per_second = sum(r["bytes_per_second"] for r in file_results) / len(file_results)
            print(f"Average file processing speed: {avg_bytes_per_second:.0f} bytes/second")
    
    # General recommendations
    print("\nOptimization Recommendations:")
    print("1. Use regex-only mode for high-volume processing")
    print("2. Process large files in chunks")
    print("3. Cache compiled regex patterns")
    print("4. Use concurrent processing for multiple files")
    print("5. Monitor memory usage for large documents")

def main():
    """Main performance optimization function."""
    print("SecureAI Performance Optimization")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Run performance tests
    results["basic_redaction"] = test_basic_redaction_performance()
    results["memory_usage"] = test_memory_usage()
    results["concurrent_processing"] = test_concurrent_processing()
    results["file_processing"] = test_file_processing()
    
    # Generate optimization report
    generate_optimization_report(results)
    
    # Save results
    output_file = "performance_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nResults saved to: {output_file}")
    print("\nPerformance optimization completed!")

if __name__ == "__main__":
    main() 