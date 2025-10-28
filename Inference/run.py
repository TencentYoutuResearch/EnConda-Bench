#!/usr/bin/env python3
"""
Main Entry Point for Environment Configuration Analysis Tool

This file serves as the primary entry point for the EnConda-Bench inference system.
It provides a simple interface to launch the environment configuration analysis tool
with support for both LLM and Agent-based analysis modes.

"""

import sys
from pathlib import Path

# Add project root directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and execute main program
from scripts.run_analysis import main

if __name__ == "__main__":
    main()