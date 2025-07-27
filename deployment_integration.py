#!/usr/bin/env python3
"""
Deployment Integration Script for AI Privacy Shield

This script helps integrate SecureAI MCP into the AI Privacy Shield product by:
1. Setting up production configurations
2. Creating deployment packages
3. Generating integration documentation
4. Setting up monitoring and logging
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def create_production_config():
    """Create production configuration files."""
    print("Creating Production Configuration")
    print("=" * 50)
    
    # Production environment configuration
    prod_config = {
        "environment": "production",
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": "logs/secureai.log",
            "max_size": "10MB",
            "backup_count": 5
        },
        "performance": {
            "max_file_size": "100MB",
            "max_concurrent_requests": 10,
            "timeout_seconds": 300,
            "cache_enabled": True,
            "cache_size": 1000
        },
        "security": {
            "api_key_required": True,
            "rate_limiting": True,
            "max_requests_per_minute": 60,
            "allowed_file_types": [".txt", ".pdf", ".py", ".js", ".json", ".yaml", ".env"]
        },
        "monitoring": {
            "metrics_enabled": True,
            "health_check_endpoint": "/health",
            "prometheus_metrics": True
        }
    }
    
    # Save production config
    with open("config/production.json", "w") as f:
        json.dump(prod_config, f, indent=2)
    
    print("Production configuration created: config/production.json")
    
    # Docker configuration
    dockerfile_content = """# AI Privacy Shield - SecureAI MCP
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs cache test_files

