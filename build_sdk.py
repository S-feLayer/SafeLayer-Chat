#!/usr/bin/env python3
"""
Build script for SecureAI SDK

This script builds and packages the SDK for distribution.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        sys.exit(1)

def clean_build():
    """Clean previous build artifacts."""
    print("🧹 Cleaning previous build artifacts...")
    
    # Remove build directories
    for dir_name in ['build', 'dist', '*.egg-info']:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}")
    
    # Remove Python cache
    for cache_dir in Path('.').rglob('__pycache__'):
        shutil.rmtree(cache_dir)
        print(f"   Removed {cache_dir}")
    
    print("✅ Clean completed")

def build_sdk():
    """Build the SDK package."""
    print("🔨 Building SecureAI SDK...")
    
    # Build the package
    run_command("python setup.py sdist bdist_wheel", "Building package")
    
    # List built packages
    dist_dir = Path("dist")
    if dist_dir.exists():
        packages = list(dist_dir.glob("*"))
        print(f"📦 Built packages:")
        for package in packages:
            print(f"   {package.name}")

def test_sdk():
    """Test the SDK installation."""
    print("🧪 Testing SDK installation...")
    
    # Find the built wheel
    dist_dir = Path("dist")
    wheel_files = list(dist_dir.glob("*.whl"))
    
    if not wheel_files:
        print("❌ No wheel file found")
        return
    
    wheel_file = wheel_files[0]
    print(f"   Testing installation of {wheel_file.name}")
    
    # Test installation in a temporary environment
    try:
        # Install the wheel
        run_command(f"pip install {wheel_file}", "Installing wheel for testing")
        
        # Test import
        test_code = """
import sys
try:
    from secureai_sdk import SecureAI
    print("✅ SDK import successful")
    print(f"   Version: {SecureAI.__module__}")
except ImportError as e:
    print(f"❌ SDK import failed: {e}")
    sys.exit(1)
"""
        
        result = subprocess.run([sys.executable, "-c", test_code], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ SDK test passed")
            print(result.stdout.strip())
        else:
            print("❌ SDK test failed")
            print(result.stderr.strip())
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

def create_documentation():
    """Create documentation for the SDK."""
    print("📚 Creating documentation...")
    
    # Create docs directory if it doesn't exist
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    # Copy tutorial
    if Path("docs/SDK_TUTORIAL.md").exists():
        print("   ✅ SDK tutorial already exists")
    else:
        print("   ⚠️  SDK tutorial not found")
    
    # Create quick start guide
    quick_start = """# SecureAI SDK Quick Start

## Installation

```bash
pip install secureai-sdk
```

## Basic Usage

```python
from secureai_sdk import SecureAI

# Initialize client
client = SecureAI(api_key="your_tinfoil_api_key")

# Redact text
result = client.redact_text("My email is john@example.com")
print(result.redacted_content)

# Redact PDF
result = client.redact_pdf("document.pdf")
print(result.redacted_file_path)

# Redact code
result = client.redact_code("config.py")
print(result.redacted_file_path)
```

## More Information

- [Full Tutorial](SDK_TUTORIAL.md)
- [API Reference](API_REFERENCE.md)
- [Examples](examples/)
"""
    
    with open(docs/QUICK_START.md", "w") as f:
        f.write(quick_start)
    
    print("   ✅ Quick start guide created")

def main():
    """Main build process."""
    print("🚀 SecureAI SDK Build Process")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"🐍 Using Python {sys.version}")
    
    # Clean previous builds
    clean_build()
    
    # Build the SDK
    build_sdk()
    
    # Test the SDK
    test_sdk()
    
    # Create documentation
    create_documentation()
    
    print("\n" + "=" * 50)
    print("✅ SDK build completed successfully!")
    print("\n📦 Distribution packages are in the 'dist' directory")
    print("📚 Documentation is in the 'docs' directory")
    print("\n🚀 Ready for distribution!")

if __name__ == "__main__":
    main() 