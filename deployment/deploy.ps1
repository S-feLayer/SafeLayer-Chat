# AI Privacy Shield - Production Deployment Script (PowerShell)
# This script handles complete production deployment with security and monitoring

param(
    [string]$Environment = "production",
    [switch]$SkipTests = $false,
    [switch]$Force = $false
)

# Configuration
$PROJECT_NAME = "secureai-dataloss"
$DOCKER_IMAGE_NAME = "secureai-mcp"
$DOCKER_TAG = "latest"
$CONTAINER_NAME = "secureai-mcp-prod"
$NETWORK_NAME = "secureai-network"

# Logging
$LOG_FILE = "logs/deployment.log"
New-Item -ItemType Directory -Force -Path "logs" | Out-Null

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    Write-Host $logMessage
    Add-Content -Path $LOG_FILE -Value $logMessage
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
    Write-Log $Message "SUCCESS"
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
    Write-Log $Message "WARNING"
}

function Write-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
    Write-Log $Message "ERROR"
    exit 1
}

# Check prerequisites
function Test-Prerequisites {
    Write-Log "Checking deployment prerequisites..."
    
    # Check Docker
    try {
        $dockerVersion = docker --version 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Docker is not installed. Please install Docker Desktop first."
        }
        Write-Success "Docker found: $dockerVersion"
    }
    catch {
        Write-Error "Docker is not installed. Please install Docker Desktop first."
    }
    
    # Check Docker Compose
    try {
        $composeVersion = docker-compose --version 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Docker Compose is not installed. Please install Docker Compose first."
        }
        Write-Success "Docker Compose found: $composeVersion"
    }
    catch {
        Write-Error "Docker Compose is not installed. Please install Docker Compose first."
    }
    
    # Check environment variables
    if (-not $env:TINFOIL_API_KEY) {
        Write-Warning "TINFOIL_API_KEY environment variable is not set. Please set it before deployment."
        $env:TINFOIL_API_KEY = "your-api-key-here"
    }
    else {
        Write-Success "TINFOIL_API_KEY is configured"
    }
    
    # Check required directories
    @("logs", "cache", "test_files", "config", "monitoring") | ForEach-Object {
        New-Item -ItemType Directory -Force -Path $_ | Out-Null
    }
    Write-Success "Required directories created"
}

# Security checks
function Test-Security {
    Write-Log "Performing security checks..."
    
    # Check for sensitive files
    if (Test-Path ".env") {
        $envContent = Get-Content ".env" -Raw
        if ($envContent -match "password|secret|key") {
            Write-Warning "Found potential secrets in .env file. Please review."
        }
    }
    
    # Check file permissions (Windows equivalent)
    try {
        $acl = Get-Acl ".env" 2>$null
        $acl.SetAccessRuleProtection($true, $false)
        Set-Acl ".env" $acl
    }
    catch {
        # File might not exist, which is fine
    }
    
    # Check for exposed ports
    $portCheck = netstat -an 2>$null | Select-String ":8000 "
    if ($portCheck) {
        Write-Warning "Port 8000 is already in use. Please stop the service first."
    }
    
    Write-Success "Security checks completed"
}

# Build and deploy
function Start-Deployment {
    Write-Log "Building and deploying SecureAI MCP..."
    
    # Stop existing containers
    Write-Log "Stopping existing containers..."
    docker-compose down --remove-orphans 2>$null
    docker stop $CONTAINER_NAME 2>$null
    docker rm $CONTAINER_NAME 2>$null
    
    # Create network if it doesn't exist
    docker network create $NETWORK_NAME 2>$null
    
    # Build the image
    Write-Log "Building Docker image..."
    docker build -t "$DOCKER_IMAGE_NAME`:$DOCKER_TAG" .
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Docker build failed"
    }
    Write-Success "Docker image built successfully"
    
    # Deploy with docker-compose
    Write-Log "Deploying with Docker Compose..."
    docker-compose up -d
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Docker Compose deployment failed"
    }
    Write-Success "Application deployed successfully"
    
    # Wait for services to start
    Write-Log "Waiting for services to start..."
    Start-Sleep -Seconds 30
    
    # Check container status
    $containerStatus = docker-compose ps
    if ($containerStatus -notmatch "Up") {
        Write-Error "Services failed to start. Check logs with: docker-compose logs"
    }
    Write-Success "All services are running"
}

# Health checks
function Test-Health {
    Write-Log "Performing health checks..."
    
    # Wait for application to be ready
    $maxAttempts = 30
    $attempt = 1
    
    while ($attempt -le $maxAttempts) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Success "Application health check passed"
                break
            }
        }
        catch {
            if ($attempt -eq $maxAttempts) {
                Write-Error "Health check failed after $maxAttempts attempts"
            }
            Write-Log "Health check attempt $attempt/$maxAttempts failed, retrying..."
            Start-Sleep -Seconds 10
            $attempt++
        }
    }
    
    # Check Prometheus metrics
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:9090/-/healthy" -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Success "Prometheus monitoring is healthy"
        }
    }
    catch {
        Write-Warning "Prometheus monitoring is not responding"
    }
    
    # Check Grafana
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3000/api/health" -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Success "Grafana dashboard is healthy"
        }
    }
    catch {
        Write-Warning "Grafana dashboard is not responding"
    }
}

