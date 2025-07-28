from mcp.server.fastmcp import FastMCP
import os
import subprocess
import time
import logging
import json
from typing import Dict, Any, Optional
from .redact_content import redact_content, get_supported_formats
from .tinfoil_llm import TinfoilLLM
from .health_check import get_health_response, get_metrics_response, record_request_duration, update_active_connections

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/secureai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create a FastMCP server instance
mcp = FastMCP(name="PrivacyFirewallServer")
tinfoil_llm = TinfoilLLM()

# Track active connections
active_connections = 0

@mcp.tool("redact_content")
def process_content(params):
    """
    Universal redaction tool that handles PDFs, code files, and text content.
    
    Parameters can be:
    - String: file path or text content
    - Dict: with keys like 'file_path', 'text', 'content_type', etc.
    """
    start_time = time.time()
    global active_connections
    active_connections += 1
    update_active_connections(active_connections)
    
    try:
        logger.info(f"Processing content request: {type(params)}")
        
        # Process the input
        result = redact_content(params, tinfoil_llm)
        
        # Record metrics
        duration = time.time() - start_time
        record_request_duration('/redact_content', duration)
        
        if result.get("success"):
            logger.info(f"Content processing successful: {result.get('content_type', 'unknown')}")
            
            # Try to open files if they exist (only in development)
            if os.getenv('SECUREAI_ENV') != 'production':
                if result.get("content_type") == "pdf":
                    try:
                        redacted_path = result["redaction_summary"]["redacted_pdf_path"]
                        highlighted_path = result["highlighted_path"]
                        
                        # Try to open files
                        try:
                            subprocess.run(["open", redacted_path], check=True)
                            subprocess.run(["open", highlighted_path], check=True)
                        except subprocess.CalledProcessError:
                            try:
                                subprocess.run(["xdg-open", redacted_path], check=True)
                                subprocess.run(["xdg-open", highlighted_path], check=True)
                            except (subprocess.CalledProcessError, FileNotFoundError):
                                logger.debug("Could not open PDF files automatically")
                    except Exception as e:
                        logger.debug(f"Could not open files: {e}")
                
                elif result.get("content_type") == "code":
                    try:
                        redacted_path = result["redaction_result"]["redacted_file_path"]
                        try:
                            subprocess.run(["open", redacted_path], check=True)
                        except subprocess.CalledProcessError:
                            try:
                                subprocess.run(["xdg-open", redacted_path], check=True)
                            except (subprocess.CalledProcessError, FileNotFoundError):
                                logger.debug("Could not open code file automatically")
                    except Exception as e:
                        logger.debug(f"Could not open file: {e}")
        else:
            logger.error(f"Content processing failed: {result.get('error', 'Unknown error')}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing content: {str(e)}", exc_info=True)
        duration = time.time() - start_time
        record_request_duration('/redact_content', duration)
        return {"success": False, "error": f"Error processing content: {str(e)}"}
    finally:
        active_connections -= 1
        update_active_connections(active_connections)

@mcp.tool("redact_pdf")
def process_pdf(params):
    """
    Legacy PDF redaction tool for backward compatibility.
    """
    return process_content(params)

@mcp.tool("redact_code")
def process_code(params):
    """
    Code file redaction tool.
    """
    if isinstance(params, str):
        params = {"file_path": params, "content_type": "code"}
    elif isinstance(params, dict):
        params["content_type"] = "code"
    
    return process_content(params)

@mcp.tool("redact_text")
def process_text(params):
    """
    Text content redaction tool.
    """
    if isinstance(params, str):
        params = {"text": params, "content_type": "text"}
    elif isinstance(params, dict):
        params["content_type"] = "text"
    
    return process_content(params)

