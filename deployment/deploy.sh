#!/bin/bash

# Privacy Firewall - Production Deployment Script
# This script handles complete production deployment with security and monitoring

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="privacy-firewall"
DOCKER_IMAGE_NAME="privacy-firewall-mcp"
DOCKER_TAG="latest"
CONTAINER_NAME="privacy-firewall-mcp-prod"
NETWORK_NAME="privacy-firewall-network"

# Logging
LOG_FILE="logs/deployment.log"
mkdir -p logs

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}✓${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}⚠${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}✗${NC} $1" | tee -a "$LOG_FILE"
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking deployment prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
    fi
    success "Docker found: $(docker --version)"
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed. Please install Docker Compose first."
    fi
    success "Docker Compose found: $(docker-compose --version)"
    
    # Check environment variables
    if [ -z "$TINFOIL_API_KEY" ]; then
        warning "TINFOIL_API_KEY environment variable is not set. Please set it before deployment."
        export TINFOIL_API_KEY="your-api-key-here"
    else
        success "TINFOIL_API_KEY is configured"
    fi
    
    # Check required directories
    mkdir -p logs cache test_files config monitoring
    success "Required directories created"
}

# Security checks
security_checks() {
    log "Performing security checks..."
    
    # Check for sensitive files
    if [ -f ".env" ]; then
        if grep -q "password\|secret\|key" .env; then
            warning "Found potential secrets in .env file. Please review."
        fi
    fi
    
    # Check file permissions
    chmod 600 .env 2>/dev/null || true
    chmod 755 logs cache test_files
    success "File permissions set"
    
    # Check for exposed ports
    if netstat -tuln 2>/dev/null | grep -q ":8000 "; then
        warning "Port 8000 is already in use. Please stop the service first."
    fi
    
    success "Security checks completed"
}

# Build and deploy
build_and_deploy() {
    log "Building and deploying SecureAI MCP..."
    
    # Stop existing containers
    log "Stopping existing containers..."
    docker-compose down --remove-orphans 2>/dev/null || true
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
    
    # Create network if it doesn't exist
    docker network create "$NETWORK_NAME" 2>/dev/null || true
    
    # Build the image
    log "Building Docker image..."
    docker build -t "$DOCKER_IMAGE_NAME:$DOCKER_TAG" . || error "Docker build failed"
    success "Docker image built successfully"
    
    # Deploy with docker-compose
    log "Deploying with Docker Compose..."
    docker-compose up -d || error "Docker Compose deployment failed"
    success "Application deployed successfully"
    
    # Wait for services to start
    log "Waiting for services to start..."
    sleep 30
    
    # Check container status
    if ! docker-compose ps | grep -q "Up"; then
        error "Services failed to start. Check logs with: docker-compose logs"
    fi
    success "All services are running"
}

# Health checks
health_checks() {
    log "Performing health checks..."
    
    # Wait for application to be ready
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s http://localhost:8000/health > /dev/null 2>&1; then
            success "Application health check passed"
            break
        fi
        
        if [ $attempt -eq $max_attempts ]; then
            error "Health check failed after $max_attempts attempts"
        fi
        
        log "Health check attempt $attempt/$max_attempts failed, retrying..."
        sleep 10
        ((attempt++))
    done
    
    # Check Prometheus metrics
    if curl -f -s http://localhost:9090/-/healthy > /dev/null 2>&1; then
        success "Prometheus monitoring is healthy"
    else
        warning "Prometheus monitoring is not responding"
    fi
    
    # Check Grafana
    if curl -f -s http://localhost:3000/api/health > /dev/null 2>&1; then
        success "Grafana dashboard is healthy"
    else
        warning "Grafana dashboard is not responding"
    fi
}

# Performance tests
performance_tests() {
    log "Running performance tests..."
    
    # Test basic functionality
    if curl -f -s -X POST http://localhost:8000/redact \
        -H "Content-Type: application/json" \
        -d '{"text": "test content", "content_type": "text"}' > /dev/null 2>&1; then
        success "Basic functionality test passed"
    else
        warning "Basic functionality test failed"
    fi
    
    # Test supported formats endpoint
    if curl -f -s http://localhost:8000/formats > /dev/null 2>&1; then
        success "Supported formats endpoint test passed"
    else
        warning "Supported formats endpoint test failed"
    fi
}

# Monitoring setup
setup_monitoring() {
    log "Setting up monitoring..."
    
    # Create monitoring dashboard
    if [ ! -f "monitoring/grafana-dashboard.json" ]; then
        cat > monitoring/grafana-dashboard.json << 'EOF'
{
  "dashboard": {
    "title": "SecureAI MCP Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(secureai_requests_total[5m])",
            "legendFormat": "requests/sec"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(secureai_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      }
    ]
  }
}
EOF
        success "Grafana dashboard configuration created"
    fi
    
    # Setup log rotation
    if [ ! -f "/etc/logrotate.d/secureai" ]; then
        sudo tee /etc/logrotate.d/secureai > /dev/null << 'EOF'
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
        success "Log rotation configured"
    fi
}

# Backup and recovery
setup_backup() {
    log "Setting up backup and recovery..."
    
    # Create backup script
    cat > deployment/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup logs
tar -czf "$BACKUP_DIR/logs.tar.gz" logs/

# Backup configuration
tar -czf "$BACKUP_DIR/config.tar.gz" config/

# Backup cache (if needed)
tar -czf "$BACKUP_DIR/cache.tar.gz" cache/

echo "Backup completed: $BACKUP_DIR"
EOF
    
    chmod +x deployment/backup.sh
    success "Backup script created"
    
    # Create recovery script
    cat > deployment/recover.sh << 'EOF'
#!/bin/bash
if [ -z "$1" ]; then
    echo "Usage: $0 <backup_directory>"
    exit 1
fi

BACKUP_DIR="$1"
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Backup directory not found: $BACKUP_DIR"
    exit 1
fi

# Stop services
docker-compose down

# Restore from backup
tar -xzf "$BACKUP_DIR/logs.tar.gz" -C ./
tar -xzf "$BACKUP_DIR/config.tar.gz" -C ./
tar -xzf "$BACKUP_DIR/cache.tar.gz" -C ./

# Restart services
docker-compose up -d

echo "Recovery completed"
EOF
    
    chmod +x deployment/recover.sh
    success "Recovery script created"
}

# Main deployment function
main() {
    echo "=========================================="
    echo "SecureAI MCP - Production Deployment"
    echo "=========================================="
    echo "Started at: $(date)"
    echo ""
    
    # Run deployment steps
    check_prerequisites
    security_checks
    build_and_deploy
    health_checks
    performance_tests
    setup_monitoring
    setup_backup
    
    echo ""
    echo "=========================================="
    success "Deployment completed successfully!"
    echo "=========================================="
    echo ""
    echo "Service URLs:"
    echo "  - Application: http://localhost:8000"
    echo "  - Health Check: http://localhost:8000/health"
    echo "  - Prometheus: http://localhost:9090"
    echo "  - Grafana: http://localhost:3000 (admin/admin)"
    echo ""
    echo "Useful commands:"
    echo "  - View logs: docker-compose logs -f"
    echo "  - Stop services: docker-compose down"
    echo "  - Restart: docker-compose restart"
    echo "  - Backup: ./deployment/backup.sh"
    echo "  - Monitor: docker stats"
    echo ""
    echo "Deployment log: $LOG_FILE"
}

# Run main function
main "$@"
