# SafeLayer-Chat - Universal Privacy Firewall

A production-ready universal privacy firewall for PDFs, code files, and text content that automatically detects and redacts sensitive data using AI-powered analysis.

## Features

- **Universal Content Support**: PDFs, code files, text documents
- **AI-Powered Detection**: Advanced sensitive data identification
- **Production Ready**: Complete monitoring, logging, and deployment setup
- **MCP Protocol**: Model Context Protocol integration
- **Real-time Processing**: Fast, efficient content redaction
- **Comprehensive Monitoring**: Prometheus metrics, Grafana dashboards
- **Security Focused**: Enterprise-grade security features

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Tinfoil API key
- 4GB+ RAM, 10GB+ storage

### Production Deployment

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd secureai-dataloss-main
   cp .env.example .env
   ```

2. **Configure Environment**
   ```bash
   # Edit .env file with your settings
   TINFOIL_API_KEY=your_api_key_here
   SECUREAI_ENV=production
   ```

3. **Deploy with One Command**
   ```bash
   # Windows PowerShell
   .\deployment\deploy.ps1
   
   # Linux/macOS
   ./deployment/deploy.sh
   ```

4. **Access Services**
   - Application: http://localhost:8000
   - Health Check: http://localhost:8000/health
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (admin/admin)

### Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python src/secure_AI/mcp_universal_redaction.py
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client Apps   │    │   MCP Server    │    │   Tinfoil API   │
│                 │◄──►│                 │◄──►│                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Redaction      │
                       │  Engine         │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  File Output    │
                       │  (PDF/Code)     │
                       └─────────────────┘
```

## Production Features

### Monitoring & Observability
- **Health Checks**: Comprehensive system health monitoring
- **Prometheus Metrics**: Request rates, response times, system resources
- **Grafana Dashboards**: Real-time visualization and alerting
- **Structured Logging**: JSON-formatted logs with rotation

### Security
- **API Key Authentication**: Secure API access
- **Rate Limiting**: Protection against abuse
- **Input Validation**: Sanitized content processing
- **File Permissions**: Secure file handling

### Performance
- **Resource Limits**: Configurable CPU/memory limits
- **Caching**: Intelligent result caching
- **Concurrent Processing**: Multi-threaded operations
- **Load Balancing**: Horizontal scaling support

### Backup & Recovery
- **Automated Backups**: Scheduled backup scripts
- **Point-in-time Recovery**: Complete system restoration
- **Configuration Management**: Version-controlled settings

## API Usage

### Basic Redaction

```python
from secureai import SecureAI

# Initialize client
secureai = SecureAI(api_key="your_key")

# Redact PDF
result = secureai.redact_pdf("document.pdf")

# Redact code
result = secureai.redact_code("source.py")

# Redact text
result = secureai.redact_text("sensitive content")
```

### MCP Integration

```python
# Connect to MCP server
from mcp import ClientSession

async with ClientSession() as session:
    # Redact content
    result = await session.call_tool(
        "redact_content",
        {"file_path": "document.pdf"}
    )
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TINFOIL_API_KEY` | Tinfoil API key | Required |
| `SECUREAI_ENV` | Environment (dev/prod) | development |
| `LOG_LEVEL` | Logging level | INFO |
| `MAX_FILE_SIZE` | Maximum file size | 100MB |
| `CACHE_ENABLED` | Enable caching | true |

### Production Configuration

```yaml
# docker-compose.yml
services:
  secureai-mcp:
    image: secureai-mcp:latest
    environment:
      - TINFOIL_API_KEY=${TINFOIL_API_KEY}
      - SECUREAI_ENV=production
    ports:
      - "8000:8000"
    volumes:
      - ./logs:/app/logs
      - ./cache:/app/cache
    restart: unless-stopped
```

## Monitoring

### Health Checks

```bash
# Application health
curl http://localhost:8000/health

# Metrics endpoint
curl http://localhost:8000/metrics
```

### Key Metrics

- **Request Rate**: Requests per second
- **Response Time**: 95th percentile latency
- **Error Rate**: Failed requests percentage
- **System Resources**: CPU, memory, disk usage

### Alerts

Configure alerts for:
- High error rates (>1%)
- Slow response times (>2s)
- High resource usage (>80%)
- Service unavailability

## Deployment Options

### 1. Docker Compose (Recommended)
```bash
docker-compose up -d
```

### 2. Kubernetes
```bash
kubectl apply -f k8s/
```

### 3. Local Development
```bash
python src/secure_AI/mcp_universal_redaction.py
```

## Troubleshooting

### Common Issues

1. **Service Won't Start**
   ```bash
   docker-compose logs secureai-mcp
   ```

2. **API Key Issues**
   ```bash
   echo $TINFOIL_API_KEY
   ```

3. **High Memory Usage**
   ```bash
   docker stats
   ```

### Debug Mode

```bash
export LOG_LEVEL=DEBUG
docker-compose restart
```

## Maintenance

### Regular Tasks

- **Updates**: `docker-compose pull && docker-compose up -d`
- **Backups**: `./deployment/backup.sh`
- **Log Rotation**: Automatic via logrotate
- **Health Monitoring**: Automated checks every 5 minutes

### Performance Tuning

- Adjust resource limits in docker-compose.yml
- Configure caching parameters
- Optimize file processing settings
- Monitor and adjust based on usage patterns

## Security Considerations

- Keep API keys secure and rotate regularly
- Use HTTPS in production
- Implement proper access controls
- Regular security updates
- Monitor for suspicious activity

## Support

- **Documentation**: [Production Deployment Guide](docs/PRODUCTION_DEPLOYMENT_GUIDE.md)
- **Issues**: Report on GitHub
- **Monitoring**: Grafana dashboard
- **Logs**: `logs/` directory

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Ready for Production**: This project includes comprehensive production deployment capabilities with monitoring, security, and scalability features.

