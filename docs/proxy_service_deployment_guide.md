# Proxy Redaction Service Deployment Guide

This guide shows how to deploy the proxy redaction service so users don't need their own Tinfoil API keys.

## 🎯 **Overview**

The proxy service allows you to:
- **Handle Tinfoil API calls** on behalf of your users
- **Provide redaction as a service** without users needing API keys
- **Implement rate limiting** and caching for cost control
- **Integrate easily** with web applications

## 🚀 **Quick Start**

### **1. Basic Setup**

```python
from secureai.proxy_redaction_service import ProxyRedactionService

# Initialize with your Tinfoil API key
proxy_service = ProxyRedactionService(
    tinfoil_api_key="your_tinfoil_api_key_here",
    rate_limit_per_hour=1000  # Requests per user per hour
)

# Use the service
result = proxy_service.redact_content(
    content="Hi John, my email is john@example.com",
    content_type="text",
    user_identifier="user_123"
)
```

### **2. Simple API Wrapper**

```python
from secureai.proxy_redaction_service import SimpleProxyAPI

# Create simple API
api = SimpleProxyAPI("your_tinfoil_api_key_here")

# Redact content
result = api.redact("Sensitive content", "text", "user_123")

# Get statistics
stats = api.stats("user_123")
```

## 🌐 **Web Application Integration**

### **Flask Application**

```python
from flask import Flask, request, jsonify
from secureai.proxy_redaction_service import ProxyRedactionService
import os

app = Flask(__name__)

# Initialize proxy service
proxy_service = ProxyRedactionService(
    tinfoil_api_key=os.getenv("TINFOIL_API_KEY"),
    rate_limit_per_hour=1000
)

@app.route('/api/redact', methods=['POST'])
def redact_endpoint():
    """Redact content endpoint."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'content' not in data:
            return jsonify({"error": "Content is required"}), 400
        
        # Get user ID from request (implement your auth logic)
        user_id = data.get('user_id', request.headers.get('X-User-ID', 'anonymous'))
        
        # Perform redaction
        result = proxy_service.redact_content(
            content=data['content'],
            content_type=data.get('content_type', 'text'),
            user_identifier=user_id,
            use_cache=data.get('use_cache', True)
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats/<user_id>', methods=['GET'])
def user_stats_endpoint(user_id):
    """Get user statistics."""
    stats = proxy_service.get_user_stats(user_id)
    return jsonify(stats)

@app.route('/api/stats', methods=['GET'])
def service_stats_endpoint():
    """Get service statistics."""
    stats = proxy_service.get_service_stats()
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### **FastAPI Application**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from secureai.proxy_redaction_service import ProxyRedactionService
import os

app = FastAPI(title="Proxy Redaction Service")

# Initialize proxy service
proxy_service = ProxyRedactionService(
    tinfoil_api_key=os.getenv("TINFOIL_API_KEY"),
    rate_limit_per_hour=1000
)

class RedactRequest(BaseModel):
    content: str
    content_type: str = "text"
    user_id: str = "anonymous"
    use_cache: bool = True

class RedactResponse(BaseModel):
    success: bool
    redaction_result: dict = None
    error: str = None
    processing_time_ms: float = None
    cached: bool = False

@app.post("/api/redact", response_model=RedactResponse)
async def redact_endpoint(request: RedactRequest):
    """Redact content endpoint."""
    try:
        result = proxy_service.redact_content(
            content=request.content,
            content_type=request.content_type,
            user_identifier=request.user_id,
            use_cache=request.use_cache
        )
        return RedactResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats/{user_id}")
async def user_stats_endpoint(user_id: str):
    """Get user statistics."""
    return proxy_service.get_user_stats(user_id)

@app.get("/api/stats")
async def service_stats_endpoint():
    """Get service statistics."""
    return proxy_service.get_service_stats()

# Run with: uvicorn main:app --host 0.0.0.0 --port 8000
```

### **Django Application**