# Set environment variables
ENV PYTHONPATH=/app/src
ENV SECUREAI_ENV=production

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the application
CMD ["python", "src/secureai/mcp_universal_redaction.py"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    print("Dockerfile created")
    
    # Docker Compose configuration
    docker_compose_content = """version: '3.8'

services:
  secureai-mcp:
    build: .
    ports:
      - "8000:8000"
    environment:
      - TINFOIL_API_KEY=${TINFOIL_API_KEY}
      - SECUREAI_ENV=production
    volumes:
      - ./logs:/app/logs
      - ./cache:/app/cache
      - ./test_files:/app/test_files
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: Add monitoring stack
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana
    restart: unless-stopped

volumes:
  grafana-storage:
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose_content)
    
    print("Docker Compose configuration created")
    
    return prod_config

def create_requirements_file():
    """Create requirements.txt for production deployment."""
    print("\nCreating Requirements File")
    print("=" * 50)
    
    requirements = [
        "fastmcp==0.4.1",
        "mcp==1.3.0",
        "PyMuPDF>=1.26.0",
        "tinfoil",
        "psutil>=5.8.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "prometheus-client>=0.17.0",
        "structlog>=23.0.0"
    ]
    
    with open("requirements.txt", "w") as f:
        for req in requirements:
            f.write(f"{req}\n")
    
    print("Requirements file created: requirements.txt")
    return requirements

def create_monitoring_config():
    """Create monitoring and logging configuration."""
    print("\nCreating Monitoring Configuration")
    print("=" * 50)
    
    # Create monitoring directory
    monitoring_dir = Path("monitoring")
    monitoring_dir.mkdir(exist_ok=True)
    
    # Prometheus configuration
    prometheus_config = {
        "global": {
            "scrape_interval": "15s",
            "evaluation_interval": "15s"
        },
        "scrape_configs": [
            {
                "job_name": "secureai-mcp",
                "static_configs": [
                    {
                        "targets": ["secureai-mcp:8000"]
                    }
                ],
                "metrics_path": "/metrics"
            }
        ]
    }
    
    with open("monitoring/prometheus.yml", "w") as f:
        json.dump(prometheus_config, f, indent=2)
    
    print("Prometheus configuration created")
    
    # Logging configuration
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "simple": {
                "format": "%(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": "logs/secureai.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5
            }
        },
        "loggers": {
            "secureai": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False
            }
        },
        "root": {
            "level": "WARNING",
            "handlers": ["console"]
        }
    }
    
    with open("config/logging.json", "w") as f:
        json.dump(logging_config, f, indent=2)
    
    print("Logging configuration created")
    
    return prometheus_config, logging_config

def create_integration_docs():
    """Create integration documentation."""
    print("\nCreating Integration Documentation")
    print("=" * 50)
    
    # Create docs directory
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    # API Integration Guide
    api_guide = """# AI Privacy Shield - SecureAI MCP Integration Guide

## Overview
This guide explains how to integrate SecureAI MCP into your AI Privacy Shield product.

## Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/postralai/secureai.git
cd secureai

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your TINFOIL_API_KEY
```

### 2. Basic Usage
```python
from secureai import redact_text, redact_content

# Redact text content
result = redact_text("Hello, my email is john.doe@example.com")
print(result["redacted_text"])

# Redact file content
result = redact_content("path/to/sensitive/file.pdf")
print(result["redacted_file_path"])
```

### 3. MCP Server Integration
```python
# Start MCP server
python src/secureai/mcp_universal_redaction.py

# Configure Claude Desktop
# Add to claude_desktop_config.json:
{
  "mcpServers": {
    "universal-redaction": {
      "command": "/path/to/python",
      "args": ["/path/to/mcp_universal_redaction.py"],
      "env": {
        "TINFOIL_API_KEY": "your_api_key"
      }
    }
  }
}
```

## API Reference

### Text Redaction
```python
redact_text(text: str, use_ai: bool = True) -> dict
```

### File Redaction
```python
redact_content(file_path: str, tinfoil_llm=None) -> dict
```

### PDF Redaction
```python
redact_pdf(pdf_path: str, output_path: str = None) -> dict
```

## Configuration

### Environment Variables
- `TINFOIL_API_KEY`: Your Tinfoil API key
- `SECUREAI_ENV`: Environment (development/production)
- `SECUREAI_LOG_LEVEL`: Logging level
- `SECUREAI_CACHE_DIR`: Cache directory

### Production Settings
- Enable logging to file
- Set up monitoring with Prometheus
- Configure rate limiting
- Set up health checks

## Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Metrics
```bash
curl http://localhost:8000/metrics
```

### Logs
```bash
tail -f logs/secureai.log
```

## Troubleshooting

### Common Issues
1. **Permission Errors**: Run as administrator on Windows
2. **API Key Issues**: Verify Tinfoil API key is valid
3. **Memory Issues**: Process large files in chunks
4. **Performance Issues**: Use regex-only mode for high volume

### Support
- Check logs in `logs/secureai.log`
- Review monitoring metrics
- Contact support team
"""
    
    with open("docs/integration_guide.md", "w") as f:
        f.write(api_guide)
    
    print("Integration guide created: docs/integration_guide.md")
    
    # Deployment Guide
    deployment_guide = """# AI Privacy Shield - Deployment Guide

## Docker Deployment

### 1. Build and Run
```bash
# Build the image
docker build -t ai-privacy-shield .

# Run with Docker Compose
docker-compose up -d
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

### 3. Production Deployment
```bash
# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose ps
```

## Kubernetes Deployment

### 1. Create Namespace
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ai-privacy-shield
```

### 2. Deploy Application
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secureai-mcp
  namespace: ai-privacy-shield
spec:
  replicas: 3
  selector:
    matchLabels:
      app: secureai-mcp
  template:
    metadata:
      labels:
        app: secureai-mcp
    spec:
      containers:
      - name: secureai-mcp
        image: ai-privacy-shield:latest
        ports:
        - containerPort: 8000
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
```

## Monitoring Setup

### 1. Prometheus Configuration
```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'secureai-mcp'
    static_configs:
      - targets: ['secureai-mcp:8000']
```

### 2. Grafana Dashboards
Import the provided Grafana dashboard JSON files for monitoring.

## Security Considerations

### 1. API Key Management
- Use Kubernetes secrets for API keys
- Rotate keys regularly
- Monitor API usage

### 2. Network Security
- Use internal networks for MCP communication
- Implement proper firewall rules
- Use TLS for external communication

### 3. Access Control
- Implement authentication for admin endpoints
- Use role-based access control
- Audit all access logs
"""
    
    with open("docs/deployment_guide.md", "w") as f:
        f.write(deployment_guide)
    
    print("Deployment guide created: docs/deployment_guide.md")

def create_health_check():
    """Create health check endpoint."""
    print("\nCreating Health Check")
    print("=" * 50)
    
    health_check_code = """#!/usr/bin/env python3
\"\"\"
Health Check Endpoint for SecureAI MCP
\"\"\"

import json
import psutil
import time
from datetime import datetime

def health_check():
    \"\"\"Perform health check and return status.\"\"\"
    try:
        # Check system resources
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Check if SecureAI modules can be imported
        try:
            import secureai
            secureai_status = "healthy"
        except ImportError:
            secureai_status = "unhealthy"
        
        # Check API key (if available)
        api_key_status = "unknown"
        try:
            import os
            if os.getenv("TINFOIL_API_KEY"):
                api_key_status = "configured"
            else:
                api_key_status = "missing"
        except:
            pass
        
        health_data = {
            "status": "healthy" if secureai_status == "healthy" else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "components": {
                "secureai": secureai_status,
                "api_key": api_key_status
            },
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "disk_percent": disk.percent
            }
        }
        
        return health_data
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

