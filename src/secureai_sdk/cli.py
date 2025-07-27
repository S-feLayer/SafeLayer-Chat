#!/usr/bin/env python3
"""
SecureAI SDK Command Line Interface

Provides command-line access to SecureAI functionality.
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Optional

from .client import SecureAI
from .exceptions import SecureAIError
from .models import ProcessingOptions

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="SecureAI SDK - Universal Privacy Firewall",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Redact text content
  secureai text "My email is john@example.com and phone is 555-123-4567"
  
  # Redact PDF file
  secureai pdf document.pdf
  
  # Redact code file
  secureai code source.py
  
  # Check service health
  secureai health
  
  # Get supported formats
  secureai formats
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Text redaction command
    text_parser = subparsers.add_parser("text", help="Redact sensitive data from text")
    text_parser.add_argument("content", help="Text content to redact")
    text_parser.add_argument("--output", "-o", help="Output file path")
    text_parser.add_argument("--aggressive", action="store_true", help="Enable aggressive redaction mode")
    text_parser.add_argument("--sensitivity", choices=["low", "medium", "high"], default="medium", help="Sensitivity level")
    
    # PDF redaction command
    pdf_parser = subparsers.add_parser("pdf", help="Redact sensitive data from PDF file")
    pdf_parser.add_argument("file", help="PDF file path")
    pdf_parser.add_argument("--output", "-o", help="Output file path")
    pdf_parser.add_argument("--aggressive", action="store_true", help="Enable aggressive redaction mode")
    pdf_parser.add_argument("--sensitivity", choices=["low", "medium", "high"], default="medium", help="Sensitivity level")
    
    # Code redaction command
    code_parser = subparsers.add_parser("code", help="Redact sensitive data from code file")
    code_parser.add_argument("file", help="Code file path")
    code_parser.add_argument("--output", "-o", help="Output file path")
    code_parser.add_argument("--aggressive", action="store_true", help="Enable aggressive redaction mode")
    code_parser.add_argument("--sensitivity", choices=["low", "medium", "high"], default="medium", help="Sensitivity level")
    
    # Health check command
    health_parser = subparsers.add_parser("health", help="Check service health")
    
    # Formats command
    formats_parser = subparsers.add_parser("formats", help="Get supported formats")
    
    # Global options
    parser.add_argument("--api-key", help="Tinfoil API key")
    parser.add_argument("--base-url", default="http://localhost:8000", help="SecureAI service URL")
    parser.add_argument("--timeout", type=int, default=300, help="Request timeout in seconds")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        # Initialize client
        client = SecureAI(
            api_key=args.api_key,
            base_url=args.base_url,
            timeout=args.timeout
        )
        
        # Execute command
        if args.command == "text":
            handle_text_redaction(client, args)
        elif args.command == "pdf":
            handle_pdf_redaction(client, args)
        elif args.command == "code":
            handle_code_redaction(client, args)
        elif args.command == "health":
            handle_health_check(client, args)
        elif args.command == "formats":
            handle_formats(client, args)
            
    except SecureAIError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if args.verbose:
            raise
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

def handle_text_redaction(client: SecureAI, args):
    """Handle text redaction command."""
    options = ProcessingOptions(
        aggressive_mode=args.aggressive,
        sensitivity_level=args.sensitivity
    )
    
    result = client.redact_text(args.content, options)
    
    if args.json:
        print(json.dumps(result.dict(), indent=2, default=str))
    else:
        if result.success:
            print("✅ Text redaction successful!")
            if result.redacted_content:
                if args.output:
                    with open(args.output, 'w') as f:
                        f.write(result.redacted_content)
                    print(f"📄 Redacted content saved to: {args.output}")
                else:
                    print("\n📝 Redacted content:")
                    print("-" * 40)
                    print(result.redacted_content)
                    print("-" * 40)
            
            if result.detected_patterns:
                print(f"🔍 Detected patterns: {', '.join(result.detected_patterns)}")
            
            if result.processing_time:
                print(f"⏱️  Processing time: {result.processing_time:.2f}s")
        else:
            print(f"❌ Redaction failed: {result.error}")

def handle_pdf_redaction(client: SecureAI, args):
    """Handle PDF redaction command."""
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"❌ File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    options = ProcessingOptions(
        aggressive_mode=args.aggressive,
        sensitivity_level=args.sensitivity
    )
    
    result = client.redact_pdf(file_path, options)
    
    if args.json:
        print(json.dumps(result.dict(), indent=2, default=str))
    else:
        if result.success:
            print("✅ PDF redaction successful!")
            if result.redacted_file_path:
                print(f"📄 Redacted PDF: {result.redacted_file_path}")
            if result.highlighted_file_path:
                print(f"🔍 Highlighted PDF: {result.highlighted_file_path}")
            
            if result.detected_patterns:
                print(f"🔍 Detected patterns: {', '.join(result.detected_patterns)}")
            
            if result.processing_time:
                print(f"⏱️  Processing time: {result.processing_time:.2f}s")
        else:
            print(f"❌ Redaction failed: {result.error}")

def handle_code_redaction(client: SecureAI, args):
    """Handle code redaction command."""
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"❌ File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    options = ProcessingOptions(
        aggressive_mode=args.aggressive,
        sensitivity_level=args.sensitivity
    )
    
    result = client.redact_code(file_path, options)
    
    if args.json:
        print(json.dumps(result.dict(), indent=2, default=str))
    else:
        if result.success:
            print("✅ Code redaction successful!")
            if result.redacted_file_path:
                print(f"📄 Redacted code: {result.redacted_file_path}")
            
            if result.detected_patterns:
                print(f"🔍 Detected patterns: {', '.join(result.detected_patterns)}")
            
            if result.processing_time:
                print(f"⏱️  Processing time: {result.processing_time:.2f}s")
        else:
            print(f"❌ Redaction failed: {result.error}")

def handle_health_check(client: SecureAI, args):
    """Handle health check command."""
    health = client.health_check()
    
    if args.json:
        print(json.dumps(health, indent=2))
    else:
        status = health.get("status", "unknown")
        if status == "healthy":
            print("✅ Service is healthy")
        else:
            print(f"⚠️  Service status: {status}")
        
        print(f"🕒 Uptime: {health.get('uptime', 0):.1f}s")
        print(f"📊 Version: {health.get('version', 'unknown')}")

def handle_formats(client: SecureAI, args):
    """Handle formats command."""
    formats = client.get_supported_formats()
    
    if args.json:
        print(json.dumps(formats.dict(), indent=2))
    else:
        print("📋 Supported Formats:")
        print("-" * 40)
        
        for category, format_list in formats.supported_formats.items():
            print(f"\n{category.upper()}:")
            for fmt in format_list:
                print(f"  • {fmt}")
        
        print(f"\n📏 Max file size: {formats.max_file_size}")

if __name__ == "__main__":
    main() 