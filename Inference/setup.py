#!/usr/bin/env python3
"""
Environment Configuration Analysis Tool Setup Script
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text(encoding="utf-8").strip().split("\n")
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith("#")]

setup(
    name="env-config-analyzer",
    version="1.0.0",
    description="A Python environment configuration error detection and repair tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Environment Analysis Team",
    author_email="team@example.com",
    url="https://github.com/example/env-config-analyzer",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "configs": ["*.yaml", "*.json"],
        "docs": ["*.md"],
    },
    install_requires=requirements,
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "env-analyzer=run:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    keywords="environment configuration analysis error detection python",
)