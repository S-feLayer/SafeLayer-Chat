#!/usr/bin/env python3
"""
Rename Secure AI to Secure AI
This script systematically renames all Secure AI references to Secure AI throughout the codebase.
"""

import os
import re
import shutil
from pathlib import Path

def rename_directory():
    """Rename the src/secureai directory to src/secureai if it exists."""
    old_path = Path("src/secureai")
    new_path = Path("src/secureai")
    
    if old_path.exists():
        print(f"Renaming directory: {old_path} -> {new_path}")
        shutil.move(str(old_path), str(new_path))
        return True
    else:
        print(f"Directory {old_path} not found, skipping...")
        return False

def update_file_content(file_path, replacements):
    """Update file content with replacements."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        for old_text, new_text in replacements:
            content = content.replace(old_text, new_text)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {file_path}")
            return True
        return False
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def main():
    """Main function to rename all Secure AI references to Secure AI."""
    print("🔄 Renaming Secure AI to Secure AI")
    print("=" * 50)
    
    # Define replacements
    replacements = [
        # Package and module names
        ("secureai", "secureai"),
        ("Secure AI", "Secure AI"),
        ("SECUREAI", "SECUREAI"),
        
        # Specific patterns
        ("src/secureai", "src/secureai"),
        ("secureai-mcp", "secureai-mcp"),
        ("SECUREAI_ENV", "SECUREAI_ENV"),
        ("SECUREAI_LOG_LEVEL", "SECUREAI_LOG_LEVEL"),
        ("SECUREAI_CACHE_DIR", "SECUREAI_CACHE_DIR"),
        
        # Import statements
        ("from secureai", "from secureai"),
        ("import secureai", "import secureai"),
        
        # GitHub URLs
        ("github.com/postralai/secureai", "github.com/postralai/secureai"),
        
        # Log files
        ("logs/secureai.log", "logs/secureai.log"),
        
        # Comments and descriptions
        ("Secure AI MCP", "Secure AI MCP"),
        ("Secure AI universal redaction", "Secure AI universal redaction"),
        ("Secure AI includes", "Secure AI includes"),
        ("Secure AI provides", "Secure AI provides"),
        ("Secure AI acts as", "Secure AI acts as"),
        
        # Business plan references
        ("Secure AI AI Privacy Shield", "Secure AI Privacy Shield"),
        
        # Documentation references
        ("Testing Guide for Secure AI", "Testing Guide for Secure AI"),
        ("Secure AI Dependency Installer", "Secure AI Dependency Installer"),
        ("Installing Secure AI Dependencies", "Installing Secure AI Dependencies"),
        ("Secure AI Performance Optimization", "Secure AI Performance Optimization"),
        
        # Installation references
        ("Installation script for Secure AI", "Installation script for Secure AI"),
        ("Performance Optimization Script for Secure AI", "Performance Optimization Script for Secure AI"),
    ]
    
    # Get all Python files, markdown files, and configuration files
    file_extensions = ['.py', '.md', '.yml', '.yaml', '.json', '.toml', '.txt', '.sh', '.ps1']
    
    updated_files = 0
    total_files = 0
    
    for root, dirs, files in os.walk('.'):
        # Skip git directory and other system directories
        if '.git' in root or '__pycache__' in root or 'node_modules' in root:
            continue
            
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root, file)
                total_files += 1
                
                if update_file_content(file_path, replacements):
                    updated_files += 1
    
    # Rename directory if it exists
    if rename_directory():
        print("✅ Directory renamed successfully")
    
    print(f"\n✅ Renaming complete!")
    print(f"📁 Total files processed: {total_files}")
    print(f"📝 Files updated: {updated_files}")
    
    print("\n🔍 Key changes made:")
    print("   - Package name: secureai → secureai")
    print("   - Directory: src/secureai → src/secureai")
    print("   - Service name: secureai-mcp → secureai-mcp")
    print("   - Environment variables: SECUREAI_* → SECUREAI_*")
    print("   - Import statements: from secureai → from secureai")
    print("   - Documentation: All Secure AI references → Secure AI")
    
    print("\n📋 Next steps:")
    print("1. Test the installation: pip install -e .")
    print("2. Run tests: python -m pytest")
    print("3. Update any remaining references manually")
    print("4. Update documentation and README files")

if __name__ == "__main__":
    main() 