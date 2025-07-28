#!/usr/bin/env python3
"""
Setup script for SecureAI SDK
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="privacy-firewall-sdk",
    version="1.0.0",
    author="Privacy Firewall Team",
    author_email="support@privacyfirewall.com",
    description="Universal Privacy Firewall SDK for PDFs, Code Files, and Text Content",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/privacyfirewall/privacy-firewall-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/privacyfirewall/privacy-firewall-sdk/issues",
        "Documentation": "https://docs.privacyfirewall.com",
        "Source Code": "https://github.com/privacyfirewall/privacy-firewall-sdk",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Filters",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "pre-commit>=2.20.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "privacyfirewall=firewall_sdk.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="privacy, security, redaction, pdf, code, text, ai, data-protection",
) 