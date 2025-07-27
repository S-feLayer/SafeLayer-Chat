# AI Privacy Shield - Deployment Guide

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
