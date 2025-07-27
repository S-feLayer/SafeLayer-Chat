#!/usr/bin/env python3
"""
Performance benchmarking script for Secure AI.
Tests speed, memory usage, and efficiency of redaction operations.
"""

import os
import time
import sys
import psutil
import tempfile
from pathlib import Path
from typing import Dict, List, Any
import statistics

# Add the src directory to the path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

class PerformanceBenchmark:
    """Performance benchmarking for Secure AI."""
    
    def __init__(self):
        self.results = {}
        self.process = psutil.Process()
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        return self.process.memory_info().rss / 1024 / 1024
    
    def benchmark_operation(self, operation_name: str, operation_func: callable, 
                          iterations: int = 5) -> Dict[str, Any]:
        """Benchmark a single operation."""
        print(f"⏱️  Benchmarking: {operation_name}")
        
        timings = []
        memory_usage = []
        
        for i in range(iterations):
            # Measure memory before
            memory_before = self.get_memory_usage()
            start_time = time.time()
            
            # Run operation
            try:
                result = operation_func()
                success = True
            except Exception as e:
                result = None
                success = False
                print(f"    Iteration {i+1} failed: {e}")
            
            # Measure timing and memory
            end_time = time.time()
            memory_after = self.get_memory_usage()
            
            timing = end_time - start_time
            memory_delta = memory_after - memory_before
            
            timings.append(timing)
            memory_usage.append(memory_delta)
            
            print(f"    Iteration {i+1}: {timing:.3f}s, {memory_delta:.1f}MB")
        
        # Calculate statistics
        stats = {
            "operation": operation_name,
            "iterations": iterations,
            "successful_iterations": len([t for t in timings if t > 0]),
            "timing": {
                "mean": statistics.mean(timings),
                "median": statistics.median(timings),
                "min": min(timings),
                "max": max(timings),
                "std": statistics.stdev(timings) if len(timings) > 1 else 0
            },
            "memory": {
                "mean": statistics.mean(memory_usage),
                "median": statistics.median(memory_usage),
                "min": min(memory_usage),
                "max": max(memory_usage),
                "std": statistics.stdev(memory_usage) if len(memory_usage) > 1 else 0
            }
        }
        
        print(f"  📊 Results: {stats['timing']['mean']:.3f}s ± {stats['timing']['std']:.3f}s")
        print(f"  💾 Memory: {stats['memory']['mean']:.1f}MB ± {stats['memory']['std']:.1f}MB")
        
        return stats
    
    def create_test_content(self, size_kb: int) -> str:
        """Create test content of specified size."""
        base_content = """
        Hello John Doe, my email is john@example.com and my phone number is 555-123-4567.
        The API key is sk-1234567890abcdef1234567890abcdef12345678.
        The JWT token is eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c.
        The database URL is postgresql://user:password123@localhost:5432/mydb.
        """
        
        # Repeat content to reach desired size
        target_size = size_kb * 1024
        content = ""
        while len(content.encode()) < target_size:
            content += base_content
        
        return content[:target_size]
    
    def benchmark_text_redaction(self) -> Dict[str, Any]:
        """Benchmark text redaction performance."""
        try:
            from secureai import redact_text
            from secureai.tinfoil_llm import TinfoilLLM
            
            tinfoil_llm = TinfoilLLM()
            
            # Test different content sizes
            size_tests = [1, 10, 50, 100]  # KB
            results = {}
            
            for size_kb in size_tests:
                print(f"\n📝 Testing {size_kb}KB text content")
                content = self.create_test_content(size_kb)
                
                def redaction_operation():
                    return redact_text(content, tinfoil_llm)
                
                results[f"{size_kb}KB"] = self.benchmark_operation(
                    f"Text Redaction ({size_kb}KB)", 
                    redaction_operation,
                    iterations=3  # Fewer iterations for larger content
                )
            
            return {"text_redaction": results}
            
        except Exception as e:
            if "TINFOIL_API_KEY" in str(e):
                print("⚠️  Skipping text redaction benchmark (TINFOIL_API_KEY not set)")
                return {"text_redaction": "skipped"}
            else:
                print(f"❌ Text redaction benchmark failed: {e}")
                return {"text_redaction": "failed"}
    
    def benchmark_code_redaction(self) -> Dict[str, Any]:
        """Benchmark code redaction performance."""
        try:
            from secureai import redact_code_file
            from secureai.tinfoil_llm import TinfoilLLM
            
            tinfoil_llm = TinfoilLLM()
            
            # Create test code files
            test_files = {
                "small": self.create_test_code_file(1),   # 1KB
                "medium": self.create_test_code_file(10), # 10KB
                "large": self.create_test_code_file(50),  # 50KB
            }
            
            results = {}
            
            for size_name, file_path in test_files.items():
                print(f"\n💻 Testing {size_name} code file")
                
                def redaction_operation():
                    return redact_code_file(file_path, tinfoil_llm)
                
                results[size_name] = self.benchmark_operation(
                    f"Code Redaction ({size_name})", 
                    redaction_operation,
                    iterations=3
                )
                
                # Cleanup
                if os.path.exists(file_path):
                    os.unlink(file_path)
            
            return {"code_redaction": results}
            
        except Exception as e:
            if "TINFOIL_API_KEY" in str(e):
                print("⚠️  Skipping code redaction benchmark (TINFOIL_API_KEY not set)")
                return {"code_redaction": "skipped"}
            else:
                print(f"❌ Code redaction benchmark failed: {e}")
                return {"code_redaction": "failed"}
    
    def create_test_code_file(self, size_kb: int) -> str:
        """Create a test code file of specified size."""
        base_code = '''
# Configuration file
API_KEY = "sk-1234567890abcdef1234567890abcdef12345678"
DATABASE_URL = "postgresql://user:password123@localhost:5432/mydb"
SECRET_TOKEN = "secret_token_here"
ADMIN_EMAIL = "admin@company.com"
ADMIN_PASSWORD = "admin123"
USER_NAME = "John Doe"
USER_PHONE = "555-987-6543"
USER_ADDRESS = "123 Main St, City, State 12345"
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
'''
        
        # Repeat content to reach desired size
        target_size = size_kb * 1024
        content = ""
        while len(content.encode()) < target_size:
            content += base_code
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(content[:target_size])
            return f.name
    
    def benchmark_content_type_detection(self) -> Dict[str, Any]:
        """Benchmark content type detection performance."""
        from secureai.redact_content import detect_content_type
        
        test_cases = [
            ("PDF file", "document.pdf"),
            ("Python file", "script.py"),
            ("JavaScript file", "app.js"),
            ("Text content", "This is some text content"),
            ("Dictionary input", {"content_type": "pdf"}),
        ]
        
        results = {}
        
        for test_name, test_input in test_cases:
            print(f"\n🔍 Testing {test_name}")
            
            def detection_operation():
                return detect_content_type(test_input)
            
            results[test_name] = self.benchmark_operation(
                f"Content Type Detection ({test_name})", 
                detection_operation,
                iterations=100  # Many iterations since this should be fast
            )
        
        return {"content_type_detection": results}
    
    def benchmark_language_detection(self) -> Dict[str, Any]:
        """Benchmark language detection performance."""
        from secureai.redact_code import detect_language
        
        test_cases = [
            ("Python", "script.py"),
            ("JavaScript", "app.js"),
            ("Java", "Main.java"),
            ("YAML", "config.yaml"),
            ("Dockerfile", "Dockerfile"),
            ("Unknown", "unknown.xyz"),
        ]
        
        results = {}
        
        for test_name, test_input in test_cases:
            print(f"\n🔧 Testing {test_name}")
            
            def detection_operation():
                return detect_language(test_input)
            
            results[test_name] = self.benchmark_operation(
                f"Language Detection ({test_name})", 
                detection_operation,
                iterations=100  # Many iterations since this should be fast
            )
        
        return {"language_detection": results}
    
    def benchmark_memory_efficiency(self) -> Dict[str, Any]:
        """Benchmark memory efficiency with large content."""
        try:
            from secureai import redact_content
            from secureai.tinfoil_llm import TinfoilLLM
            
            tinfoil_llm = TinfoilLLM()
            
            # Test with very large content
            print(f"\n💾 Testing memory efficiency with large content")
            
            # Create 1MB of content
            large_content = self.create_test_content(1024)  # 1MB
            
            memory_before = self.get_memory_usage()
            start_time = time.time()
            
            result = redact_content(large_content, tinfoil_llm)
            
            end_time = time.time()
            memory_after = self.get_memory_usage()
            
            timing = end_time - start_time
            memory_used = memory_after - memory_before
            
            stats = {
                "operation": "Large Content Processing",
                "content_size_mb": len(large_content.encode()) / 1024 / 1024,
                "timing": {
                    "total_time": timing,
                    "throughput_mbps": (len(large_content.encode()) / 1024 / 1024) / timing
                },
                "memory": {
                    "peak_usage_mb": memory_used,
                    "efficiency_mb_per_mb": memory_used / (len(large_content.encode()) / 1024 / 1024)
                }
            }
            
            print(f"  📊 Results: {timing:.3f}s, {memory_used:.1f}MB")
            print(f"  🚀 Throughput: {stats['timing']['throughput_mbps']:.2f}MB/s")
            print(f"  💾 Memory efficiency: {stats['memory']['efficiency_mb_per_mb']:.2f}MB/MB")
            
            return {"memory_efficiency": stats}
            
        except Exception as e:
            if "TINFOIL_API_KEY" in str(e):
                print("⚠️  Skipping memory efficiency benchmark (TINFOIL_API_KEY not set)")
                return {"memory_efficiency": "skipped"}
            else:
                print(f"❌ Memory efficiency benchmark failed: {e}")
                return {"memory_efficiency": "failed"}
    
    def run_all_benchmarks(self) -> Dict[str, Any]:
        """Run all performance benchmarks."""
        print("🚀 Running Performance Benchmarks")
        print("=" * 60)
        
        all_results = {}
        
        # Run different benchmark categories
        all_results.update(self.benchmark_content_type_detection())
        all_results.update(self.benchmark_language_detection())
        all_results.update(self.benchmark_text_redaction())
        all_results.update(self.benchmark_code_redaction())
        all_results.update(self.benchmark_memory_efficiency())
        
        # Generate summary
        summary = self._generate_summary(all_results)
        all_results["summary"] = summary
        
        # Print summary
        self._print_summary(summary)
        
        return all_results
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of all benchmark results."""
        summary = {
            "total_operations": 0,
            "average_timing": 0,
            "fastest_operation": None,
            "slowest_operation": None,
            "memory_usage": 0
        }
        
        timings = []
        
        for category, category_results in results.items():
            if isinstance(category_results, dict):
                for operation_name, operation_results in category_results.items():
                    if isinstance(operation_results, dict) and "timing" in operation_results:
                        timing = operation_results["timing"]["mean"]
                        timings.append((operation_name, timing))
                        
                        if summary["fastest_operation"] is None or timing < summary["fastest_operation"][1]:
                            summary["fastest_operation"] = (operation_name, timing)
                        
                        if summary["slowest_operation"] is None or timing > summary["slowest_operation"][1]:
                            summary["slowest_operation"] = (operation_name, timing)
        
        if timings:
            summary["total_operations"] = len(timings)
            summary["average_timing"] = statistics.mean([t[1] for t in timings])
        
        return summary
    
    def _print_summary(self, summary: Dict[str, Any]):
        """Print benchmark summary."""
        print("\n" + "=" * 60)
        print("📊 Performance Benchmark Summary")
        print("-" * 40)
        print(f"Total Operations Tested: {summary['total_operations']}")
        print(f"Average Timing: {summary['average_timing']:.3f}s")
        
        if summary["fastest_operation"]:
            print(f"Fastest Operation: {summary['fastest_operation'][0]} ({summary['fastest_operation'][1]:.3f}s)")
        
        if summary["slowest_operation"]:
            print(f"Slowest Operation: {summary['slowest_operation'][0]} ({summary['slowest_operation'][1]:.3f}s)")
        
        print("\n💡 Performance Recommendations:")
        if summary["average_timing"] > 1.0:
            print("  - Consider optimizing slow operations")
        if summary["fastest_operation"] and summary["fastest_operation"][1] < 0.001:
            print("  - Fast operations are performing well")
        print("  - Monitor memory usage for large content")
        print("  - Consider caching for repeated operations")

def main():
    """Run the performance benchmarks."""
    benchmark = PerformanceBenchmark()
    results = benchmark.run_all_benchmarks()
    
    # Save results to file
    import json
    with open("performance_benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: performance_benchmark_results.json")
    print("\n✅ Performance benchmarking completed!")

if __name__ == "__main__":
    main() 