```python
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
from secureai.proxy_redaction_service import ProxyRedactionService

# Initialize proxy service
proxy_service = ProxyRedactionService(
    tinfoil_api_key=os.getenv("TINFOIL_API_KEY"),
    rate_limit_per_hour=1000
)

@csrf_exempt
@require_http_methods(["POST"])
def redact_view(request):
    """Redact content endpoint."""
    try:
        data = json.loads(request.body)
        
        if 'content' not in data:
            return JsonResponse({"error": "Content is required"}, status=400)
        
        # Get user ID (implement your auth logic)
        user_id = data.get('user_id', 'anonymous')
        
        result = proxy_service.redact_content(
            content=data['content'],
            content_type=data.get('content_type', 'text'),
            user_identifier=user_id,
            use_cache=data.get('use_cache', True)
        )
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_http_methods(["GET"])
def user_stats_view(request, user_id):
    """Get user statistics."""
    stats = proxy_service.get_user_stats(user_id)
    return JsonResponse(stats)

@require_http_methods(["GET"])
def service_stats_view(request):
    """Get service statistics."""
    stats = proxy_service.get_service_stats()
    return JsonResponse(stats)
```

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/redact/', views.redact_view, name='redact'),
    path('api/stats/<str:user_id>/', views.user_stats_view, name='user_stats'),
    path('api/stats/', views.service_stats_view, name='service_stats'),
]
```

## 🔧 **Production Deployment**

### **1. Environment Setup**

```bash
# .env file
TINFOIL_API_KEY=your_tinfoil_api_key_here
FLASK_ENV=production
FLASK_DEBUG=0
```

### **2. Docker Deployment**

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  proxy-redaction:
    build: .
    ports:
      - "5000:5000"
    environment:
      - TINFOIL_API_KEY=${TINFOIL_API_KEY}
      - FLASK_ENV=production
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
```

### **3. Kubernetes Deployment**

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: proxy-redaction
spec:
  replicas: 3
  selector:
    matchLabels:
      app: proxy-redaction
  template:
    metadata:
      labels:
        app: proxy-redaction
    spec:
      containers:
      - name: proxy-redaction
        image: your-registry/proxy-redaction:latest
        ports:
        - containerPort: 5000
        env:
        - name: TINFOIL_API_KEY
          valueFrom:
            secretKeyRef:
              name: tinfoil-secret
              key: api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: proxy-redaction-service
spec:
  selector:
    app: proxy-redaction
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

### **4. AWS Lambda Deployment**

```python
# lambda_function.py
import json
import os
from secureai.proxy_redaction_service import ProxyRedactionService

# Initialize proxy service
proxy_service = ProxyRedactionService(
    tinfoil_api_key=os.getenv("TINFOIL_API_KEY"),
    rate_limit_per_hour=1000
)

def lambda_handler(event, context):
    """AWS Lambda handler."""
    try:
        # Parse request
        body = json.loads(event['body'])
        
        # Perform redaction
        result = proxy_service.redact_content(
            content=body['content'],
            content_type=body.get('content_type', 'text'),
            user_identifier=body.get('user_id', 'anonymous')
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({"error": str(e)})
        }
```

## 🔒 **Security Considerations**

### **1. API Key Management**

```python
# Use environment variables
import os
from dotenv import load_dotenv

load_dotenv()

proxy_service = ProxyRedactionService(
    tinfoil_api_key=os.getenv("TINFOIL_API_KEY")
)
```

### **2. User Authentication**

```python
# Example with JWT authentication
import jwt
from functools import wraps

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "No token provided"}), 401
        
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(*args, **kwargs)
    return decorated

@app.route('/api/redact', methods=['POST'])
@require_auth
def redact_endpoint():
    user_id = request.user_id
    # ... rest of the function
```

### **3. Rate Limiting**

```python
# Custom rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/redact', methods=['POST'])
@limiter.limit("10 per minute")
def redact_endpoint():
    # ... implementation
```

## 📊 **Monitoring and Logging**

### **1. Application Logging**

```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
    handlers=[
        RotatingFileHandler('logs/proxy_service.log', maxBytes=10240000, backupCount=10),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Log redaction requests
@app.route('/api/redact', methods=['POST'])
def redact_endpoint():
    user_id = request.json.get('user_id', 'anonymous')
    content_length = len(request.json.get('content', ''))
    
    logger.info(f"Redaction request from user {user_id}, content length: {content_length}")
    
    # ... rest of implementation
```

