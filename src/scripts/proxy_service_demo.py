#!/usr/bin/env python3
"""
Proxy Redaction Service Demo

This script demonstrates how to use the proxy redaction service
so users don't need their own Tinfoil API keys.
"""

import os
import sys
import time
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from secureai.proxy_redaction_service import ProxyRedactionService, SimpleProxyAPI

def demonstrate_proxy_service():
    """Demonstrate the proxy redaction service."""
    
    print("🔄 PROXY REDACTION SERVICE DEMONSTRATION")
    print("=" * 60)
    print("Handling Tinfoil API calls on behalf of users")
    print("=" * 60)
    
    # Check for Tinfoil API key (you need this as the service provider)
    if not os.getenv("TINFOIL_API_KEY"):
        print("⚠️ TINFOIL_API_KEY not set. Please set your API key:")
        print("export TINFOIL_API_KEY='your_key_here'")
        return
    
    try:
        # Initialize proxy service (you provide the API key)
        print("\n🔧 Initializing Proxy Service...")
        proxy_service = ProxyRedactionService(
            tinfoil_api_key=os.getenv("TINFOIL_API_KEY"),
            rate_limit_per_hour=100  # Limit for demo
        )
        
        # Create sample content
        sensitive_content = """
        Hi team,
        
        I need to share some sensitive project information:
        
        My name is Sarah Johnson and my email is sarah.johnson@techcorp.com
        My phone number is +1-555-987-6543
        My employee ID is EMP-78901
        
        Project Details:
        - Client: Acme Solutions Inc. (456 Business Ave, San Francisco, CA 94102)
        - Contract Number: CNT-2024-003
        - Budget: $150,000
        - Timeline: 6 months
        
        Technical Information:
        - Database URL: postgresql://admin:secretpass123@prod-db.techcorp.com:5432/project_db
        - API Key: sk-1234567890abcdef1234567890abcdef1234567890abcdef
        - GitHub Token: ghp_1234567890abcdef1234567890abcdef1234567890
        - AWS Access Key: AKIA1234567890ABCDEF
        
        Personal Notes:
        - Meeting with John Smith (john.smith@acme.com) on Friday
        - Discussing sensitive merger details
        - Need to keep this confidential!
        
        Best regards,
        Sarah
        """
        
        # Demonstrate multiple users
        users = ["user_123", "user_456", "user_789"]
        
        for i, user_id in enumerate(users):
            print(f"\n👤 Processing for User: {user_id}")
            print("-" * 40)
            
            # Get user stats before processing
            stats_before = proxy_service.get_user_stats(user_id)
            print(f"📊 Stats before: {stats_before['requests_this_hour']} requests this hour")
            
            # Process redaction
            start_time = time.time()
            result = proxy_service.redact_content(
                content=sensitive_content,
                content_type="text",
                user_identifier=user_id,
                use_cache=True
            )
            processing_time = time.time() - start_time
            
            # Display results
            if result["success"]:
                redaction_result = result["redaction_result"]
                print(f"✅ Redaction successful!")
                print(f"   📝 Items redacted: {redaction_result['redaction_count']}")
                print(f"   ⏱️ Processing time: {result['processing_time_ms']}ms")
                print(f"   💾 Cached: {result.get('cached', False)}")
                
                # Show sample of redacted content
                redacted_text = redaction_result["redacted_text"]
                print(f"   📄 Sample redacted content:")
                print(f"   '{redacted_text[:100]}...'")
                
            else:
                print(f"❌ Redaction failed: {result['error']}")
            
            # Get user stats after processing
            stats_after = proxy_service.get_user_stats(user_id)
            print(f"📊 Stats after: {stats_after['requests_this_hour']} requests this hour")
            print(f"   🎯 Remaining requests: {stats_after['remaining_requests']}")
        
        # Demonstrate caching
        print(f"\n🔄 CACHING DEMONSTRATION")
        print("-" * 40)
        
        user_id = "cache_test_user"
        content = "Hi John Doe, my email is john@example.com"
        
        print("First request (should be slow):")
        start_time = time.time()
        result1 = proxy_service.redact_content(content, "text", user_id)
        time1 = time.time() - start_time
        print(f"   Time: {time1:.3f}s, Cached: {result1.get('cached', False)}")
        
        print("Second request (should be fast, cached):")
        start_time = time.time()
        result2 = proxy_service.redact_content(content, "text", user_id)
        time2 = time.time() - start_time
        print(f"   Time: {time2:.3f}s, Cached: {result2.get('cached', False)}")
        
        print(f"   ⚡ Speed improvement: {time1/time2:.1f}x faster")
        
        # Demonstrate rate limiting
        print(f"\n🚫 RATE LIMITING DEMONSTRATION")
        print("-" * 40)
        
        user_id = "rate_limit_test"
        
        # Make requests until rate limited
        for i in range(5):
            result = proxy_service.redact_content("Test content", "text", user_id)
            stats = proxy_service.get_user_stats(user_id)
            
            print(f"Request {i+1}: {'✅ Success' if result['success'] else '❌ Rate Limited'}")
            print(f"   Remaining: {stats['remaining_requests']}")
            
            if not result['success'] and 'Rate limit exceeded' in result.get('error', ''):
                print("   🚫 Rate limit hit!")
                break
        
        # Show service statistics
        print(f"\n📈 SERVICE STATISTICS")
        print("-" * 40)
        
        service_stats = proxy_service.get_service_stats()
        print(f"Total users: {service_stats['total_users']}")
        print(f"Total requests (last hour): {service_stats['total_requests_last_hour']}")
        print(f"Cached items: {service_stats['cached_items']}")
        print(f"Rate limit per hour: {service_stats['rate_limit_per_hour']}")
        
        print("\n🎉 Proxy Service Demonstration Complete!")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")

