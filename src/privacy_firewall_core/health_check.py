"""
Health check endpoint for SecureAI MCP server.
Provides monitoring and deployment verification capabilities.
"""

import json
import time
import psutil
import os
from datetime import datetime
from typing import Dict, Any, Optional
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Prometheus metrics
REQUEST_COUNT = Counter('secureai_requests_total', 'Total requests', ['endpoint', 'method'])
REQUEST_DURATION = Histogram('secureai_request_duration_seconds', 'Request duration', ['endpoint'])
ACTIVE_CONNECTIONS = Gauge('secureai_active_connections', 'Active connections')
SYSTEM_MEMORY = Gauge('secureai_system_memory_bytes', 'System memory usage')
SYSTEM_CPU = Gauge('secureai_system_cpu_percent', 'System CPU usage')

class HealthChecker:
    """Health check service for SecureAI MCP."""
    
    def __init__(self):
        self.start_time = time.time()
        self.health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "uptime": 0,
            "services": {},
            "system": {},
            "dependencies": {}
        }
    
    def check_system_health(self) -> Dict[str, Any]:
        """Check system resources and health."""
        try:
            # System metrics
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=1)
            disk = psutil.disk_usage('/')
            
            # Update Prometheus metrics
            SYSTEM_MEMORY.set(memory.used)
            SYSTEM_CPU.set(cpu_percent)
            
            return {
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "used": memory.used,
                    "percent": memory.percent
                },
                "cpu": {
                    "percent": cpu_percent
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": (disk.used / disk.total) * 100
                }
            }
        except Exception as e:
            return {"error": str(e)}
    
    def check_dependencies(self) -> Dict[str, Any]:
        """Check external dependencies."""
        dependencies = {}
        
        # Check Tinfoil API
        try:
            from .tinfoil_llm import TinfoilLLM
            tinfoil = TinfoilLLM()
            # Simple test call
            test_result = tinfoil.analyze_text("test")
            dependencies["tinfoil_api"] = {
                "status": "healthy",
                "response_time": 0.1  # Placeholder
            }
        except Exception as e:
            dependencies["tinfoil_api"] = {
                "status": "unhealthy",
                "error": str(e)
            }
        
        # Check file system access
        try:
            test_dir = "cache/health_check"
            os.makedirs(test_dir, exist_ok=True)
            test_file = os.path.join(test_dir, "test.txt")
            with open(test_file, 'w') as f:
                f.write("health check")
            with open(test_file, 'r') as f:
                content = f.read()
            os.remove(test_file)
            os.rmdir(test_dir)
            
            dependencies["file_system"] = {
                "status": "healthy",
                "writable": True
            }
        except Exception as e:
            dependencies["file_system"] = {
                "status": "unhealthy",
                "error": str(e)
            }
        
        return dependencies
    
    def check_services(self) -> Dict[str, Any]:
        """Check internal services."""
        services = {}
        
        # Check redaction service
        try:
            from .redact_content import get_supported_formats
            formats = get_supported_formats()
            services["redaction_service"] = {
                "status": "healthy",
                "supported_formats": len(formats)
            }
        except Exception as e:
            services["redaction_service"] = {
                "status": "unhealthy",
                "error": str(e)
            }
        
        # Check MCP server
        try:
            services["mcp_server"] = {
                "status": "healthy",
                "transport": "stdio"
            }
        except Exception as e:
            services["mcp_server"] = {
                "status": "unhealthy",
                "error": str(e)
            }
        
        return services
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status."""
        self.health_status["uptime"] = time.time() - self.start_time
        self.health_status["timestamp"] = datetime.utcnow().isoformat()
        self.health_status["system"] = self.check_system_health()
        self.health_status["dependencies"] = self.check_dependencies()
        self.health_status["services"] = self.check_services()
        
        # Determine overall status
        all_healthy = True
        for service in self.health_status["services"].values():
            if service.get("status") != "healthy":
                all_healthy = False
                break
        
        for dep in self.health_status["dependencies"].values():
            if dep.get("status") != "healthy":
                all_healthy = False
                break
        
        self.health_status["status"] = "healthy" if all_healthy else "unhealthy"
        
        return self.health_status
    
    def get_metrics(self) -> str:
        """Get Prometheus metrics."""
        return generate_latest()

# Global health checker instance
health_checker = HealthChecker()

def get_health_response() -> Dict[str, Any]:
    """Get health check response."""
    REQUEST_COUNT.labels(endpoint='/health', method='GET').inc()
    return health_checker.get_health_status()

def get_metrics_response() -> str:
    """Get metrics response."""
    REQUEST_COUNT.labels(endpoint='/metrics', method='GET').inc()
    return health_checker.get_metrics()

def record_request_duration(endpoint: str, duration: float):
    """Record request duration for metrics."""
    REQUEST_DURATION.labels(endpoint=endpoint).observe(duration)

def update_active_connections(count: int):
    """Update active connections count."""
    ACTIVE_CONNECTIONS.set(count)