@mcp.tool("get_supported_formats")
def get_formats(params=None):
    """
    Get list of supported file formats and content types.
    """
    start_time = time.time()
    global active_connections
    active_connections += 1
    update_active_connections(active_connections)
    
    try:
        logger.info("Getting supported formats")
        result = {
            "success": True,
            "supported_formats": get_supported_formats()
        }
        
        duration = time.time() - start_time
        record_request_duration('/get_supported_formats', duration)
        
        return result
    except Exception as e:
        logger.error(f"Error getting supported formats: {str(e)}", exc_info=True)
        duration = time.time() - start_time
        record_request_duration('/get_supported_formats', duration)
        return {"success": False, "error": f"Error getting supported formats: {str(e)}"}
    finally:
        active_connections -= 1
        update_active_connections(active_connections)

@mcp.tool("health_check")
def health_check(params=None):
    """
    Get system health status and metrics.
    """
    start_time = time.time()
    global active_connections
    active_connections += 1
    update_active_connections(active_connections)
    
    try:
        logger.info("Performing health check")
        result = get_health_response()
        
        duration = time.time() - start_time
        record_request_duration('/health_check', duration)
        
        return result
    except Exception as e:
        logger.error(f"Error during health check: {str(e)}", exc_info=True)
        duration = time.time() - start_time
        record_request_duration('/health_check', duration)
        return {"success": False, "error": f"Error during health check: {str(e)}"}
    finally:
        active_connections -= 1
        update_active_connections(active_connections)

@mcp.tool("get_metrics")
def get_metrics(params=None):
    """
    Get Prometheus metrics for monitoring.
    """
    start_time = time.time()
    global active_connections
    active_connections += 1
    update_active_connections(active_connections)
    
    try:
        logger.debug("Getting metrics")
        metrics = get_metrics_response()
        
        duration = time.time() - start_time
        record_request_duration('/get_metrics', duration)
        
        return {
            "success": True,
            "metrics": metrics,
            "content_type": "text/plain"
        }
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}", exc_info=True)
        duration = time.time() - start_time
        record_request_duration('/get_metrics', duration)
        return {"success": False, "error": f"Error getting metrics: {str(e)}"}
    finally:
        active_connections -= 1
        update_active_connections(active_connections)

# Define resources for different content types
@mcp.resource("content://redact")
def redact_content_endpoint():
    return {
        "meta": None,
        "contents": [{
            "uri": "content://redact",
            "mime_type": "application/json",
            "text": "Universal content redaction endpoint"
        }]
    }

@mcp.resource("pdf://redact")
def redact_pdf_endpoint():
    return {
        "meta": None,
        "contents": [{
            "uri": "pdf://redact",
            "mime_type": "application/json",
            "text": "PDF redaction endpoint"
        }]
    }

@mcp.resource("code://redact")
def redact_code_endpoint():
    return {
        "meta": None,
        "contents": [{
            "uri": "code://redact",
            "mime_type": "application/json",
            "text": "Code redaction endpoint"
        }]
    }

@mcp.resource("text://redact")
def redact_text_endpoint():
    return {
        "meta": None,
        "contents": [{
            "uri": "text://redact",
            "mime_type": "application/json",
            "text": "Text redaction endpoint"
        }]
    }

@mcp.resource("health://status")
def health_endpoint():
    return {
        "meta": None,
        "contents": [{
            "uri": "health://status",
            "mime_type": "application/json",
            "text": json.dumps(get_health_response(), indent=2)
        }]
    }

@mcp.resource("metrics://prometheus")
def metrics_endpoint():
    return {
        "meta": None,
        "contents": [{
            "uri": "metrics://prometheus",
            "mime_type": "text/plain",
            "text": get_metrics_response()
        }]
    }

# Startup logging
logger.info("Privacy Firewall MCP Server starting up...")
logger.info(f"Environment: {os.getenv('PRIVACY_FIREWALL_ENV', 'development')}")
logger.info(f"Tinfoil API Key configured: {'Yes' if os.getenv('TINFOIL_API_KEY') else 'No'}")

if __name__ == "__main__":
    try:
        logger.info("Starting Privacy Firewall MCP Server...")
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server failed to start: {str(e)}", exc_info=True)
        raise 