def demonstrate_simple_api():
    """Demonstrate the simple API wrapper."""
    
    print("\n🔧 SIMPLE API WRAPPER DEMONSTRATION")
    print("=" * 50)
    
    if not os.getenv("TINFOIL_API_KEY"):
        print("⚠️ TINFOIL_API_KEY not set")
        return
    
    try:
        # Initialize simple API
        api = SimpleProxyAPI(os.getenv("TINFOIL_API_KEY"))
        
        # Test redaction
        content = "Hi Jane Smith, my email is jane@example.com"
        result = api.redact(content, "text", "test_user")
        
        print(f"Redaction result: {'✅ Success' if result['success'] else '❌ Failed'}")
        if result['success']:
            print(f"Items redacted: {result['redaction_result']['redaction_count']}")
        
        # Test stats
        stats = api.stats("test_user")
        print(f"User stats: {stats}")
        
        service_stats = api.stats()
        print(f"Service stats: {service_stats}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def demonstrate_web_integration():
    """Demonstrate web integration patterns."""
    
    print("\n🌐 WEB INTEGRATION PATTERNS")
    print("=" * 50)
    
    print("""
    Here are the integration patterns for web applications:
    
    1. FLASK INTEGRATION:
    ```python
    from flask import Flask, request, jsonify
    from secureai.proxy_redaction_service import ProxyRedactionService
    
    # Initialize service (you provide the API key)
    proxy_service = ProxyRedactionService(os.getenv("TINFOIL_API_KEY"))
    
    app = Flask(__name__)
    
    @app.route('/redact', methods=['POST'])
    def redact():
        data = request.get_json()
        result = proxy_service.redact_content(
            content=data['content'],
            content_type=data.get('content_type', 'text'),
            user_identifier=data.get('user_id', 'anonymous')
        )
        return jsonify(result)
    
    app.run(debug=True)
    ```
    
    2. FASTAPI INTEGRATION:
    ```python
    from fastapi import FastAPI
    from pydantic import BaseModel
    from secureai.proxy_redaction_service import ProxyRedactionService
    
    app = FastAPI()
    proxy_service = ProxyRedactionService(os.getenv("TINFOIL_API_KEY"))
    
    class RedactRequest(BaseModel):
        content: str
        content_type: str = "text"
        user_id: str = "anonymous"
    
    @app.post("/redact")
    async def redact(request: RedactRequest):
        return proxy_service.redact_content(
            request.content, 
            request.content_type, 
            request.user_id
        )
    ```
    
    3. DJANGO INTEGRATION:
    ```python
    from django.http import JsonResponse
    from django.views.decorators.csrf import csrf_exempt
    from django.views.decorators.http import require_http_methods
    import json
    from secureai.proxy_redaction_service import ProxyRedactionService
    
    proxy_service = ProxyRedactionService(os.getenv("TINFOIL_API_KEY"))
    
    @csrf_exempt
    @require_http_methods(["POST"])
    def redact_view(request):
        data = json.loads(request.body)
        result = proxy_service.redact_content(
            content=data['content'],
            content_type=data.get('content_type', 'text'),
            user_identifier=data.get('user_id', 'anonymous')
        )
        return JsonResponse(result)
    ```
    
    4. CLIENT-SIDE USAGE:
    ```javascript
    // Frontend JavaScript
    async function redactContent(content, userId) {
        const response = await fetch('/api/redact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: content,
                content_type: 'text',
                user_id: userId
            })
        });
        
        return await response.json();
    }
    
    // Usage
    const result = await redactContent(
        "Hi John, my email is john@example.com", 
        "user_123"
    );
    
    if (result.success) {
        console.log("Redacted content:", result.redaction_result.redacted_text);
    }
    ```
    """)

def main():
    """Main demonstration function."""
    
    print("🔄 PROXY REDACTION SERVICE DEMONSTRATION")
    print("=" * 60)
    print("Handling Tinfoil API calls on behalf of users")
    print("=" * 60)
    
    # Run demonstrations
    demonstrate_proxy_service()
    demonstrate_simple_api()
    demonstrate_web_integration()
    
    print("\n🎉 All Demonstrations Complete!")
    print("\n💡 Key Benefits:")
    print("  • Users don't need Tinfoil API keys")
    print("  • Centralized rate limiting and caching")
    print("  • Easy integration with web applications")
    print("  • Cost-effective for multiple users")
    print("  • Secure API key management")

if __name__ == "__main__":
    main() 