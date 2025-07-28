import time
import threading
from typing import Dict, List, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import hashlib
import json

class PerformanceOptimizer:
    """
    Performance optimization utilities for redaction operations.
    """
    
    def __init__(self, max_workers: int = 4, cache_size: int = 1000):
        self.max_workers = max_workers
        self.cache_size = cache_size
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self._cache = {}
        self._cache_lock = threading.Lock()
    
    def __del__(self):
        """Cleanup executor on deletion."""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=True)
    
    @lru_cache(maxsize=1000)
    def cached_detection(self, content_hash: str) -> Dict[str, List[str]]:
        """
        Cached version of sensitive data detection.
        """
        # This is a placeholder - actual implementation would use the hash to retrieve cached results
        return {}
    
    def generate_content_hash(self, content: str) -> str:
        """Generate a hash for content caching."""
        return hashlib.sha256(content.encode()).hexdigest()
    
    def batch_process(self, items: List[Any], processor: Callable, 
                     batch_size: int = 10) -> List[Any]:
        """
        Process items in batches for better performance.
        """
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            
            # Process batch in parallel
            futures = []
            for item in batch:
                future = self.executor.submit(processor, item)
                futures.append(future)
            
            # Collect results
            batch_results = []
            for future in as_completed(futures):
                try:
                    result = future.result()
                    batch_results.append(result)
                except Exception as e:
                    print(f"Error processing batch item: {e}")
                    batch_results.append(None)
            
            results.extend(batch_results)
        
        return results
    
    def parallel_redaction(self, content_chunks: List[str], 
                          redaction_func: Callable) -> List[Dict[str, Any]]:
        """
        Perform redaction on multiple content chunks in parallel.
        """
        futures = []
        
        for chunk in content_chunks:
            future = self.executor.submit(redaction_func, chunk)
            futures.append(future)
        
        results = []
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error in parallel redaction: {e}")
                results.append({"error": str(e)})
        
        return results
    
    def chunk_content(self, content: str, chunk_size: int = 10000) -> List[str]:
        """
        Split large content into manageable chunks.
        """
        if len(content) <= chunk_size:
            return [content]
        
        chunks = []
        for i in range(0, len(content), chunk_size):
            chunk = content[i:i + chunk_size]
            
            # Try to break at word boundaries
            if i + chunk_size < len(content):
                last_space = chunk.rfind(' ')
                if last_space > chunk_size * 0.8:  # If we can break at a reasonable point
                    chunk = chunk[:last_space]
                    i = i + last_space - chunk_size  # Adjust for next iteration
            
            chunks.append(chunk)
        
        return chunks
    
    def merge_chunk_results(self, chunk_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Merge results from multiple content chunks.
        """
        if not chunk_results:
            return {}
        
        merged = {
            "masked_content": "",
            "redaction_count": 0,
            "redacted_items": [],
            "errors": []
        }
        
        for result in chunk_results:
            if "error" in result:
                merged["errors"].append(result["error"])
                continue
            
            # Merge masked content
            if "masked_content" in result:
                merged["masked_content"] += result["masked_content"]
            
            # Sum redaction counts
            if "redaction_count" in result:
                merged["redaction_count"] += result["redaction_count"]
            
            # Merge redacted items
            if "redacted_items" in result:
                merged["redacted_items"].extend(result["redacted_items"])
        
        return merged

class MemoryOptimizer:
    """
    Memory optimization utilities for large content processing.
    """
    
    def __init__(self, max_memory_mb: int = 512):
        self.max_memory_mb = max_memory_mb
        self.current_memory = 0
    
    def estimate_memory_usage(self, content: str) -> int:
        """Estimate memory usage in MB for content processing."""
        # Rough estimation: content size + overhead
        return len(content.encode()) / (1024 * 1024) * 2  # 2x overhead
    
    def should_chunk(self, content: str) -> bool:
        """Determine if content should be chunked based on memory constraints."""
        estimated_memory = self.estimate_memory_usage(content)
        return estimated_memory > self.max_memory_mb
    
    def optimize_chunk_size(self, content: str) -> int:
        """Calculate optimal chunk size based on available memory."""
        content_size_mb = len(content.encode()) / (1024 * 1024)
        
        if content_size_mb <= self.max_memory_mb:
            return len(content)
        
        # Calculate chunk size to fit within memory constraints
        optimal_chunk_mb = self.max_memory_mb * 0.8  # Leave 20% buffer
        return int(optimal_chunk_mb * 1024 * 1024)

class Profiler:
    """
    Performance profiling utilities.
    """
    
    def __init__(self):
        self.timings = {}
        self.memory_usage = {}
    
    def start_timer(self, operation: str):
        """Start timing an operation."""
        self.timings[operation] = {"start": time.time()}
    
    def end_timer(self, operation: str):
        """End timing an operation."""
        if operation in self.timings:
            self.timings[operation]["end"] = time.time()
            self.timings[operation]["duration"] = (
                self.timings[operation]["end"] - self.timings[operation]["start"]
            )
    
    def get_timing(self, operation: str) -> Optional[float]:
        """Get timing for an operation."""
        if operation in self.timings and "duration" in self.timings[operation]:
            return self.timings[operation]["duration"]
        return None
    
    def get_all_timings(self) -> Dict[str, float]:
        """Get all operation timings."""
        return {
            op: data.get("duration", 0) 
            for op, data in self.timings.items()
        }
    
    def print_summary(self):
        """Print a summary of all timings."""
        print("\n📊 Performance Summary:")
        print("-" * 40)
        
        total_time = 0
        for operation, duration in self.get_all_timings().items():
            print(f"{operation:30} {duration:.3f}s")
            total_time += duration
        
        print("-" * 40)
        print(f"{'Total':30} {total_time:.3f}s") 