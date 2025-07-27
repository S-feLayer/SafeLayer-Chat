# SecureAI MCP - Production Deployment Guide

This guide provides comprehensive instructions for deploying the SecureAI MCP service to production environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Security Configuration](#security-configuration)
4. [Deployment Options](#deployment-options)
5. [Monitoring and Observability](#monitoring-and-observability)
6. [Backup and Recovery](#backup-and-recovery)
7. [Performance Optimization](#performance-optimization)
8. [Troubleshooting](#troubleshooting)
9. [Maintenance](#maintenance)

## Prerequisites

### System Requirements

- **Operating System**: Linux (Ubuntu 20.04+), macOS, or Windows 10+
- **Docker**: Version 20.10+ with Docker Compose
- **Memory**: Minimum 4GB RAM, Recommended 8GB+
- **Storage**: Minimum 10GB free space
- **Network**: Internet access for API calls and package downloads

### Software Dependencies

- Python 3.10+ (for local development)
- Docker Desktop (for containerized deployment)
- Git (for version control)

### API Keys and Credentials

- **Tinfoil API Key**: Required for AI-powered content analysis
- **Environment Variables**: Configured in `.env` file

## Environment Setup

### 1. Clone and Prepare Repository

```bash
git clone <repository-url>
cd secureai-dataloss-main
```

### 2. Configure Environment Variables

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your production values:

```env
# API Configuration
TINFOIL_API_KEY=your_actual_tinfoil_api_key

# Environment
SECUREAI_ENV=production

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Security
API_KEY_REQUIRED=true
RATE_LIMITING=true
MAX_REQUESTS_PER_MINUTE=60
```

### 3. Create Required Directories

```bash
mkdir -p logs cache test_files config monitoring backups
```

## Security Configuration

### 1. File Permissions

Set appropriate file permissions:

```bash
# Linux/macOS
chmod 600 .env
chmod 755 logs cache test_files
chmod +x deployment/*.sh

# Windows PowerShell
icacls .env /inheritance:r /grant:r "%USERNAME%:F"
```

### 2. Network Security

- Configure firewall rules to allow only necessary ports
- Use reverse proxy (nginx/traefik) for SSL termination
- Implement rate limiting at the network level

### 3. API Security

- Rotate API keys regularly
- Use environment variables for sensitive data
- Implement request validation and sanitization

## Deployment Options

### Option 1: Docker Compose (Recommended)

#### Quick Deployment

```bash
# Windows PowerShell
.\deployment\deploy.ps1

# Linux/macOS
./deployment/deploy.sh
```

#### Manual Docker Deployment

```bash
# Build and start services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### Option 2: Kubernetes Deployment

Create Kubernetes manifests:

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secureai-mcp
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
        image: secureai-mcp:latest
        ports:
        - containerPort: 8000
        env:
        - name: TINFOIL_API_KEY
          valueFrom:
            secretKeyRef:
              name: secureai-secrets
              key: tinfoil-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

### Option 3: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python src/secure_AI/mcp_universal_redaction.py
```

## Monitoring and Observability

### 1. Health Checks

Monitor service health:

```bash
# Check application health
curl http://localhost:8000/health

# Check Prometheus metrics
curl http://localhost:9090/-/healthy

# Check Grafana dashboard
curl http://localhost:3000/api/health
```

### 2. Logging

Configure structured logging:

```python
import logging
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

### 3. Metrics Collection

Prometheus metrics are automatically exposed at `/metrics`:

- Request count and duration
- System resource usage
- Active connections
- Error rates

### 4. Alerting

Configure alerts for critical metrics:

```yaml
# monitoring/alerts.yaml
groups:
- name: secureai_alerts
  rules:
  - alert: HighErrorRate
    expr: rate(secureai_requests_total{endpoint=~".*error.*"}[5m]) > 0.1
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "High error rate detected"
      description: "Error rate is {{ $value }} errors per second"
```

## Backup and Recovery

### 1. Automated Backups

```bash
# Create backup
./deployment/backup.sh

# Windows PowerShell
.\deployment\backup.ps1
```

### 2. Manual Backup

```bash
# Backup configuration
tar -czf backup-config-$(date +%Y%m%d).tar.gz config/

# Backup logs
tar -czf backup-logs-$(date +%Y%m%d).tar.gz logs/

# Backup cache (if needed)
tar -czf backup-cache-$(date +%Y%m%d).tar.gz cache/
```

### 3. Recovery Procedures

```bash
# Stop services
docker-compose down

# Restore from backup
./deployment/recover.sh backup-20231201_143022

# Restart services
docker-compose up -d
```

## Performance Optimization

### 1. Resource Limits

Configure Docker resource limits:

```yaml
# docker-compose.yml
services:
  secureai-mcp:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

### 2. Caching Strategy

Enable caching for improved performance:

```python
# Configure Redis cache
CACHE_ENABLED=true
CACHE_TYPE=redis
CACHE_REDIS_URL=redis://localhost:6379/0
```

### 3. Load Balancing

For high availability, use multiple instances:

```yaml
# docker-compose.yml
services:
  secureai-mcp:
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
```

## Troubleshooting

### Common Issues

#### 1. Service Won't Start

```bash
# Check logs
docker-compose logs secureai-mcp

# Check environment variables
docker-compose config

# Verify API key
echo $TINFOIL_API_KEY
```

#### 2. High Memory Usage

```bash
# Monitor memory usage
docker stats

# Check for memory leaks
docker exec secureai-mcp ps aux --sort=-%mem
```

#### 3. Network Connectivity Issues

```bash
# Test API connectivity
curl -X POST http://localhost:8000/health

# Check port availability
netstat -tuln | grep 8000
```

### Debug Mode

Enable debug logging:

```bash
# Set debug environment variable
export LOG_LEVEL=DEBUG

# Restart services
docker-compose restart
```

## Maintenance

### 1. Regular Updates

```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Rebuild Docker image
docker-compose build --no-cache

# Restart services
docker-compose up -d
```

### 2. Log Rotation

Configure log rotation:

```bash
# Linux logrotate configuration
sudo tee /etc/logrotate.d/secureai << EOF
logs/secureai.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
}
EOF
```

### 3. Health Monitoring

Set up automated health checks:

```bash
# Create health check script
cat > /usr/local/bin/secureai-health-check << 'EOF'
#!/bin/bash
curl -f http://localhost:8000/health || exit 1
EOF

chmod +x /usr/local/bin/secureai-health-check

# Add to crontab
echo "*/5 * * * * /usr/local/bin/secureai-health-check" | crontab -
```

### 4. Performance Monitoring

Monitor key metrics:

- Request latency (target: < 2 seconds)
- Error rate (target: < 1%)
- Memory usage (target: < 80%)
- CPU usage (target: < 70%)

## Security Best Practices

1. **Regular Security Updates**: Keep all dependencies updated
2. **Access Control**: Implement proper authentication and authorization
3. **Data Encryption**: Encrypt sensitive data at rest and in transit
4. **Audit Logging**: Log all access and changes
5. **Vulnerability Scanning**: Regular security scans
6. **Backup Security**: Encrypt backup files

## Support and Documentation

- **Documentation**: Check `docs/` directory for detailed guides
- **Issues**: Report issues on the project repository
- **Monitoring**: Use Grafana dashboard for real-time monitoring
- **Logs**: Check `logs/` directory for application logs

## Emergency Procedures

### Service Outage

1. Check health endpoints
2. Review recent logs
3. Restart services if necessary
4. Contact support if issues persist

### Data Loss

1. Stop all services immediately
2. Assess the scope of data loss
3. Restore from latest backup
4. Investigate root cause

### Security Incident

1. Isolate affected systems
2. Preserve evidence
3. Assess impact
4. Implement containment measures
5. Notify stakeholders

---

For additional support or questions, refer to the project documentation or contact the development team. 