### **2. Health Checks**

```python
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        # Test Tinfoil connection
        test_result = proxy_service.redact_content(
            "test content", "text", "health_check"
        )
        
        return jsonify({
            "status": "healthy",
            "tinfoil_connection": "ok",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500
```

### **3. Metrics Collection**

```python
from prometheus_client import Counter, Histogram, generate_latest

# Define metrics
redaction_requests = Counter('redaction_requests_total', 'Total redaction requests', ['user_id', 'content_type'])
redaction_duration = Histogram('redaction_duration_seconds', 'Redaction processing time')

@app.route('/api/redact', methods=['POST'])
def redact_endpoint():
    start_time = time.time()
    
    # ... redaction logic
    
    # Record metrics
    duration = time.time() - start_time
    redaction_requests.labels(user_id=user_id, content_type=content_type).inc()
    redaction_duration.observe(duration)

@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint."""
    return generate_latest()
```

## 💰 **Cost Optimization**

### **1. Caching Strategy**

```python
# Redis caching
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_redaction(content_hash):
    """Get cached redaction result."""
    cached = redis_client.get(f"redaction:{content_hash}")
    return json.loads(cached) if cached else None

def cache_redaction_result(content_hash, result):
    """Cache redaction result."""
    redis_client.setex(
        f"redaction:{content_hash}",
        3600,  # 1 hour TTL
        json.dumps(result)
    )
```

### **2. Batch Processing**

```python
def batch_redact(content_list, user_id):
    """Process multiple content items efficiently."""
    results = []
    
    for content in content_list:
        # Check cache first
        content_hash = hashlib.md5(content.encode()).hexdigest()
        cached_result = get_cached_redaction(content_hash)
        
        if cached_result:
            results.append(cached_result)
        else:
            result = proxy_service.redact_content(content, "text", user_id)
            cache_redaction_result(content_hash, result)
            results.append(result)
    
    return results
```

## 🚀 **Client Integration Examples**

### **JavaScript/TypeScript**

```typescript
// Client-side integration
class RedactionClient {
    private baseUrl: string;
    private apiKey: string;

    constructor(baseUrl: string, apiKey: string) {
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
    }

    async redactContent(content: string, userId: string, contentType: string = 'text') {
        const response = await fetch(`${this.baseUrl}/api/redact`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`,
                'X-User-ID': userId
            },
            body: JSON.stringify({
                content,
                content_type: contentType,
                user_id: userId
            })
        });

        if (!response.ok) {
            throw new Error(`Redaction failed: ${response.statusText}`);
        }

        return await response.json();
    }

    async getUserStats(userId: string) {
        const response = await fetch(`${this.baseUrl}/api/stats/${userId}`, {
            headers: {
                'Authorization': `Bearer ${this.apiKey}`
            }
        });

        return await response.json();
    }
}

// Usage
const client = new RedactionClient('https://your-redaction-service.com', 'your-api-key');

const result = await client.redactContent(
    "Hi John, my email is john@example.com",
    "user_123"
);

if (result.success) {
    console.log("Redacted content:", result.redaction_result.redacted_text);
}
```

### **Python Client**

```python
import requests

class RedactionClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def redact_content(self, content: str, user_id: str, content_type: str = 'text'):
        """Redact content using the proxy service."""
        response = self.session.post(
            f"{self.base_url}/api/redact",
            json={
                'content': content,
                'content_type': content_type,
                'user_id': user_id
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_user_stats(self, user_id: str):
        """Get user statistics."""
        response = self.session.get(f"{self.base_url}/api/stats/{user_id}")
        response.raise_for_status()
        return response.json()

# Usage
client = RedactionClient('https://your-redaction-service.com', 'your-api-key')

result = client.redact_content(
    "Hi John, my email is john@example.com",
    "user_123"
)

if result['success']:
    print("Redacted content:", result['redaction_result']['redacted_text'])
```

This deployment approach allows you to provide redaction services to multiple users without requiring them to manage their own Tinfoil API keys, while maintaining security, performance, and cost control. 