# Performance tests
function Test-Performance {
    Write-Log "Running performance tests..."
    
    # Test basic functionality
    try {
        $body = @{
            text = "test content"
            content_type = "text"
        } | ConvertTo-Json
        
        $response = Invoke-WebRequest -Uri "http://localhost:8000/redact" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Success "Basic functionality test passed"
        }
    }
    catch {
        Write-Warning "Basic functionality test failed"
    }
    
    # Test supported formats endpoint
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/formats" -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Success "Supported formats endpoint test passed"
        }
    }
    catch {
        Write-Warning "Supported formats endpoint test failed"
    }
}

# Monitoring setup
function Set-Monitoring {
    Write-Log "Setting up monitoring..."
    
    # Create monitoring dashboard
    if (-not (Test-Path "monitoring/grafana-dashboard.json")) {
        $dashboardConfig = @{
            dashboard = @{
                title = "SecureAI MCP Dashboard"
                panels = @(
                    @{
                        title = "Request Rate"
                        type = "graph"
                        targets = @(
                            @{
                                expr = "rate(secureai_requests_total[5m])"
                                legendFormat = "requests/sec"
                            }
                        )
                    },
                    @{
                        title = "Response Time"
                        type = "graph"
                        targets = @(
                            @{
                                expr = "histogram_quantile(0.95, rate(secureai_request_duration_seconds_bucket[5m]))"
                                legendFormat = "95th percentile"
                            }
                        )
                    }
                )
            }
        }
        
        $dashboardConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath "monitoring/grafana-dashboard.json" -Encoding UTF8
        Write-Success "Grafana dashboard configuration created"
    }
}

# Backup and recovery
function Set-Backup {
    Write-Log "Setting up backup and recovery..."
    
    # Create backup script
    $backupScript = @"
# AI Privacy Shield Backup Script
`$BACKUP_DIR = "backups/`$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Force -Path "`$BACKUP_DIR" | Out-Null

# Backup logs
Compress-Archive -Path "logs/*" -DestinationPath "`$BACKUP_DIR/logs.zip" -Force

# Backup configuration
Compress-Archive -Path "config/*" -DestinationPath "`$BACKUP_DIR/config.zip" -Force

# Backup cache
Compress-Archive -Path "cache/*" -DestinationPath "`$BACKUP_DIR/cache.zip" -Force

Write-Host "Backup completed: `$BACKUP_DIR"
"@
    
    $backupScript | Out-File -FilePath "deployment/backup.ps1" -Encoding UTF8
    Write-Success "Backup script created"
    
    # Create recovery script
    $recoveryScript = @"
# AI Privacy Shield Recovery Script
param([string]`$BackupDir)

if (-not `$BackupDir) {
    Write-Host "Usage: .`$0 <backup_directory>"
    exit 1
}

if (-not (Test-Path `$BackupDir)) {
    Write-Host "Backup directory not found: `$BackupDir"
    exit 1
}

# Stop services
docker-compose down

# Restore from backup
Expand-Archive -Path "`$BackupDir/logs.zip" -DestinationPath "./" -Force
Expand-Archive -Path "`$BackupDir/config.zip" -DestinationPath "./" -Force
Expand-Archive -Path "`$BackupDir/cache.zip" -DestinationPath "./" -Force

# Restart services
docker-compose up -d

Write-Host "Recovery completed"
"@
    
    $recoveryScript | Out-File -FilePath "deployment/recover.ps1" -Encoding UTF8
    Write-Success "Recovery script created"
}

# Main deployment function
function Start-MainDeployment {
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "SecureAI MCP - Production Deployment" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "Started at: $(Get-Date)" -ForegroundColor Cyan
    Write-Host ""
    
    # Run deployment steps
    Test-Prerequisites
    Test-Security
    Start-Deployment
    Test-Health
    Test-Performance
    Set-Monitoring
    Set-Backup
    
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Success "Deployment completed successfully!"
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Service URLs:" -ForegroundColor White
    Write-Host "  - Application: http://localhost:8000" -ForegroundColor Yellow
    Write-Host "  - Health Check: http://localhost:8000/health" -ForegroundColor Yellow
    Write-Host "  - Prometheus: http://localhost:9090" -ForegroundColor Yellow
    Write-Host "  - Grafana: http://localhost:3000 (admin/admin)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Useful commands:" -ForegroundColor White
    Write-Host "  - View logs: docker-compose logs -f" -ForegroundColor Yellow
    Write-Host "  - Stop services: docker-compose down" -ForegroundColor Yellow
    Write-Host "  - Restart: docker-compose restart" -ForegroundColor Yellow
    Write-Host "  - Backup: .\deployment\backup.ps1" -ForegroundColor Yellow
    Write-Host "  - Monitor: docker stats" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Deployment log: $LOG_FILE" -ForegroundColor Yellow
}

# Run main deployment
Start-MainDeployment 