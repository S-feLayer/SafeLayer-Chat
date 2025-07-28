#!/usr/bin/env python3
"""
Proxy Redaction Service

This service handles Tinfoil API calls on behalf of users, so they don't need
to set up their own Tinfoil API keys. Perfect for SaaS applications.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import hashlib
from functools import lru_cache

from .tinfoil_llm import TinfoilLLM
from .redact_content import redact_content
from .enhanced_detection import EnhancedDetection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProxyRedactionService:
    """
    Proxy service that handles Tinfoil API calls on behalf of users.
    """
    
    def __init__(self, tinfoil_api_key: str, rate_limit_per_hour: int = 1000):
        """
        Initialize the proxy service.
        
        Args:
            tinfoil_api_key: Your Tinfoil API key for handling user requests
            rate_limit_per_hour: Rate limit per user per hour
        """
        self.tinfoil_llm = TinfoilLLM()
        self.rate_limit_per_hour = rate_limit_per_hour
        self.user_usage = {}  # Track user usage
        self.cache = {}  # Simple in-memory cache
        
        # Override the API key for the TinfoilLLM instance
        self.tinfoil_llm.api_key = tinfoil_api_key
        
        logger.info(f"Proxy Redaction Service initialized with rate limit: {rate_limit_per_hour}/hour")
    
    def _get_user_id(self, user_identifier: str) -> str:
        """Generate a consistent user ID from any identifier."""
        return hashlib.md5(user_identifier.encode()).hexdigest()[:16]
    
    def _check_rate_limit(self, user_identifier: str) -> bool:
        """
        Check if user is within rate limits.
        
        Returns:
            True if within limits, False if rate limited
        """
        user_id = self._get_user_id(user_identifier)
        now = datetime.now()
        
        if user_id not in self.user_usage:
            self.user_usage[user_id] = []
        
        # Remove old entries (older than 1 hour)
        self.user_usage[user_id] = [
            timestamp for timestamp in self.user_usage[user_id]
            if now - timestamp < timedelta(hours=1)
        ]
        
        # Check if within limit
        if len(self.user_usage[user_id]) >= self.rate_limit_per_hour:
            logger.warning(f"Rate limit exceeded for user: {user_identifier}")
            return False
        
        # Add current request
        self.user_usage[user_id].append(now)
        return True
    
    def _get_cache_key(self, content: str, content_type: str) -> str:
        """Generate cache key for content."""
        content_hash = hashlib.md5(f"{content}:{content_type}".encode()).hexdigest()
        return content_hash
    
    def _get_cached_result(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached result if available."""
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            # Check if cache is still valid (24 hours)
            if datetime.now() - cached_data['timestamp'] < timedelta(hours=24):
                logger.info("Returning cached redaction result")
                return cached_data['result']
            else:
                # Remove expired cache
                del self.cache[cache_key]
        return None
    
    def _cache_result(self, cache_key: str, result: Dict[str, Any]):
        """Cache the redaction result."""
        self.cache[cache_key] = {
            'result': result,
            'timestamp': datetime.now()
        }
        # Limit cache size
        if len(self.cache) > 1000:
            # Remove oldest entries
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
    
    def redact_content(self, 
                      content: str, 
                      content_type: str = "text",
                      user_identifier: str = "anonymous",
                      use_cache: bool = True) -> Dict[str, Any]:
        """
        Redact content on behalf of a user.
        
        Args:
            content: Content to redact
            content_type: Type of content (text, code, pdf)
            user_identifier: User identifier for rate limiting
            use_cache: Whether to use caching
            
        Returns:
            Redaction result with metadata
        """
        start_time = datetime.now()
        
        # Check rate limit
        if not self._check_rate_limit(user_identifier):
            return {
                "success": False,
                "error": "Rate limit exceeded. Please try again later.",
                "rate_limit_info": {
                    "limit_per_hour": self.rate_limit_per_hour,
                    "user_identifier": user_identifier
                }
            }
        
        # Check cache if enabled
        if use_cache:
            cache_key = self._get_cache_key(content, content_type)
            cached_result = self._get_cached_result(cache_key)
            if cached_result:
                cached_result["cached"] = True
                cached_result["processing_time_ms"] = 0
                return cached_result
        
        try:
            # Perform redaction using Tinfoil
            logger.info(f"Processing redaction for user: {user_identifier}")
            
            result = redact_content(content, self.tinfoil_llm)
            
            # Add metadata
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            result["processing_time_ms"] = round(processing_time, 2)
            result["user_identifier"] = user_identifier
            result["timestamp"] = datetime.now().isoformat()
            result["cached"] = False
            
            # Cache result if successful
            if result["success"] and use_cache:
                cache_key = self._get_cache_key(content, content_type)
                self._cache_result(cache_key, result)
            
            logger.info(f"Redaction completed for user: {user_identifier} in {processing_time:.2f}ms")
            return result
            
        except Exception as e:
            logger.error(f"Redaction failed for user {user_identifier}: {str(e)}")
            return {
                "success": False,
                "error": f"Redaction failed: {str(e)}",
                "user_identifier": user_identifier,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_user_stats(self, user_identifier: str) -> Dict[str, Any]:
        """Get usage statistics for a user."""
        user_id = self._get_user_id(user_identifier)
        now = datetime.now()
        
        if user_id not in self.user_usage:
            return {
                "user_identifier": user_identifier,
                "requests_this_hour": 0,
                "rate_limit": self.rate_limit_per_hour,
                "remaining_requests": self.rate_limit_per_hour
            }
        
        # Count requests in the last hour
        recent_requests = [
            timestamp for timestamp in self.user_usage[user_id]
            if now - timestamp < timedelta(hours=1)
        ]
        
        requests_this_hour = len(recent_requests)
        remaining_requests = max(0, self.rate_limit_per_hour - requests_this_hour)
        
        return {
            "user_identifier": user_identifier,
            "requests_this_hour": requests_this_hour,
            "rate_limit": self.rate_limit_per_hour,
            "remaining_requests": remaining_requests,
            "rate_limited": requests_this_hour >= self.rate_limit_per_hour
        }
    
    def get_service_stats(self) -> Dict[str, Any]:
        """Get overall service statistics."""
        total_users = len(self.user_usage)
        total_cached_items = len(self.cache)
        
        # Calculate total requests in the last hour
        now = datetime.now()
        total_requests_last_hour = sum(
            len([ts for ts in timestamps if now - ts < timedelta(hours=1)])
            for timestamps in self.user_usage.values()
        )
        
        return {
            "total_users": total_users,
            "total_requests_last_hour": total_requests_last_hour,
            "cached_items": total_cached_items,
            "rate_limit_per_hour": self.rate_limit_per_hour,
            "service_uptime": "active"
        }

class SimpleProxyAPI:
    """
    Simple API wrapper for the proxy service.
    """
    
    def __init__(self, tinfoil_api_key: str):
        """Initialize the API with your Tinfoil API key."""
        self.service = ProxyRedactionService(tinfoil_api_key)
    
    def redact(self, content: str, content_type: str = "text", user_id: str = "anonymous") -> Dict[str, Any]:
        """
        Simple redaction endpoint.
        
        Args:
            content: Content to redact
            content_type: Type of content
            user_id: User identifier
            
        Returns:
            Redaction result
        """
        return self.service.redact_content(content, content_type, user_id)
    
    def stats(self, user_id: str = None) -> Dict[str, Any]:
        """
        Get statistics.
        
        Args:
            user_id: User identifier (optional)
            
        Returns:
            Statistics
        """
        if user_id:
            return self.service.get_user_stats(user_id)
        else:
            return self.service.get_service_stats()

# Example usage functions
def create_proxy_service(tinfoil_api_key: str, rate_limit: int = 1000) -> ProxyRedactionService:
    """
    Create a proxy redaction service.
    
    Args:
        tinfoil_api_key: Your Tinfoil API key
        rate_limit: Rate limit per user per hour
        
    Returns:
        Configured proxy service
    """
    return ProxyRedactionService(tinfoil_api_key, rate_limit)

def redact_for_user(service: ProxyRedactionService, 
                   content: str, 
                   user_id: str, 
                   content_type: str = "text") -> Dict[str, Any]:
    """
    Redact content for a specific user.
    
    Args:
        service: Proxy service instance
        content: Content to redact
        user_id: User identifier
        content_type: Type of content
        
    Returns:
        Redaction result
    """
    return service.redact_content(content, content_type, user_id)

# Flask/FastAPI integration example
def create_flask_app(proxy_service: ProxyRedactionService):
    """
    Create a Flask app for the proxy service.
    
    Example:
        from flask import Flask, request, jsonify
        app = create_flask_app(proxy_service)
        app.run(debug=True)
    """
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    @app.route('/redact', methods=['POST'])
    def redact_endpoint():
        """Redact content endpoint."""
        try:
            data = request.get_json()
            content = data.get('content', '')
            content_type = data.get('content_type', 'text')
            user_id = data.get('user_id', 'anonymous')
            
            if not content:
                return jsonify({"error": "Content is required"}), 400
            
            result = proxy_service.redact_content(content, content_type, user_id)
            return jsonify(result)
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/stats/<user_id>', methods=['GET'])
    def user_stats_endpoint(user_id):
        """Get user statistics."""
        stats = proxy_service.get_user_stats(user_id)
        return jsonify(stats)
    
    @app.route('/stats', methods=['GET'])
    def service_stats_endpoint():
        """Get service statistics."""
        stats = proxy_service.get_service_stats()
        return jsonify(stats)
    
    return app

def create_fastapi_app(proxy_service: ProxyRedactionService):
    """
    Create a FastAPI app for the proxy service.
    
    Example:
        import uvicorn
        app = create_fastapi_app(proxy_service)
        uvicorn.run(app, host="0.0.0.0", port=8000)
    """
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    
    app = FastAPI(title="Proxy Redaction Service")
    
    class RedactRequest(BaseModel):
        content: str
        content_type: str = "text"
        user_id: str = "anonymous"
    
    @app.post("/redact")
    async def redact_endpoint(request: RedactRequest):
        """Redact content endpoint."""
        try:
            result = proxy_service.redact_content(
                request.content, 
                request.content_type, 
                request.user_id
            )
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/stats/{user_id}")
    async def user_stats_endpoint(user_id: str):
        """Get user statistics."""
        return proxy_service.get_user_stats(user_id)
    
    @app.get("/stats")
    async def service_stats_endpoint():
        """Get service statistics."""
        return proxy_service.get_service_stats()
    
    return app 