if __name__ == "__main__":
    health = health_check()
    print(json.dumps(health, indent=2))
"""
    
    with open("src/secureai/health_check.py", "w") as f:
        f.write(health_check_code)
    
    print("Health check module created: src/secureai/health_check.py")

def create_deployment_package():
    """Create deployment package."""
    print("\nCreating Deployment Package")
    print("=" * 50)
    
    # Create deployment directory
    deploy_dir = Path("deployment")
    deploy_dir.mkdir(exist_ok=True)
    
    # Files to include in deployment
    deployment_files = [
        "src/",
        "config/",
        "requirements.txt",
        "Dockerfile",
        "docker-compose.yml",
        "README.md",
        "docs/",
        ".env.example"
    ]
    
    # Create deployment script
    deploy_script = """#!/bin/bash
# AI Privacy Shield Deployment Script

set -e

echo "Deploying AI Privacy Shield - SecureAI MCP"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Set up environment
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file and add your TINFOIL_API_KEY"
    echo "   Then run this script again."
    exit 1
fi

# Build and start services
echo "Building Docker image..."
docker-compose build

echo "Starting services..."
docker-compose up -d

echo "Waiting for services to start..."
sleep 10

# Check health
echo "Checking service health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "Services are healthy!"
else
    echo "Services are not responding. Check logs with: docker-compose logs"
    exit 1
fi

echo "Deployment completed successfully!"
echo ""
echo "Service URLs:"
echo "   - SecureAI MCP: http://localhost:8000"
echo "   - Prometheus: http://localhost:9090"
echo "   - Grafana: http://localhost:3000 (admin/admin)"
echo ""
echo "Documentation: docs/"
echo "Monitoring: http://localhost:3000"
"""
    
    with open("deployment/deploy.sh", "w") as f:
        f.write(deploy_script)
    
    # Make script executable
    os.chmod("deployment/deploy.sh", 0o755)
    
    print("Deployment script created: deployment/deploy.sh")
    
    # Create deployment README
    deploy_readme = """# AI Privacy Shield - Deployment Package

This package contains everything needed to deploy SecureAI MCP in production.

## Quick Deploy

1. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your TINFOIL_API_KEY
   ```

2. **Deploy:**
   ```bash
   ./deployment/deploy.sh
   ```

## Manual Deployment

1. **Build Docker image:**
   ```bash
   docker build -t ai-privacy-shield .
   ```

2. **Start services:**
   ```bash
   docker-compose up -d
   ```

3. **Verify deployment:**
   ```bash
   curl http://localhost:8000/health
   ```

## Configuration

- Edit `config/production.json` for production settings
- Modify `docker-compose.yml` for custom deployment
- Update monitoring configuration in `monitoring/`

## Monitoring

- **Health Check:** http://localhost:8000/health
- **Metrics:** http://localhost:8000/metrics
- **Grafana:** http://localhost:3000 (admin/admin)
- **Prometheus:** http://localhost:9090

## Troubleshooting

1. Check logs: `docker-compose logs`
2. Verify environment: `docker-compose exec secureai-mcp env`
3. Test health: `curl http://localhost:8000/health`
4. Check metrics: `curl http://localhost:8000/metrics`

## Support

- Documentation: `docs/`
- Logs: `logs/`
- Configuration: `config/`
"""
    
    with open("deployment/README.md", "w") as f:
        f.write(deploy_readme)
    
    print("Deployment README created: deployment/README.md")

def main():
    """Main deployment integration function."""
    print("AI Privacy Shield - Deployment Integration")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create necessary directories
    Path("config").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path("cache").mkdir(exist_ok=True)
    
    # Run integration steps
    create_production_config()
    create_requirements_file()
    create_monitoring_config()
    create_integration_docs()
    create_health_check()
    create_deployment_package()
    
    print("\nDeployment integration completed!")
    print("\nNext steps:")
    print("1. Review configuration in config/")
    print("2. Set up environment variables in .env")
    print("3. Test deployment with: ./deployment/deploy.sh")
    print("4. Monitor with: http://localhost:3000")
    print("5. Check health: http://localhost:8000/health")
    
    print("\nDocumentation:")
    print("- Integration Guide: docs/integration_guide.md")
    print("- Deployment Guide: docs/deployment_guide.md")
    print("- Windows Troubleshooting: docs/windows_troubleshooting.md")

if __name__ == "__main__":
    main() 